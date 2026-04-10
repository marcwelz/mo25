#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10.04.2026 10:44
@author: marcwelz
@project: mo25
"""
import json
import time
from dataclasses import dataclass

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

# Konfiguration
API_BASE_URL:str = "https://api.frankfurter.app"
BASE_CURRENCY:str = "CHF"
CACHE_FILE: Path = Path("exchange_rate_cache.json")
CACHE_TTL_SECONDS: int = 3600  # 1 Stunde

@dataclass
class ExchangeRateCache:
    cache_file: Path
    ttl_seconds: int

    def is_valid(self) -> bool:
        if not self.cache_file.exists():
            return False
        data = self._load_raw()
        cached_at = data.get("cached_at", 0)
        age = time.time() - cached_at
        return age < self.ttl_seconds

    def load(self) -> dict:
        return self._load_raw().get("rates", {})

    def save(self, rates: dict) -> None:
        payload = {
            "cached_at": time.time(),
            "cached_date": datetime.now().isoformat(),
            "base": BASE_CURRENCY,
            "rates": rates,
        }
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"[Cache] Gespeichert: {self.cache_file}")

    def _load_raw(self) -> dict:
        with open(self.cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

@dataclass
class ExchangeRateClient:
    def __init__(self, base_currency: str = BASE_CURRENCY):
        self.base_currency = base_currency
        self.cache = ExchangeRateCache(CACHE_FILE, CACHE_TTL_SECONDS)
        self._rates_df: pd.DataFrame | None = None

    def _fetch_from_api(self) -> dict:
        """Holt frische Kursdaten von der API."""
        url = f"{API_BASE_URL}/latest"
        params = {"from": self.base_currency}
        print(f"[API] Anfrage: {url} (base={self.base_currency})")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # CHF:CHF = 1.0 manuell einfügen (API gibt Basiswährung nicht zurück)
        rates = data["rates"]
        rates[self.base_currency] = 1.0
        return rates

    def _load_rates(self) -> dict:
        if self.cache.is_valid():
            print("[Cache] Verwende gecachte Kursdaten.")
            return self.cache.load()
        rates = self._fetch_from_api()
        self.cache.save(rates)
        return rates

    def get_rates_dataframe(self) -> pd.DataFrame:
        if self._rates_df is None:
            rates_dict = self._load_rates()
            self._rates_df = pd.DataFrame(
                list(rates_dict.items()),
                columns=["currency", "rate_from_chf"]
            ).sort_values("currency").reset_index(drop=True)
        return self._rates_df

    def get_rate(self, target_currency: str) -> float:
        target_currency = target_currency.upper().strip()
        df = self.get_rates_dataframe()
        row = df[df["currency"] == target_currency]
        if row.empty:
            available = ", ".join(df["currency"].tolist())
            raise ValueError(
                f"Währung '{target_currency}' nicht gefunden. "
                f"Verfügbar: {available}"
            )
        return float(row["rate_from_chf"].iloc[0])

    def convert_to_chf(self, amount: float, from_currency: str) -> float:
        rate = self.get_rate(from_currency)
        return amount / rate

    def convert_from_chf(self, amount_chf: float, to_currency: str) -> float:
        rate = self.get_rate(to_currency)
        return amount_chf * rate

_default_client: ExchangeRateClient | None = None


def get_chf_rate(currency: str) -> float:
    global _default_client
    if _default_client is None:
        _default_client = ExchangeRateClient()
    return _default_client.get_rate(currency)

if __name__ == "__main__":
    print("=" * 55)
    print("  Frankfurter API – CHF Wechselkurs-Abfrage")
    print("=" * 55)

    client = ExchangeRateClient()

    df = client.get_rates_dataframe()
    print(f"\nVerfügbare Währungen ({len(df)} total):")
    print(df.to_string(index=False))

    print("\n--- Einzelabfragen (1 CHF = X) ---")
    test_currencies = ["EUR", "USD", "GBP", "JPY", "CAD"]
    for curr in test_currencies:
        try:
            rate = client.get_rate(curr)
            print(f"  CHF → {curr}: {rate:.4f}")
        except ValueError as e:
            print(f"  Fehler: {e}")

    print("\n--- Modul-Funktion get_chf_rate() ---")
    eur_rate = get_chf_rate("EUR")
    print(f"  get_chf_rate('EUR') = {eur_rate:.4f}")

    print("\n--- Konvertierungsbeispiele ---")
    betrag_eur = 100.0
    betrag_chf = client.convert_to_chf(betrag_eur, "EUR")
    print(f"  {betrag_eur:.2f} EUR → {betrag_chf:.2f} CHF")

    betrag_chf2 = 500.0
    betrag_usd = client.convert_from_chf(betrag_chf2, "USD")
    print(f"  {betrag_chf2:.2f} CHF → {betrag_usd:.2f} USD")

"""
    print("\n--- Fehlerbehandlung ---")
    try:
        get_chf_rate("XYZ")
    except ValueError as e:
        print(f"  Erwarteter Fehler: {e[:60]}...")
"""