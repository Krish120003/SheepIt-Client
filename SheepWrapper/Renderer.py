from subprocess import Popen, PIPE
import threading
import os
import re
import time

import logging


class RenderStatus:
    ERROR = -1
    NONE = 0
    STARTING = 1
    RENDERING = 2
    COMPOSITING = 3
    DONE = 4


class RenderTask(threading.Thread):
    def __init__(
        self, executable_path, file_path, output_path, script_path, frame_number
    ):
        threading.Thread.__init__(self)
        self.daemon = True
        self.default_args = [
            "--factory-startup",
            "--disable-autoexec",
            "-noaudio",
            "-b",
        ]
        self.status = RenderStatus.NONE
        self.time_elapsed = ""
        self.time_remaining = ""
        self.tiles = (0, 1)
        self.max_mem = 0

        self.executable_path = executable_path
        self.file_path = file_path
        self.output_path = output_path
        self.frame_number = frame_number
        self.script_path = script_path

    def run(self):
        self.process = Popen(
            [
                self.executable_path,
                *self.default_args,
                self.file_path,
                "-o",
                self.output_path,
                "--python",
                self.script_path,
                "-f",
                str(self.frame_number),
            ],
            stdout=PIPE,
            stderr=PIPE,
        )

        self.status = RenderStatus.STARTING

        while self.process.poll() == None:
            self.process_output(self.process.stdout.readline().decode())
            logging.debug(
                " | ".join(
                    [
                        str(self.status),
                        str(self.time_elapsed),
                        str(self.time_remaining),
                        str(self.tiles),
                        str(self.max_mem),
                    ]
                )
            )

        self.status = RenderStatus.DONE

    def process_output(self, line):
        logging.debug(line.strip())
        # print(line)
        if "render" in line.lower():
            self.status = RenderStatus.RENDERING
        r = re.search("Time:([a-zA-Z0-9:.]+)", line)
        if r:
            self.time_elapsed = r.group(1)
        r = re.search("Remaining:([a-zA-Z0-9:.]+)", line)
        if r:
            self.time_remaining = r.group(1)
        r = re.search("Rendered ([0-9]+)\/([0-9]+)", line)
        if r:
            self.tiles = (int(r.group(1)), int(r.group(2)))
        r = re.search("Peak ([0-9.]+)M", line)
        if r:
            self.max_mem = float(r.group(1))
        if "Compositing" in line:
            self.status = RenderStatus.COMPOSITING


if __name__ == "__main__":
    executable_path = "/home/krish/Documents/Tests/Blender-sheep/96a408177b324f9172d137b4db117924/rend.exe"
    file_path = "/home/krish/Documents/Projects/SClient/Blub.blend"
    output_path = "/home/krish/Documents/Projects/SClient/out"

    task = RenderTask(executable_path, file_path, output_path, "", 0)
    task.start()

    while task.status != RenderStatus.DONE:
        print(
            task.status,
            (str(round(100 * task.tiles[0] / task.tiles[1], 2)) + "%").center(6),
            str(task.tiles).center(16),
            "Elapsed: " + task.time_elapsed,
            "Remaining: " + task.time_remaining,
        )
        time.sleep(0.2)
