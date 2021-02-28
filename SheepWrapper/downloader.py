import requests
import threading
import pathlib
import os


class Downlader(threading.Thread):
    def __init__(self, sess, url, location):
        threading.Thread.__init__(self)
        self.state = 0
        self.url = url
        self.file_size = 1
        self.downloaded = 0
        self.location = location
        self.sess = sess

    def get_part(self, start, end):
        start = int(start)
        end = int(end)
        headers = {"Range": f"bytes={start}-{end}"}
        # print(headers["Range"])
        return self.sess.get(self.url, headers=headers).content

    def run(self, part=1024 * 1024):

        if not os.path.exists(pathlib.Path(self.location).parent):
            os.makedirs(pathlib.Path(self.location).parent)

        with open(self.location, "w+b") as f:
            f.write(self.sess.get(self.url).content)

        return

        """
        # LEGACY
        print("STARTING")
        r = self.sess.head(self.url)
        if r.status_code == 302:
            print(r.headers)
            self.url = r.headers.get("Location")
            r = self.sess.head(self.url)
        print("HEADERS DOWNLOADED")

        print(r.headers)

        self.file_size = int(r.headers["content-length"])
        temp = self.file_size

        start = 0

        if not os.path.exists(pathlib.Path(self.location).parent):
            os.makedirs(pathlib.Path(self.location).parent)

        if self.file_size <= part:
            with open(self.location, "w+b") as f:
                print(self.url)
                download = self.sess.get(self.url)
                print(download.content)
                print(download.status_code)
                print(download.headers)
                f.write(download.content)
            self.downloaded = self.file_size
            print("Done writing small file")
            return

        with open(self.location, "w+b") as f:
            while temp > 0:
                print("Loop?")

                end = start + min(part - 1, temp)

                part_data = self.get_part(start, end)
                f.write(part_data)

                start += part
                temp -= part

                self.downloaded = end

            self.downloaded = self.file_size

        return
        """
