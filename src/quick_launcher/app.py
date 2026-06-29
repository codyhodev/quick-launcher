import sys

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QPixmap, QPolygon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon

from quick_launcher.config import Config, default_config_path, load_config
from quick_launcher.menu import build_menu


ICON_SIZE = 64


def create_rocket_icon() -> QIcon:
    pixmap = QPixmap(ICON_SIZE, ICON_SIZE)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#3498db"))

    cx, cy = ICON_SIZE // 2, ICON_SIZE // 2
    w, h = 16, 32
    left, top = cx - w // 2, cy - h // 2

    painter.drawRoundedRect(left, top + h // 3, w, h * 2 // 3, 2, 2)

    nose = QPolygon([
        QPoint(cx, top),
        QPoint(cx - 10, top + h // 3),
        QPoint(cx + 10, top + h // 3),
    ])
    painter.drawPolygon(nose)

    fin_left = QPolygon([
        QPoint(left - 2, top + h - 8),
        QPoint(left - 2, top + h + 4),
        QPoint(left + 6, top + h - 4),
    ])
    fin_right = QPolygon([
        QPoint(left + w + 2, top + h - 8),
        QPoint(left + w + 2, top + h + 4),
        QPoint(left + w - 6, top + h - 4),
    ])
    painter.drawPolygon(fin_left)
    painter.drawPolygon(fin_right)

    painter.setBrush(QColor("#e74c3c"))
    flame = QPolygon([
        QPoint(cx - 4, top + h + 4),
        QPoint(cx + 4, top + h + 4),
        QPoint(cx, top + h + 14),
    ])
    painter.drawPolygon(flame)

    painter.end()
    return QIcon(pixmap)


class TrayApp(QSystemTrayIcon):
    def __init__(self, config: Config) -> None:
        super().__init__()
        menu = build_menu(config.launchers, config.terminal_cmd)
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(self._quit)
        self.setContextMenu(menu)
        self.setIcon(create_rocket_icon())

    def _quit(self) -> None:
        QApplication.instance().quit()


def main() -> None:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    tray = TrayApp(load_config())
    tray.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
