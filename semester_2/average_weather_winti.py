#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02.06.2026 13:34
@author: marcwelz
@project: mo25
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date

WINTERTHUR_LAT = 47.4994
WINTERTHUR_LON = 8.7274


def fetch_weather_data(start_date: str, end_date: str) -> pd.DataFrame:
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": WINTERTHUR_LAT,
        "longitude": WINTERTHUR_LON,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "precipitation_sum",
            "windspeed_10m_max",
        ],
        "timezone": "Europe/Zurich",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data["daily"])
    df["time"] = pd.to_datetime(df["time"])
    return df


def plot_weather(df: pd.DataFrame):
    fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
    fig.suptitle("Weather in Winterthur, Switzerland – Last 5 Years", fontsize=16, fontweight="bold")

    ax1 = axes[0]
    ax1.fill_between(
        df["time"], df["temperature_2m_min"], df["temperature_2m_max"],
        alpha=0.3, color="tomato", label="Min–Max range"
    )
    ax1.plot(df["time"], df["temperature_2m_mean"], color="tomato", linewidth=0.7, label="Mean temp")
    ax1.set_ylabel("Temperature (°C)")
    ax1.legend(loc="upper right", fontsize=8)
    ax1.grid(True, alpha=0.3)

    ax2 = axes[1]
    ax2.bar(df["time"], df["precipitation_sum"], color="steelblue", width=1.0, alpha=0.7, label="Precipitation")
    ax2.set_ylabel("Precipitation (mm)")
    ax2.legend(loc="upper right", fontsize=8)
    ax2.grid(True, alpha=0.3, axis="y")

    ax3 = axes[2]
    ax3.plot(df["time"], df["windspeed_10m_max"], color="seagreen", linewidth=0.7, label="Max wind speed")
    ax3.set_ylabel("Wind Speed (km/h)")
    ax3.legend(loc="upper right", fontsize=8)
    ax3.grid(True, alpha=0.3)

    ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    output_path = "semester_2/winterthur_weather_5years.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Chart saved to {output_path}")


if __name__ == "__main__":
    today = date.today()
    end_date = today.strftime("%Y-%m-%d")
    start_date = date(today.year - 5, today.month, today.day).strftime("%Y-%m-%d")

    print(f"Fetching weather data for Winterthur from {start_date} to {end_date}...")
    df = fetch_weather_data(start_date, end_date)
    print(f"Loaded {len(df)} daily records.")
    plot_weather(df)
