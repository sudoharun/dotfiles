from pathlib import Path
from ignis.app import IgnisApp
from ignis import utils
from windows.bar import Bar
from windows.app_runner import Launcher
from windows.notifications import NotificationsPopups, NotificationsCentrePlusCalendar
from windows.osd import RootOSDWindow
from windows.quick_settings import QuickSettings

scss = str(Path(__file__).parent.resolve() / "styles" / "styles.scss")
app = IgnisApp.get_initialized()
app.apply_css(scss)

for monitor in range(utils.get_n_monitors()):
    Launcher(monitor)
    NotificationsCentrePlusCalendar(monitor)
    RootOSDWindow(monitor)
    QuickSettings(monitor)
    Bar(monitor)
    NotificationsPopups(monitor) # Under bar to prevent first notification getting cut off underneath bar
