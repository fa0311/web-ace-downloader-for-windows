import requests
import json
import os
import time
import img2pdf
import glob
import re

class web_ace_downloader:
    def __init__(self, dir="./"):
        self.file = 0
        self.session = requests.session()
        self.dir = dir
        self.ADDRESS = "https://web-ace.jp"

    def __get_headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }

    def auto_list_download(self, url, sleeptime=2, pdfConversion=True, zero_padding=True):
        self.get_product(url)
        self.json_download(url)
        self.file = 0
        if os.path.isdir(self.dir + self.product["title"]) != True:
            os.mkdir(self.dir + self.product["title"])
        for page in self.list:
            time.sleep(sleeptime)
            self.download(page, False)
            self.output(self.dir + self.product["title"] + "/", zero_padding=zero_padding)
        if pdfConversion:
            self.convertToPdf(self.dir + self.product["title"] + "/")

    def json_download(self, url):
        # Counterfeit User agent for absolutely successfully connection.
        json_data = self.session.get(url + "/json/", headers=self.__get_headers()).text
        self.list = json.loads(json_data)

    def get_product(self, url):
        response = self.session.get(url)
        if response.status_code != 200:
            raise Exception('Request Error')
        reg_next_readable = r'<div class="viewerbtn_toNext"><a href="([a-z0-9\/]*?)">次の話へ<i class="fa-chevron-right"></i></a></div>'
        reg_title = r'<title>(.*?)｜ヤングエースUP - 無料で漫画が読めるWebコミックサイト</title>'
        self.product = {
            "next_readable" : self.ADDRESS + re.findall(reg_next_readable, response.text)[0],
            "title" : re.findall(reg_title, response.text)[0],
        }

    def json_localread(self, filepath):
        with open(filepath) as json_file:
            json_data = json.load(json_file)
            self.list = json_data

    def download(self, url, fakeque=False):
        if fakeque:
            print("Emulating Download : " + url)
            self.img = url
        else:
            self.img = self.session.get(self.ADDRESS + url, headers=self.__get_headers())

    def output(self, dir,zero_padding=True):
        file = str(self.file)
        if zero_padding:
            index = 1
            zfill = 0
            while len(self.list) >= index:
                index *= 10
                zfill += 1
            file = file.zfill(zfill)
        with open(dir + file + ".jpg", mode='wb') as f:
            f.write(self.img.content)
        self.file += 1

    def convertToPdf(self, dir):
        img = [i.replace("\\","/") for i in glob.glob(f"{dir}/*") if not i.endswith(".pdf")]
        with open(dir + "output.pdf", "wb") as f:
            f.write(img2pdf.convert(img))

    # A simple Json Dumper for debugging.
    def dumpSimplifiedJson(self, jsObject):
        f = open("JSON.json", "w")
        json.dump(
            jsObject,
            f,
            ensure_ascii=False,
            indent=4,
            sort_keys=True,
            separators=(",", ": "),
        )