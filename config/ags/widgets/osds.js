// Powermenu

const PowerMenuWidget = Widget.Box({
  class_name: "powermenu",
  children: [
    Widget.Button({
      class_name: "powermenu-item",
      on_primary_click_release: () => {
        App.ToggleWindow("powermenu");
        Utils.execAsync("hyprlock");
      },
      child: Widget.Icon({
        icon: "system-lock-screen-symbolic",
        size: 64,
      }),
    }),
    Widget.Button({
      class_name: "powermenu-item",
      on_primary_click_release: () => {
        App.ToggleWindow("powermenu");
        Utils.exec("bash -c 'hyprlock & sleep 1 && systemctl suspend'");
      },
      child: Widget.Icon({
        icon: "system-suspend-symbolic",
        size: 64,
      }),
    }),
    Widget.Button({
      class_name: "powermenu-item",
      on_primary_click_release: () => {
        App.ToggleWindow("powermenu");
        Utils.exec("pkill Hyprland");
      },
      child: Widget.Icon({
        icon: "system-log-out-symbolic",
        size: 64,
      }),
    }),

    Widget.Button({
      class_name: "powermenu-item",
      on_primary_click_release: () => {
        App.ToggleWindow("powermenu");
        Utils.exec("reboot");
      },
      child: Widget.Icon({
        icon: "system-restart-symbolic",
        size: 64,
      }),
    }),
    Widget.Button({
      class_name: "powermenu-item",
      on_primary_click_release: () => {
        App.ToggleWindow("powermenu");
        Utils.exec("shutdown -f now");
      },
      child: Widget.Icon({
        icon: "system-shutdown-symbolic",
        size: 64,
      }),
    }),
  ],
});

export const PowerMenuButton = Widget.Button({
  class_name: "powermenu-button",
  on_primary_click: () => App.ToggleWindow("powermenu"),
  child: Widget.Icon({
    icon: "system-shutdown-symbolic",
    size: 18,
  }),
});

export const PowerMenuWindow = Widget.Window({
  name: "powermenu",
  layer: "overlay",
  child: PowerMenuWidget,
  popup: true,
  keymode: "exclusive",
  visible: false,
});

// Screenshot
