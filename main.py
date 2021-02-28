# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtGui import QGuiApplication, QFontDatabase
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, QTimer, Slot, Signal

import logging
import time
import math
import sys

from SheepWrapper import SheepItInterface, RenderStatus


class SheepQtInterface(QObject):

    setPause = Signal(bool)
    setStatus = Signal(str)
    setStatusColor = Signal(str)
    setSessionTime = Signal(str)
    setProgressPercent = Signal(str)
    setTimeElasped = Signal(str)
    setEngineDetails = Signal(str)

    setFramesRendered = Signal(int)
    setProgress = Signal(int)
    setSessionPoints = Signal(int)
    setUserPoints = Signal(int)

    def __init__(self):
        QObject.__init__(self)

        # Statics
        self.colors = {"rendering": "2CC056", "processing": "FE9905"}
        self.interface = SheepItInterface()
        self.interface.login("FlipFX", "24a137Eem5XZDHosUqWNHHRcE7Wq7TulA3k8BTSe")

        # States
        self.session_start = time.time()
        self.paused = False
        self.color = self.colors.get("processing")
        self.status = "Starting"
        self.progress = 10000
        self.frame_time_elasped = ""
        self.percent_progress = ""
        self.job_name = ""
        self.frames_rendered = 0
        self.session_points = 0
        self.total_points = 0

        # UI Update Loop
        self.uiTimer = QTimer()
        self.uiTimer.timeout.connect(self.updateUI)
        self.uiTimer.start(33)

        # Interaction Update Loop
        self.interactTimer = QTimer()
        self.interactTimer.timeout.connect(self.interact)
        self.interactTimer.start(33)

        # Paused Ping
        self.paused_ping_counter = 1

    def interact(self):
        if not self.paused:
            # Requesting Jobs
            if not self.interface.job:
                logging.info("No current job, requesting one")
                stats = self.interface.get_job(1)
                try:
                    self.session_points = stats["@credits_session"]
                    self.total_points = stats["@credits_total"]

                    self.setSessionPoints.emit(self.session_points)
                    self.setUserPoints.emit(self.total_points)
                except:
                    pass

            if self.interface.job and self.interface.job.state == "Done":
                logging.info("Job complete, requesting new job")
                self.frames_rendered += 1
                stats = self.interface.get_job(1)
                try:
                    self.session_points = stats["@credits_session"]
                    self.total_points = stats["@credits_total"]

                    self.setSessionPoints.emit(self.session_points)
                    self.setUserPoints.emit(self.total_points)
                except:
                    pass

            if not self.interface.job.started:
                self.interface.job.start()

            self.status = self.interface.job.state
            if self.interface.job.engine:
                self.frame_time_elasped = self.interface.job.engine.time_elapsed
                self.job_name = self.interface.job.file_name.replace(".blend", "")
                if self.interface.job.engine.status == RenderStatus.RENDERING:
                    temp = self.interface.job.engine.tiles
                    self.progress = round(temp[0] / temp[1] * 10000)
                    self.percent_progress = str(round(temp[0] / temp[1] * 100)) + "%"

                    self.color = self.colors.get("rendering")

                    self.status = "Rendering"

                elif self.interface.job.engine.status == RenderStatus.COMPOSITING:
                    self.progress = 10000
                    self.percent_progress = "100%"

                    self.color = self.colors.get("processing")

                    self.status = "Compositing"

                else:
                    self.progress = 10000
                    self.percent_progress = ""

                    self.color = self.colors.get("processing")
            else:
                pass

        else:
            if self.paused_ping_counter % 120 == 0:
                self.interface.job.ping()
            self.paused_ping_counter += 1

    def updateUI(self):
        self.setStatus.emit(self.status)
        self.setStatusColor.emit(self.color)
        self.setProgress.emit(self.progress)
        self.setProgressPercent.emit(self.percent_progress)
        self.setTimeElasped.emit(self.frame_time_elasped)
        self.setEngineDetails.emit(
            f"Cycles - CPU - {self.job_name}" if self.job_name else ""
        )
        self.setFramesRendered.emit(self.frames_rendered)
        self.setSessionTime.emit(self._format_time(time.time(), self.session_start))

    def _format_time(self, t1, t2):
        t = math.ceil(t1 - t2)
        s = ""
        added = 0
        if (24 * 60 * 60) - 1 < t:
            days = t // (24 * 60 * 60)
            s += str(round(days)) + (" day " if days == 1 else " days ")
            t -= days * 24 * 60 * 60
            added += 1
        if (60 * 60) - 1 < t and added != 2:
            hours = t // (60 * 60)
            s += str(round(hours)) + (" hour " if hours == 1 else " hours ")
            t -= hours * 60 * 60
            added += 1
        if 59 < t and added != 2:
            mins = t // 60
            s += str(round(mins)) + (" min " if mins == 1 else " mins ")
            t -= mins * 60
            added += 1
        if added != 2:
            seconds = round(t)
            s += str(seconds) + " s "
        return s.strip()

    @Slot()
    def togglePause(self):
        self.paused = not self.paused
        self.setPause.emit(self.paused)

    @Slot()
    def safeClose(self):
        try:
            self.interface.logout()
        except Exception as e:
            logging.error("SheepIt Logout Failed")


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
