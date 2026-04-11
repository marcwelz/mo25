# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 21:04:08 2026

@author: dawud & marcwelz
"""
import threading
import urllib.request
import time

from traffic_data import *

import ssl
import urllib.request

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# source ai
def get_site_ids(folder: str) -> list[str]:
    import os
    import xml.dom.minidom

    NS: str = "http://datex2.eu/schema/2/2_0"
    files: list[str] = sorted([f for f in os.listdir(folder) if f.endswith(".xml")])
    if not files:
        return []

    dom = xml.dom.minidom.parse(os.path.join(folder, files[0]))
    env = dom.documentElement
    return [
        sm.getElementsByTagNameNS(NS, "measurementSiteReference")[0].getAttribute("id")
        for sm in env.getElementsByTagNameNS(NS, "siteMeasurements")
    ]

class Download:
    def run_download(self):
        url = "https://transport.data.gouv.fr/resources/79165/download"
        folder = "downloaded_files_2"
        index = 1

        # Ordner erstellen, falls er noch nicht existiert
        os.makedirs(folder, exist_ok=True)
        try:
            while True:
                filename = os.path.join(folder, f"traffic_data_{index:03d}_2.xml")

                opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
                with opener.open(url) as response, open(filename, "wb") as f:
                    f.write(response.read())

                index += 1
                time.sleep(60 * 6)  # 6 Minuten warten
        except KeyboardInterrupt:
            print("\nDownloader manuell gestoppt.")

    def analysis(self) -> None:
        site_ids: list[str] = get_site_ids('downloaded_files_2')
        flow_rate: FlowRates = FlowRates('downloaded_files_2', site_ids)
        flow_rate.plot_data()

    def activate(self):
        t_sim: threading.Thread = threading.Thread(target=self.run_download)
        t_input: threading.Thread = threading.Thread(target=self.analysis, daemon=True)
        t_sim.start()
        t_input.start()
        t_sim.join() # waits until thread is finished

if __name__ == "__main__":
    download: Download = Download()
    download.activate()