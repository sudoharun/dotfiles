from ctypes import CDLL
CDLL('libgtk4-layer-shell.so')

import sys
import versions
from pathlib import Path

from gi.repository import AstalIO, Astal, Gio

from windows.Bar import Bar
from windows.Desktop import Desktop, LeftEdge, RightEdge, TopEdge
from windows.NotificationPopups import NotificationPopups
from windows.OSDs import OSDWindow

scss = str(Path(__file__).parent.resolve() / "style" / "default.scss")
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
        Desktop(self)
        LeftEdge(self)
        TopEdge(self)
        RightEdge(self)
        OSDWindow(self)
        Bar(self)

application_id = "com.harun.astal"
instance_name = "gtk4"
app = App(application_id=application_id, instance_name=instance_name)

if __name__ == "__main__":
    try:
        app.acquire_socket()
        app.run(None)
    except Exception as e:
        print(AstalIO.send_message(instance_name, "".join(sys.argv[1:])))
