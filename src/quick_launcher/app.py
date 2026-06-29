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
    painter.setBrush(QColor("#ffffff"))

    cx, cy = ICON_SIZE // 2, ICON_SIZE // 2
    w, h = 20, 44
    left, top = cx - w // 2, cy - h // 2

    painter.drawRoundedRect(left, top + h // 3, w, h * 2 // 3, 3, 3)

    nose = QPolygon([
        QPoint(cx, top),
        QPoint(cx - 12, top + h // 3),
        QPoint(cx + 12, top + h // 3),
    ])
    painter.drawPolygon(nose)

    fin_left = QPolygon([
        QPoint(left - 4, top + h - 10),
        QPoint(left - 4, top + h + 4),
        QPoint(left + 8, top + h - 6),
    ])
    fin_right = QPolygon([
        QPoint(left + w + 4, top + h - 10),
        QPoint(left + w + 4, top + h + 4),
        QPoint(left + w - 8, top + h - 6),
    ])
    painter.drawPolygon(fin_left)
    painter.drawPolygon(fin_right)

    painter.setBrush(QColor("#e74c3c"))
    flame = QPolygon([
        QPoint(cx - 6, top + h + 4),
        QPoint(cx + 6, top + h + 4),
        QPoint(cx, top + h + 18),
    ])
    painter.drawPolygon(flame)

    painter.end()
    return QIcon(pixmap)


class TrayApp(QSystemTrayIcon):
    def __init__(self, config: Config) -> None:
        super().__init__()
        menu = build_menu(config.launchers, config.terminal_cmd, config.font_size)
        quit_action = menu.addAction(config.quit_label)
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
