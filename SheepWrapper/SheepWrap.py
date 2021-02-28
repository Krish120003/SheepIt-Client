import patoolib
import time
import sys
import shutil
import logging
import json
import os
import urllib
import threading

import requests
import tempfile
import xmltodict
import coloredlogs

from .downloader import Downlader
from .Renderer import RenderStatus, RenderTask
from . import utils


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
)

coloredlogs.install(level="INFO")


class SheepJob(threading.Thread):
    def __init__(self, sess, ops, data, working_dir):
        threading.Thread.__init__(self)
        self.daemon = True
        self.sess = sess
        self.name = data["@name"]
        self.job_id = data["@id"]
        self.file_name = data["@path"]
        self.frame = data["@frame"]
        self.validation_url = data["@validation_url"]
        self.password = data["@password"] if data["@password"] else None
        self.working_dir = working_dir
        self.data = data
        self.ops = ops

        self.engine = None

        self.state = "Initializing Job"
        self.progress = None
        self.started = False

        self.renderer = {
            "engine": "CYCLES"
            if "--engine CYCLES" in data["renderer"]["@commandline"]
            else "EEVEE",
            "script": data["script"],
            "hash": data["renderer"]["@md5"],
        }

        self.render_start = None

        self.status = {"code": 0}

        self.output_file = None

        logging.debug(working_dir)

    def ping(self):
        r = self.sess.post(
            self.ops["keepmealive"],
            params={"job": self.job_id, "frame": self.frame, "extras": ""},
        )
        logging.info(f"Session Heartbeat Sent" + str(r.content))

    def get_binary(self):
        self.bin_file_zip = os.path.abspath(
            os.path.join(f"binaries/{self.renderer.get('hash')}.zip")
        )
        if os.path.exists(self.bin_file_zip):
            pass
        else:
            d = Downlader(
                self.sess,
                self.ops["download-archive"] + f"?type=binary&job={self.job_id}",
                self.bin_file_zip,
            )
            d.run()

    def get_blend(self):
        self.blend_file_zip = os.path.abspath(
            os.path.join(f"blends/{self.data.get('@archive_md5','default')}.zip")
        )

        if os.path.exists(self.blend_file_zip):
            pass

        d = Downlader(
            self.sess,
            self.ops["download-archive"] + f"?type=job&job={self.job_id}",
            self.blend_file_zip,
        )
        d.run()

    def create_script(self):
        with open(os.path.join(os.getcwd(), "worker/script.py"), "w") as f:
            f.write(
                self.renderer["script"]
                + """\n
sheepit_set_compute_device("NONE", "CPU", "CPU")
bpy.context.scene.render.tile_x = 32
bpy.context.scene.render.tile_y = 32
import signal
def hndl(signum, frame):
    pass
signal.signal(signal.SIGINT, hndl)
                    """
            )

    def upload_frame(self):
        url = urllib.parse.unquote(self.validation_url)
        params = {
            "rendertime": round(abs(time.time() - self.render_start)),
            "frame": self.frame,
            "cores": 12,
            "extras": "",
            "memoryused": 1024 * 1024,
        }
        upload_name = None

        for file in os.listdir(os.path.join(os.getcwd(), "worker/")):
            if file.endswith("_out.png"):
                upload_name = file
                break

        self.output_file = os.path.join(os.getcwd(), f"worker/{upload_name}")

        f = open(os.path.join(os.getcwd(), f"worker/{upload_name}"), "rb")
        files = {"file": (upload_name, f)}
        try:
            r = self.sess.post(url, params=params, files=files)
            # ADD ERROR CHECKING LATER
            if (
                int(
                    json.loads(json.dumps(xmltodict.parse(r.content)))["jobvalidate"][
                        "@status"
                    ]
                )
                != 0
            ):
                logging.error(f"Job {self.job_id} - Frame Upload Failed")
            else:
                logging.info(f"Job {self.job_id} - Frame Upload Complete")

        except Exception as e:
            print(e)
            f.close()
        f.close()

    def render(self):
        self.engine = RenderTask(
            os.path.join(os.getcwd(), "worker/rend.exe"),
            os.path.join(os.getcwd(), f"worker/{self.file_name}"),
            os.path.join(os.getcwd(), "worker/########_out.png"),
            os.path.join(os.getcwd(), "worker/script.py"),
            self.frame,
        )
        self.engine.start()

        t = 1

        while True:
            logging.info(
                f"Job {self.job_id} - Renderer Info - {round((self.engine.tiles[0]/self.engine.tiles[1])*100, 2)}%"
            )
            if self.engine.status == RenderStatus.DONE:
                break
            if t % 12 == 0:
                self.ping()
            time.sleep(5)
            t += 1

    def run(self):
        self.started = True
        if os.path.exists(os.path.join(os.getcwd(), "worker/")):
            shutil.rmtree(os.path.join(os.getcwd(), "worker/"))
            logging.info("Cleared worker library.")

        logging.info(f"Job {self.job_id} - Started Binary Download")
        self.state = "Downloading Blender"
        self.get_binary()
        logging.info(f"Job {self.job_id} - Finished Binary Download")

        logging.info(f"Job {self.job_id} - Started Blend Download")
        self.state = "Downloading Project"
        self.get_blend()
        logging.info(f"Job {self.job_id} - Finished Blend Download")

        logging.info(f"Job {self.job_id} - Extracting Renderer")
        self.state = "Extracting Renderer"
        patoolib.extract_archive(
            self.bin_file_zip, outdir=os.path.join(os.getcwd(), "worker/"), verbosity=-1
        )
        logging.info(f"Job {self.job_id} - Extraction Complete")

        logging.info(f"Job {self.job_id} - Extracting Project")
        self.state = "Extracting Project"
        patoolib.extract_archive(
            self.blend_file_zip,
            outdir=os.path.join(os.getcwd(), "worker/"),
            verbosity=-1,
            password=self.password,
        )
        logging.info(f"Job {self.job_id} - Extraction Complete")

        logging.info(f"Job {self.job_id} - Creating Script File")
        self.create_script()
        logging.info(f"Job {self.job_id} - Script Creation Complete")

        logging.info(f"Job {self.job_id} - Starting Rendering")
        self.render_start = time.time()
        self.render()
        self.state = "Finishing Up"
        logging.info(f"Job {self.job_id} - Rendering Complete")

        logging.info(f"Job {self.job_id} - Starting Frame Upload")
        self.state = "Uploading Project"
        self.upload_frame()
        self.state = "Done"


class SheepItInterface:
    # Main Class For Networking
    def __init__(self, working_dir=os.path.join(tempfile.gettempdir(), "/SClient/")):
        logging.info("INIT")
        self.baseURL = "https://sheepit-renderfarm.com"
        self.VERSION = "6.21055.0"
        self.ops = {}
        self.working_dir = working_dir

        # Setup Web Session
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Python/3.9.1"})

        self.job = None

    def login(self, username, password, ram="default"):
        params = utils.sheep_system_info()

        self.username = username
        self.password = password

        params["version"] = self.VERSION
        params["login"] = self.username
        params["password"] = self.password
        params["ram"] = (params["ram_max"] // 2) if ram == "default" else int(ram)

        r = self.session.get(self.baseURL + "/server/config.php", params=params)
        if r.status_code != 200:
            raise Exception("Request Failed")

        data = json.loads(json.dumps(xmltodict.parse(r.content)))

        try:
            status = int(data.get("config").get("@status"))

            if status == 101:
                raise Exception("Update Required")
            elif status == 102:
                raise Exception("Auth Failed")

            for op in data.get("config").get("request"):
                self.ops[op["@type"]] = self.baseURL + op["@path"]

            self.password = data.get("config").get("@publickey")
            logging.info("Login Successful")
            return data.get("config").get("@publickey")

        except:
            raise Exception("Incomplete Data")

    def logout(self, *args, **kwargs):
        r = self.session.get(self.ops["logout"])
        logging.info("Client Logged Out")
        if args or kwargs:
            sys.exit()
        return r

    def get_job(self, job_type):
        if self.job:
            try:
                self.job.engine.process.terminate()
            except Exception as e:
                logging.error(e)
        r = self.session.get(self.ops["request-job"], params={"computemethod": "1"})
        if r.status_code != 200:
            logging.error("Job Request Failed")
            raise Exception("Request Failed")

        data = json.loads(json.dumps(xmltodict.parse(r.content)))["jobrequest"]

        # print(data)

        # logging.info(data)

        try:
            status = int(data.get("@status"))
            if status == 200:
                # Somehow indicate a wait, and return updated stats
                return "No Job"
            elif status == 201:
                # WIP
                return
            elif status == 202:
                self.login(self.username, self.password)
                return self.get_job(job_type)
            elif status in [203, 204]:
                # WIP
                return
            elif status in [206, 207]:
                # WIP
                return
            elif status == 0:
                self.job = SheepJob(
                    self.session, self.ops, data.get("job"), self.working_dir
                )
                return data.get("stats")

        except:
            raise Exception("Incomplete Data")


if __name__ == "__main__":
    import signal
    import sys

    s = SheepItInterface()

    signal.signal(signal.SIGINT, s.logout)

    s.login(input("Username: "), input("Password / Render Key: "))
    while True:
        s.get_job(1)
        s.job.start()
