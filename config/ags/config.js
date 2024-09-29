import { WorkspacesContainer } from "./widgets/workspaces.js";
import { Controls } from "./controls.js";
import { NotificationPopups } from "./controls.js";
import { SysTray } from "./controls.js";
import { PowerMenuButton } from "./widgets/osds.js";
import { PowerMenuWindow } from "./widgets/osds.js";

const DateWidget = () =>
  Widget.Label({ justification: "center" }).poll(
    1000,
    (self) => (self.label = Utils.exec("date '+%I:%M%P%n%a %d %b, %Y'")),
  );

function SearchApps() {
  return Widget.Button({
    class_name: "search-button",
    on_primary_click: () => Utils.execAsync("wofi"),
    child: Widget.Icon({
      icon: "search-symbolic",
      size: 18,
    }),
  });
}

const BarLeft = Widget.Box({
  class_name: "bar-left",
  spacing: 10,
  children: [
    SearchApps(),
    Widget.Label("|"),
    WorkspacesContainer,
  ],
});

const BarRight = Widget.Box({
  class_name: "bar-right",
  hpack: "end",
  hexpand: false,
  spacing: 2,
  children: [
    Controls,
    SysTray,
    PowerMenuButton,
  ],
})

const BarWidget = Widget.CenterBox({
  start_widget: BarLeft,
  center_widget: DateWidget(),
  end_widget: BarRight,
});

const Bar = Widget.Window({
  name: "bar",
  anchor: ["top", "left", "right"],
  exclusivity: "exclusive",
  child: BarWidget,
});

App.config({
  windows: [
    Bar,
    NotificationPopups(),
    PowerMenuWindow,
  ],
  style: "./style.css",
});
