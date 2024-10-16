import sys
import versions
from gi.repository import Astal, Gio
from windows.Notifications import NotifWindow
from pathlib import Path

scss = str(Path(__file__).parent.resolve() / "styles.scss")
css = "/tmp/style.css"

class App(Astal.Application):
    def do_request(self, msg: str, conn: Gio.SocketConnection) -> None:
        print(msg)
        Astal.write_sock(conn, "hello")

    def do_activate(self) -> None:
        self.hold()
        Astal.Process.execv(["sass", scss, css])
        self.apply_css(css, True)
        for mon in self.get_monitors():
            self.add_window(NotifWindow(mon))


instance_name = "notifications"
app = App(instance_name=instance_name)

if __name__ == "__main__":
    if app.acquire_socket():
        app.run(None)
    else:
        print(Astal.Application.send_message(instance_name, "".join(sys.argv[1:])))
