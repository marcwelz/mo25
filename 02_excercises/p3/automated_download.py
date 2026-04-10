#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 03.04.2026 21:10
@author: marcwelz
@project: mo25
"""
import ssl
import time
import urllib.request
from pathlib import Path

# Config
URL: str = "https://transport.data.gouv.fr/resources/79165/download"
SAVE_DIR: Path = Path("downloaded_files")
INTERVAL_SECONDS: int = 360
TOTAL_DOWNLOADS: int = 50

ssl_context: ssl.SSLContext = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def download_file(index: int) -> None:
    SAVE_DIR.mkdir(exist_ok=True)
    filename: Path = SAVE_DIR / f"traffic_data_{index:03d}.xml"
    try:
        opener: urllib.request.OpenerDirector = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=ssl_context)
        )
        with opener.open(URL) as response, open(filename, "wb") as f:
            f.write(response.read())
        print(f"[{index:03d}] saved: {filename}")
    except Exception as e:
        print(f"[{index:03d}] error: {e}")

for i in range(1, TOTAL_DOWNLOADS + 1):
    download_file(i)
    if i < TOTAL_DOWNLOADS:
        time.sleep(INTERVAL_SECONDS)