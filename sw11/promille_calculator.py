#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 09.05.2026 10:08
@author: marcwelz
@project: mo25
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class Drink:
    name: str
    alkohol_prozent: float   # z.B. 5.0 für Bier
    menge_ml: float          # Menge in ml
    uhrzeit: datetime        # Zeitpunkt des Konsums


@dataclass
class Person:
    alter: int
    gewicht_kg: float
    geschlecht: str          # "m" oder "w"
    drinks: list[Drink] = field(default_factory=list)

    # Widmark-Faktor: 0.7 für Männer, 0.6 für Frauen
    @property
    def widmark_faktor(self) -> float:
        return 0.7 if self.geschlecht.lower() == "m" else 0.6

    # Alkohol-Abbaurate: ~0.15‰/h, bei Jugendlichen etwas langsamer
    @property
    def abbaurate(self) -> float:
        if self.alter < 18:
            return 0.10
        return 0.15


def berechne_alkohol_gramm(drink: Drink) -> float:
    """Gramm reinen Alkohols in einem Drink (Dichte Ethanol ≈ 0.789 g/ml)"""
    return drink.menge_ml * (drink.alkohol_prozent / 100) * 0.789


def berechne_promille_zum_zeitpunkt(person: Person, zeitpunkt: datetime) -> float:
    """Aktuellen Blutalkohol in ‰ zum gegebenen Zeitpunkt berechnen (Widmark-Formel)."""
    gesamt_promille = 0.0

    for drink in person.drinks:
        if drink.uhrzeit > zeitpunkt:
            continue  # Drink liegt in der Zukunft
        gramm = berechne_alkohol_gramm(drink)
        peak_promille = gramm / (person.gewicht_kg * person.widmark_faktor)
        stunden_seit_drink = (zeitpunkt - drink.uhrzeit).total_seconds() / 3600
        # Resorptionszeit ca. 30 Min berücksichtigen
        resorption_h = 0.5
        if stunden_seit_drink < resorption_h:
            faktor = stunden_seit_drink / resorption_h
            aktuell = peak_promille * faktor
        else:
            abbau = person.abbaurate * (stunden_seit_drink - resorption_h)
            aktuell = max(0.0, peak_promille - abbau)
        gesamt_promille += aktuell

    return gesamt_promille


def berechne_nuechtern_zeitpunkt(person: Person, grenzwert: float = 0.5) -> datetime | None:
    """Zeitpunkt berechnen, ab dem der Promillewert unter den Grenzwert fällt."""
    if not person.drinks:
        return None

    jetzt = datetime.now()
    letzter_drink = max(d.uhrzeit for d in person.drinks)
    # Suche ab dem letzten Drink (auch wenn dieser in der Zukunft liegt)
    zeitpunkt = max(jetzt, letzter_drink)

    for _ in range(24 * 60):
        zeitpunkt += timedelta(minutes=1)
        promille = berechne_promille_zum_zeitpunkt(person, zeitpunkt)
        if promille <= grenzwert:
            return zeitpunkt

    return None


def berechne_max_drinks(person: Person, alkohol_prozent: float, menge_ml: float,
                        grenzwert: float = 0.5) -> float:
    """Maximale Anzahl Drinks berechnen, um unter dem Grenzwert zu bleiben."""
    for anzahl in range(1, 50):
        test_person = Person(
            alter=person.alter,
            gewicht_kg=person.gewicht_kg,
            geschlecht=person.geschlecht,
            drinks=[
                Drink(
                    name="Test",
                    alkohol_prozent=alkohol_prozent,
                    menge_ml=menge_ml,
                    uhrzeit=datetime.now()
                )
                for _ in range(anzahl)
            ]
        )
        peak = berechne_promille_zum_zeitpunkt(test_person, datetime.now() + timedelta(minutes=30))
        if peak > grenzwert:
            return anzahl - 1
    return 0


def ausgabe_bericht(person: Person, grenzwert: float = 0.5):
    jetzt = datetime.now()
    aktuell = berechne_promille_zum_zeitpunkt(person, jetzt)
    nuechtern = berechne_nuechtern_zeitpunkt(person, grenzwert)

    print("=" * 55)
    print("          PROMILLE-RECHNER – BERICHT")
    print("=" * 55)
    print(f"  Person:       {person.alter} Jahre, {person.gewicht_kg} kg, "
          f"{'männlich' if person.geschlecht == 'm' else 'weiblich'}")
    print(f"  Widmark-Faktor: {person.widmark_faktor}  |  Abbau: {person.abbaurate} ‰/h")
    print(f"  Aktuelle Zeit:  {jetzt.strftime('%H:%M Uhr')}")
    print("-" * 55)
    print(f"  Getränke:")
    for d in person.drinks:
        gramm = berechne_alkohol_gramm(d)
        print(f"    • {d.name}: {d.menge_ml} ml @ {d.alkohol_prozent}% "
              f"({gramm:.1f}g Alk.) – {d.uhrzeit.strftime('%H:%M')}")
    print("-" * 55)
    letzter_drink = max(d.uhrzeit for d in person.drinks) if person.drinks else None
    peak = berechne_promille_zum_zeitpunkt(person, letzter_drink + timedelta(minutes=30)) if letzter_drink else 0.0

    print(f"  Aktueller Blutalkohol: {aktuell:.2f} ‰")
    if aktuell > grenzwert:
        print(f"  *** FAHREN VERBOTEN (>{grenzwert} ‰) ***")
        if nuechtern:
            diff_min = int((nuechtern - jetzt).total_seconds() // 60)
            print(f"  Fahren wieder erlaubt ab: {nuechtern.strftime('%H:%M Uhr')} ({diff_min} Min)")
    elif peak > grenzwert and nuechtern:
        print(f"  Aktuell: Fahren erlaubt (unter {grenzwert} ‰)")
        diff_min = int((nuechtern - jetzt).total_seconds() // 60)
        print(f"  Nach Konsum: Fahren wieder erlaubt ab {nuechtern.strftime('%H:%M Uhr')} ({diff_min} Min)")
    else:
        print(f"  Fahren erlaubt (unter {grenzwert} ‰)")
        if person.drinks:
            print(f"  (Peak-Promille {peak:.2f} ‰ – Grenzwert {grenzwert} ‰ wird nie erreicht)")
    print("=" * 55)


# ---------------------------------------------------------------------------
# Beispiel-Nutzung
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    heute = datetime.now()

    # Person definieren
    person = Person(
        alter=22,
        gewicht_kg=94,
        geschlecht="m",
        drinks=[
            Drink("Bier 0.5L",    alkohol_prozent=5.0,  menge_ml=500, uhrzeit=heute.replace(hour=20, minute=0, second=0, microsecond=0)),
            Drink("Bier 0.5L",    alkohol_prozent=5.0,  menge_ml=500, uhrzeit=heute.replace(hour=21, minute=0, second=0, microsecond=0)),
        ]
    )

    ausgabe_bericht(person)

    # Wie viele 0.5L Bier darf man noch trinken und unter 0.5‰ bleiben?
    max_bier = berechne_max_drinks(person, alkohol_prozent=5.0, menge_ml=500, grenzwert=0.5)
    print(f"\n  Max. weitere 0.5L Bier (5%) unter 0.5‰: {max_bier}")
