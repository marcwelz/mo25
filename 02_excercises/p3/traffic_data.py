#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 11.04.2026 10:06
@author: marcwelz
@project: mo25
"""

import matplotlib.pyplot as plt
from datetime import datetime
import xml.dom.minidom  # Modul zum Parsen und Bearbeiten von XML-Dokumenten
import os

class FlowRates:
    def __init__(self, data_dir, site_ids):

        # Namespace für Datex2-XML-Dateien (standardisiertes Format für Verkehrsdaten)
        self.ns_dx = "http://datex2.eu/schema/2/2_0"
        self.data = self.__load_traffic_data(data_dir, site_ids)

    def __load_traffic_data(self, directory_path, site_ids):
        """
        Liest mehrere XML-Dateien aus einem Verzeichnis ein und extrahiert
        Verkehrsflussdaten für bestimmte Messstellen.

        Parameters
        ----------
        directory_path : str
            Pfad zum Verzeichnis mit den XML-Dateien

        site_ids : list
            Liste der Messstellen-IDs (z.B. ["MB631.B8", "A9022010250"])


        Returns
        -------
        data : dict
            Dictionary mit Struktur:
            {
                site_id : {
                    "timestamps": [...],
                    "flow_rates": [...]
                }
            }
        """

        # Dictionary vorbereiten
        data = {}

        for site in site_ids:
            data[site] = {
                "timestamps": [],
                "flow_rates": []
            }

        # XML-Dateien im Verzeichnis finden
        files = sorted(os.listdir(directory_path))

        for file in files:

            file_path = os.path.join(directory_path, file)

            # Optional: nur XML-Dateien berücksichtigen
            if not file.endswith(".xml"):
                continue

            for site in site_ids:

                try:
                    timestamps, flow_rates = self.__extract_flow_rate_data(
                        file_path,
                        site
                    )

                    data[site]["timestamps"].extend(timestamps)
                    data[site]["flow_rates"].extend(flow_rates)

                except Exception as e:
                    print(f"Fehler beim Lesen von {file} für {site}: {e}")

        return data

    def __extract_flow_rate_data(self, file_path, measurement_site_id):
        """
        Extrahiert Verkehrsflussdaten (Fahrzeuganzahl pro Zeiteinheit) aus einer Datex2-XML-Datei
        für eine bestimmte Messstelle.

        Args:
            file_path (str): Pfad zur XML-Datei
            measurement_site_id (str): ID der Messstelle (z.B. "MB631.B8")

        Returns:
            tuple: (timestamps, flow_rates) - zwei Listen mit Zeitstempeln und zugehörigen Flussraten
        """
        # XML-Dokument parsen
        dom = xml.dom.minidom.parse(open(file_path))

        # Wurzelelement des Dokuments holen
        env = dom.documentElement

        # Listen für Ergebnisse vorbereiten
        timestamps = []
        flow_rates = []

        # Alle "siteMeasurements"-Elemente durchgehen (enthält Messdaten pro Standort)
        for sm in env.getElementsByTagNameNS(self.ns_dx, "siteMeasurements"):
            # Referenz auf die Messstelle holen
            site_ref = sm.getElementsByTagNameNS(self.ns_dx, "measurementSiteReference")[0]

            # Prüfen, ob es die gesuchte Messstelle ist
            if site_ref.getAttribute("id") == measurement_site_id:
                # Zeitstempel der Messung extrahieren
                mtd = sm.getElementsByTagNameNS(self.ns_dx, "measurementTimeDefault")[0]
                timestamp = datetime.fromisoformat(mtd.childNodes[0].nodeValue)

                # Verkehrsflussrate extrahieren
                flow = sm.getElementsByTagNameNS(self.ns_dx, "vehicleFlowRate")[0]
                flow_rate = float(flow.childNodes[0].nodeValue)

                # Daten zu den Listen hinzufügen
                timestamps.append(timestamp)
                flow_rates.append(flow_rate)

        return timestamps, flow_rates

    def plot_data(self):
        items = self.data.items()
        # Plot für jede Messstelle erstellen
        fig, axs = plt.subplots(len(items), 1, figsize=(10, 15), sharex=True)

        for i, (site_id, values) in enumerate(items):
            # Daten plotten
            axs[i].plot(values["timestamps"], values["flow_rates"], label=site_id)
            axs[i].set_title(f"Traffic Flow Rate over Time for {site_id}")
            axs[i].set_ylabel("Vehicle Flow Rate")
            axs[i].legend()
            axs[i].grid(True)

        axs[-1].set_xlabel("Time")
        plt.tight_layout()
        plt.show()

