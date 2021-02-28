# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtGui import QGuiApplication, QFontDatabase
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, QTimer, Slot, Signal


class SheepQtInterface(QObject):

    setPause = Signal(bool)

    def __init__(self):
        QObject.__init__(self)

        self.paused = False
        self.setStatus = Signal(str)

    @Slot()
    def togglePause(self):
        self.paused = not self.paused
        self.setPause.emit(self.paused)


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    QFontDatabase.addApplicationFont("assets/Roboto/Roboto-Medium.ttf")

    engine = QQmlApplicationEngine()

    main = SheepQtInterface()
    engine.rootContext().setContextProperty("backend", main)

    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
