const hyprland = await Service.import("hyprland");

const dispatch = (ws) => hyprland.messageAsync(`dispatch workspace ${ws}`);

const Workspaces = Widget.EventBox({
  className: "workspaces",
  hexpand: false,
  onScrollUp: () => dispatch("+1"),
  onScrollDown: () => dispatch("-1"),
  child: Widget.Box({
    children: Array.from({ length: 10 }, (_, i) => i + 1).map((i) =>
      Widget.Button({
        attribute: i,
        label: `${i}`,
        onClicked: () => dispatch(i),
      }),
    ),

    setup: (self) =>
      self.hook(hyprland, () =>
        self.children.forEach((btn) => {
          if (btn.attribute === hyprland.active.workspace.id) {
            btn.class_name = "active-ws workspace";
          } else if (
            hyprland.workspaces.some((ws) => ws.id === btn.attribute)
          ) {
            btn.class_name = "occupied-ws workspace";
          } else {
            btn.class_name = "workspace";
          }
        }),
      ),
  }),
});

export const WorkspacesContainer = Widget.Box({
  className: "workspaces-container",
  hexpand: false,
  hpack: "start",
  child: Workspaces,
});
