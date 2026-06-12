#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 12.06.2026 12:26
@author: marcwelz
@project: mo25
"""

import urllib.request
import urllib.error

port = 32701
gefunden = {}

for name in ("landsteiner", "linnaeus", "winogradsky"):
    treffer = []
    for param in range(1001):
        url = f"http://160.85.252.87:{port}/algo/{name}/{param}"
        try:
            resp = urllib.request.urlopen(url, timeout=5)
            body = resp.read()
            if resp.status == 200:          # erfolgreicher Aufruf
                treffer.append((param, body))
        except urllib.error.HTTPError:
            pass                            # 4xx/5xx -> falscher Parameter
        except urllib.error.URLError:
            pass                            # Netzwerkproblem
    gefunden[name] = treffer
    print(name, "->", [p for p, _ in treffer])