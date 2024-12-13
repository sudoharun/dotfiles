import sys
import versions
from gi.repository import AstalIO, Astal, Gio
from Notifications import NCWindow, NPWindow
from pathlib import Path

scss = str(Path(__file__).parent.resolve() / "style.scss")
css = "/tmp/style.css"

class App(Astal.Application):
    def do_astal_application_request(
        self, msg: str, conn: Gio.SocketConnection
    ) -> None:
        print(msg)
        AstalIO.write_sock(conn, "hello")

    def do_activate(self) -> None:
        self.hold()
        AstalIO.Process.execv(["sass", scss, css])
        self.apply_css(css, True)
        print("hello")
        self.add_window(NCWindow(self.get_monitors()[0]))
        self.add_window(NPWindow(self.get_monitors()[0]))

instance_name = "notifications"
app = App(instance_name=instance_name)

if __name__ == "__main__":
    try:
        print(app.acquire_socket())
        app.run(None)
    except Exception as e:
        print(AstalIO.send_message(instance_name, "".join(sys.argv[1:])))
