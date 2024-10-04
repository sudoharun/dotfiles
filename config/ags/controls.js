const network = await Service.import("network");
const audio = await Service.import("audio");
const battery = await Service.import("battery");
const notifications = await Service.import("notifications");
const systemtray = await Service.import("systemtray");
import brightness from "./modules/brightness.js";

// Objects
const Network = {
  icon () {
    return network[network.primary].icon_name;
  },
  connection () {
    switch (network.connectivity) {
      case 'full': {
        if (network.primary == "wifi") {
          return `Connected to ${network.wifi.ssid}`
        } else {
          return "Connected via Ethernet"
        }
      };
      case 'limited':
        return "Limited Connectivity";
      case 'unknown':
        return "Unknown Connectivity";
      default:
        return "Not Connected"
    }
  },
  strength () {
    if (network.primary == "wifi" && network.wifi.strength > 1) {
      return {
        visible: true,
        value: `Strength: ${network.wifi.strength}`
      };
    } else {
      return {
        visible: false,
        value: "",
      }
    }
  }
};


// Bar widgets

function NetworkButton() {
  return Widget.Button({
    on_primary_click: () => Utils.exec("echo 0"),
    child: Widget.Icon({ size: 18 }),
    setup: (self) =>
      self.hook(network, () => {
        self.child.icon_name = Network.icon()
        self.child.tooltip_text = Network.connection()
      }),
  });
}

function AudioButton() {
  return Widget.Button({
    on_primary_click: () => Utils.exec("echo 0"),
    child: Widget.Icon({ size: 18 }),
    setup: (self) =>
      self.hook(audio, () => {
        const vol = Math.round(audio.speaker.volume * 100);
        const icon = [
          [101, "overamplified"],
          [67, "high"],
          [34, "medium"],
          [1, "low"],
          [0, "muted"],
        ].find(([threshold]) => threshold <= vol)?.[1];
        if (!audio.speaker.is_muted) {
          self.child.icon_name = `audio-volume-${icon}-symbolic`;
          self.tooltip_text = `Volume: ${vol}%`;
        } else {
          self.child.icon_name = "audio-volume-muted-symbolic";
          self.tooltip_text = `Volume: ${vol}% (Muted)`;
        }
      }),
  });
}

function BatteryButton() {
  return Widget.Button({
    on_primary_click: () => Utils.exec("echo 0"),
    child: Widget.Icon({ size: 18 }),
    setup: (self) =>
      self.hook(battery, () => {
        self.child.icon_name = battery.icon_name;
        self.child.tooltip_text = `Battery: ${battery.percent}%`;
      }),
  });
}

export const Controls = Widget.Box({
  class_name: "controls",
  hpack: "end",
  spacing: 2,
  homogeneous: false,
  children: [NetworkButton(), AudioButton(), BatteryButton()],
});

// Control Widgets/Windows
const NetworkWidget = Widget.Box({
  children: [Widget.Label(), Widget.Button()],
  setup: (self) =>
    self.hook(network, () => {
      if (network.connectivity == "full") {
        if (network.primary == "wifi") {
          self.child.icon_name = network.wifi.icon_name;
          self.child.tooltip_text = `Strength: ${network.wifi.strength}%`;
        } else {
          self.child.icon_name = network.wired.icon_name;
          self.child.tooltip_text = "Connect via ethernet";
        }
      } else if (network.connectivity == "limited") {
        self.child.icon_name = network.wifi.icon_name;
        self.child.tooltip_text = "Limited Connectivity";
      } else if (network.connectivity == "unknown") {
        self.child.icon_name = network.wifi.icon_name;
        self.child.tooltip_text = "Unknown Connectivity";
      } else {
        self.child.icon_name = network.wifi.icon_name;
        self.child.tooltip_text = "Not Connected";
      }
    }),
});

// Systray
const SysTrayItem = (item) =>
  Widget.Button({
    class_name: "systray-item",
    child: Widget.Icon({ size: 20 }).bind("icon", item, "icon"),
    tooltipMarkup: item.bind("tooltip_markup"),
    on_primary_click: (_, event) => item.activate(event),
    on_secondary_click: (_, event) => item.openMenu(event),
  });

export const SysTray = Widget.Box({
  class_name: "systray",
  hpack: "end",
  spacing: 2,
  children: systemtray.bind("items").as((i) => i.map(SysTrayItem)),
});

// Notifications Popups

function NotificationIcon({ app_entry, app_icon, image }) {
  if (image) {
    return Widget.Box({
      css:
        `background-image: url("${image}");` +
        "background-size: contain;" +
        "background-repeat: no-repeat;" +
        "background-position: center;",
    });
  }

  let icon = "dialog-information-symbolic";
  if (Utils.lookUpIcon(app_icon)) icon = app_icon;

  if (app_entry && Utils.lookUpIcon(app_entry)) icon = app_entry;

  return Widget.Box({
    child: Widget.Icon(icon),
  });
}

// Notifications

function Notification(n) {
  const icon = Widget.Box({
    vpack: "start",
    class_name: "icon",
    child: NotificationIcon(n),
  });

  const title = Widget.Label({
    class_name: "title",
    xalign: 0,
    justification: "left",
    hexpand: true,
    max_width_chars: 18,
    truncate: "end",
    wrap: true,
    label: n.summary,
    use_markup: true,
  });

  const body = Widget.Label({
    class_name: "body",
    hexpand: true,
    use_markup: true,
    xalign: 0,
    justification: "left",
    label: n.body,
    wrap: true,
  });

  const actions = Widget.Box({
    class_name: "actions",
    children: n.actions.map(({ id, label }) =>
      Widget.Button({
        class_name: "action-button",
        on_clicked: () => {
          n.invoke(id);
          n.dismiss();
        },
        hexpand: true,
        child: Widget.Label(label),
      }),
    ),
  });

  return Widget.EventBox(
    {
      attribute: { id: n.id },
      on_primary_click: n.dismiss,
    },
    Widget.Box(
      {
        class_name: `notification ${n.urgency}`,
        vertical: true,
      },
      Widget.Box([icon, Widget.Box({ vertical: true }, title, body)]),
      actions,
    ),
  );
}

export function NotificationPopups(monitor = 0) {
  const list = Widget.Box({
    vertical: true,
    children: notifications.popups.map(Notification),
  });

  function onNotified(_, id) {
    const n = notifications.getNotification(id);
    if (n) list.children = [Notification(n), ...list.children];
  }

  function onDismissed(_, id) {
    list.children.find((n) => n.attribute.id === id)?.destroy();
  }

  list
    .hook(notifications, onNotified, "notified")
    .hook(notifications, onDismissed, "dismissed");

  return Widget.Window({
    monitor,
    name: `notifications${monitor}`,
    class_name: "notification-popups",
    anchor: ["top", "right"],
    child: Widget.Box({
      css: "min-width: 2px; min-height: 2px;",
      class_name: "notifications",
      vertical: true,
      child: list,
    }),
  });
}
