#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 18.04.2026 11:56
@author: marcwelz
@project: mo25
"""

import pandas as pd
from dataclasses import dataclass

CSV_PATH: str = "verkehrsdaten.csv"

def load_traffic_data(filepath: str) -> pd.DataFrame:
    try:
        df: pd.DataFrame = pd.read_csv(filepath, parse_dates=["Datum"])
    except FileNotFoundError:
        raise Exception(f"File '{filepath}' not found. Make sure the CSV exists.")

    required_columns: list[str] = ["Datum", "Linie", "Verkehrsmittel", "Passagiere", "Verspätung_min"]
    for col in required_columns:
        assert col in df.columns, f"Required column '{col}' is missing in the CSV."

    assert not df.empty, "The loaded DataFrame is empty."
    return df

def avg_passengers_per_type(df: pd.DataFrame) -> pd.Series:
    assert "Passagiere" in df.columns, "Column 'Passagiere' not found."
    result: pd.Series = df.groupby("Verkehrsmittel")["Passagiere"].mean().round(1)
    return result

def avg_delay_per_type(df: pd.DataFrame) -> pd.Series:
    assert "Verspätung_min" in df.columns, "Column 'Verspätung_min' not found."
    result: pd.Series = df.groupby("Verkehrsmittel")["Verspätung_min"].mean().round(2)
    return result

def filter_high_delay_lines(df: pd.DataFrame, threshold_min: float = 5.0) -> pd.DataFrame:
    assert threshold_min >= 0, "Threshold must be a non-negative number."

    avg_delay_per_line: pd.Series = df.groupby("Linie")["Verspätung_min"].mean().round(2)
    high_delay_lines: pd.Series = avg_delay_per_line[avg_delay_per_line > threshold_min]

    result_df: pd.DataFrame = high_delay_lines.reset_index()
    result_df.columns = pd.Index(["Linie", "Avg_Verspaetung_min"])

    return result_df

if __name__ == "__main__":
    print("=" * 55)
    print("  P04 Task 1 – Traffic Data Analysis")
    print("=" * 55)

    df: pd.DataFrame = load_traffic_data(CSV_PATH)
    print("\n[1] Loaded data (first 5 rows):")
    print(df.head())

    print("\n[2a] Average passengers per transport type:")
    print(avg_passengers_per_type(df).to_string())

    print("\n[2b] Average delay (min) per transport type:")
    print(avg_delay_per_type(df).to_string())

    print("\n[3] Lines with average delay > 5 min:")
    high_delay: pd.DataFrame = filter_high_delay_lines(df, threshold_min=5.0)
    if high_delay.empty:
        print("  No lines exceed the threshold.")
    else:
        print(high_delay[["Linie", "Avg_Verspaetung_min"]].to_string(index=False))
