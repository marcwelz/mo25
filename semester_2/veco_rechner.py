# -*- coding: utf-8 -*-
"""VECO Rechner — Verkehrsökonomie (GUI, tkinter)"""

import math
import sys
import io
import tkinter as tk
from tkinter import ttk, scrolledtext


# ── Formatierungs-Helfer ─────────────────────────────────────────────

def f(n, d=2):
    if n is None or not math.isfinite(n):
        return "-"
    s = ("{:,.%df}" % d).format(n).replace(",", "'")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def zeile(label, wert, einheit="", formel=""):
    print("  %-40s %14s %s" % (label, wert, einheit))
    if formel:
        print("  %-40s   (%s)" % ("", formel))


def titel(t):
    print("=" * 62)
    print("  " + t)
    print("=" * 62)


def abschnitt(t):
    print("\n  -- " + t + " " + "-" * max(1, 54 - len(t)))


def urteil(symbol, text):
    print("\n  [%s] %s" % (symbol, text))


# ── Berechnungsfunktionen ────────────────────────────────────────────

def calc_db(p, vk, fk, m=None):
    titel("Deckungsbeitrag & Break-even")
    db = p - vk
    zeile("Deckungsbeitrag pro Stueck", f(db), "CHF", "%s - %s" % (f(p), f(vk)))
    if p:
        zeile("DB-Marge", f(db / p * 100, 1), "%", "DB / Preis")
    if db <= 0:
        urteil("X", "DB <= 0: Preis deckt nicht mal variable Kosten. Break-even unerreichbar.")
        return
    be = fk / db
    zeile("Break-even-Menge", f(be, 1), "Stueck", "%s / %s" % (f(fk), f(db)))
    zeile("Break-even-Umsatz", f(be * p), "CHF", "BE-Menge x Preis")
    if m is not None:
        abschnitt("Bei geplanter Menge %s Stueck" % f(m, 0))
        gdb = db * m
        gewinn = gdb - fk
        zeile("Gesamt-Deckungsbeitrag", f(gdb), "CHF", "%s x %s" % (f(db), f(m, 0)))
        zeile("Gewinn / Verlust", f(gewinn), "CHF", "Gesamt-DB - Fixkosten")
        if m:
            zeile("Sicherheitsmarge", f((m - be) / m * 100, 1), "%",
                  "(Menge - BE) / Menge")
        if gewinn >= 0:
            urteil("OK", "Ueber dem Break-even: Gewinn %s CHF." % f(gewinn))
        else:
            urteil("!",  "Unter dem Break-even: es fehlen %s Stueck." % f(be - m, 0))
    print("\n  Kurzfr. Preisuntergrenze = variable Kosten")
    print("  Langfr. Preisuntergrenze = Selbstkosten (Vollkosten)")


def calc_kalk(ep, gk, gw, sk, rb):
    titel("Kalkulation: Einstand -> Verkaufspreis")
    sek = ep * (1 + gk / 100)
    netto = sek * (1 + gw / 100)
    ziel = netto / (1 - sk / 100)
    brutto = ziel / (1 - rb / 100)
    zeile("Selbstkosten", f(sek), "CHF", "%s + %s%% Gemeinkosten" % (f(ep), f(gk, 1)))
    zeile("Nettoerloes", f(netto), "CHF", "%s + %s%% Gewinn" % (f(sek), f(gw, 1)))
    zeile("Zielverkaufspreis", f(ziel), "CHF", "%s / (1 - %s%%)" % (f(netto), f(sk, 1)))
    zeile("Bruttoverkaufspreis (Katalog)", f(brutto), "CHF",
          "%s / (1 - %s%%)" % (f(ziel), f(rb, 1)))
    if ep:
        zeile("Gesamtaufschlag auf Einstand", f((brutto / ep - 1) * 100, 1), "%")
    zeile("Gewinn in Franken", f(netto - sek), "CHF")
    print("\n  Warum / statt x bei Skonto/Rabatt? Abzug wird 'im Hundert'")
    print("  vom Verkaufspreis berechnet -- klassische Pruefungsfalle.")


def calc_statisch(inv, rest, nd, gew):
    titel("Statische Investitionsrechnung")
    abschr = (inv - rest) / nd
    kap = (inv + rest) / 2
    cf = gew + abschr
    zeile("Jaehrliche Abschreibung (linear)", f(abschr), "CHF",
          "(%s - %s) / %s" % (f(inv), f(rest), f(nd, 0)))
    zeile("Durchschn. gebundenes Kapital", f(kap), "CHF",
          "(%s + %s) / 2" % (f(inv), f(rest)))
    zeile("Durchschn. Cashflow pro Jahr", f(cf), "CHF",
          "%s + %s Abschr." % (f(gew), f(abschr)))
    if kap:
        zeile("Rentabilitaet", f(gew / kap * 100, 1), "%", "Gewinn / Durchschn. Kapital")
    if cf > 0:
        amort = inv / cf
        zeile("Amortisationsdauer", f(amort), "Jahre", "%s / %s" % (f(inv), f(cf)))
        if amort <= nd:
            urteil("OK", "Amortisation (%s J.) innerhalb der Nutzungsdauer (%s J.)."
                   % (f(amort, 1), f(nd, 0)))
        else:
            urteil("X", "Amortisation (%s J.) laenger als Nutzungsdauer (%s J.)."
                   % (f(amort, 1), f(nd, 0)))
    else:
        urteil("X", "Cashflow <= 0 -- keine Amortisation moeglich.")
    print("\n  Fallen: Rentabilitaet durch DURCHSCHN. Kapital teilen;")
    print("          fuer Amortisation Abschreibungen zum Gewinn addieren.")


def calc_npv(inv, cf, nd, rest, i):
    titel("Dynamische Investitionsrechnung: Barwert & NPV")
    n = min(int(round(nd)), 50)
    rate = i / 100

    def npv_bei(r):
        s = -inv
        for t in range(1, n + 1):
            s += cf / (1 + r) ** t
        s += rest / (1 + r) ** n
        return s

    print("\n  Jahr   Rueckfluss   Abzinsfaktor       Barwert")
    print("  " + "-" * 52)
    summe = 0.0
    for t in range(1, n + 1):
        flow = cf + (rest if t == n else 0)
        fak = 1 / (1 + rate) ** t
        bw = flow * fak
        summe += bw
        extra = "  (+ Restwert)" if (t == n and rest) else ""
        print("  %4d %12s %12s %14s%s" % (t, f(flow, 0), f(fak, 4), f(bw, 0), extra))
    print("  " + "-" * 52)
    zeile("Summe Barwerte", f(summe, 0), "CHF")
    npv = summe - inv
    zeile("Net Present Value (NPV)", f(npv, 0), "CHF",
          "%s - %s Investition" % (f(summe, 0), f(inv, 0)))
    lo, hi = -0.95, 10.0
    if (npv_bei(lo) > 0) != (npv_bei(hi) > 0):
        for _ in range(100):
            mid = (lo + hi) / 2
            if (npv_bei(mid) > 0) == (npv_bei(lo) > 0):
                lo = mid
            else:
                hi = mid
        irr = (lo + hi) / 2
        zeile("Interner Zinssatz (IRR)", f(irr * 100, 2), "%", "Zinssatz, bei dem NPV = 0")
    if npv >= 0:
        urteil("OK", "NPV >= 0: Projekt schlaegt Alternativanlage zu %s%%." % f(i, 2))
    else:
        urteil("X", "NPV < 0: Alternativanlage zu %s%% waere besser." % f(i, 2))


def calc_bilanz(fm, ford, vor, av, kfk, lfk, ek):
    titel("Bilanz-Kennzahlen: Liquiditaet & Deckung")
    uv = fm + ford + vor
    akt = uv + av
    pas = kfk + lfk + ek
    zeile("Umlaufvermoegen", f(uv), "CHF", "FM + Forderungen + Vorraete")
    zeile("Bilanzsumme Aktiven / Passiven", "%s / %s" % (f(akt), f(pas)), "CHF")
    if abs(akt - pas) > 0.5:
        urteil("!", "Aktiven != Passiven (Diff. %s) -- Eingaben pruefen!" % f(akt - pas))
    abschnitt("Liquiditaet")
    if kfk:
        zeile("Liquiditaetsgrad 1 (Cash Ratio)", f(fm / kfk * 100, 1), "%",
              "FM / kFK, Faustregel >= 20-30%")
        l2 = (fm + ford) / kfk
        zeile("Liquiditaetsgrad 2 (Quick Ratio)", f(l2 * 100, 1), "%",
              "(FM + Ford.) / kFK, Faustregel >= 100%")
        zeile("Liquiditaetsgrad 3 (Current Ratio)", f(uv / kfk * 100, 1), "%",
              "UV / kFK, Faustregel >= 150-200%")
        if l2 >= 1:
            urteil("OK", "Quick Ratio >= 100%: kurzfristige Schulden gedeckt.")
        else:
            urteil("!", "Quick Ratio < 100%: ohne Vorratsverkauf nicht voll gedeckt.")
    abschnitt("Kapitalstruktur & goldene Bilanzregel")
    if pas:
        zeile("Eigenkapitalquote", f(ek / pas * 100, 1), "%",
              "EK / Gesamtkapital, Faustregel >= 30%")
    if av:
        zeile("Anlagedeckungsgrad 1", f(ek / av * 100, 1), "%", "EK / AV")
        adg2 = (ek + lfk) / av
        zeile("Anlagedeckungsgrad 2", f(adg2 * 100, 1), "%",
              "(EK + lFK) / AV, Faustregel >= 100%")
        if adg2 >= 1:
            urteil("OK", "Goldene Bilanzregel erfuellt: AV langfristig finanziert.")
        else:
            urteil("X", "Goldene Bilanzregel verletzt: Fristen-Mismatch!")


def calc_eoq(d, co, ch, pr=None):
    titel("Optimale Bestellmenge (EOQ) & Losgroesse (EBQ)")
    eoq = math.sqrt(2 * co * d / ch)
    nb = d / eoq
    zeile("Optimale Bestellmenge EOQ", f(eoq), "Stueck",
          "sqrt(2 x %s x %s / %s)" % (f(co), f(d, 0), f(ch)))
    zeile("Bestellungen pro Jahr", f(nb), "x/Jahr", "D / EOQ")
    zeile("Bestellzyklus", f(360 / nb), "Tage", "360 / Bestellungen")
    zeile("Durchschn. Lagerbestand", f(eoq / 2), "Stueck", "EOQ / 2")
    zeile("Minimale Gesamtkosten", f(math.sqrt(2 * co * d * ch)), "CHF/Jahr",
          "sqrt(2 x Co x D x Ch)")
    if pr is not None:
        if pr > d:
            ebq = math.sqrt(2 * co * d / (ch * (1 - d / pr)))
            abschnitt("Eigenproduktion")
            zeile("Optimale Losgroesse EBQ", f(ebq), "Stueck",
                  "EOQ-Logik, korr. um (1 - D/P)")
            print("\n  EBQ > EOQ: waehrend der Produktion wird schon verbraucht.")
        else:
            urteil("X", "P muss groesser sein als D, sonst nicht produzierbar.")


def calc_lager(ab, eb, jv, wert=None):
    titel("Lager-Kennzahlen")
    avg = (ab + eb) / 2
    zeile("Durchschn. Lagerbestand", f(avg, 1), "Stueck",
          "(%s + %s) / 2" % (f(ab, 0), f(eb, 0)))
    if avg:
        um = jv / avg
        zeile("Umschlagshaeufigkeit", f(um, 2), "x/Jahr",
              "%s / %s" % (f(jv, 0), f(avg, 1)))
        if um:
            zeile("Durchschn. Lagerdauer", f(360 / um, 1), "Tage", "360 / Umschlag")
    if wert is not None:
        zeile("Durchschn. gebundenes Kapital", f(avg * wert), "CHF",
              "Durchschn. Bestand x Wert/Stueck")


def calc_prod(out, inp, ert, auf, kap):
    titel("Produktivitaet, Wirtschaftlichkeit, Rentabilitaet")
    if inp:
        zeile("Produktivitaet", f(out / inp, 2), "Output/Input", "Mengen, nicht Geld!")
    if auf:
        w = ert / auf
        zeile("Wirtschaftlichkeit", f(w, 3), "", "Ertrag / Aufwand, >1 = wirtschaftlich")
    g = ert - auf
    zeile("Gewinn", f(g), "CHF", "Ertrag - Aufwand")
    if kap:
        zeile("Rentabilitaet", f(g / kap * 100, 1), "%", "Gewinn / Kapitaleinsatz")
    if auf:
        if ert / auf >= 1:
            urteil("OK", "Wirtschaftlichkeit >= 1: Ertraege uebersteigen Aufwaende.")
        else:
            urteil("X", "Wirtschaftlichkeit < 1: mehr Aufwand als Ertrag.")
    print("\n  Notizen-Falle: Aufwand/Ertrag vs. Ertrag/Aufwand --")
    print("  vor der Pruefung in den Slides verifizieren!")


# ── GUI-Basisklasse ──────────────────────────────────────────────────

_BG_NORMAL  = 'white'
_BG_VALID   = '#e8f5e9'   # light green  — valid number
_BG_INVALID = '#ffebee'   # light red    — unparseable text
_BG_MISSING = '#fff3e0'   # light orange — required field left empty

def _parse_raw(raw):
    return float(raw.replace("'", "").replace(" ", "").replace(",", "."))


class CalcTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._entries  = {}   # key -> StringVar
        self._widgets  = {}   # key -> tk.Entry
        self._optional = {}   # key -> bool
        self._build()

    def _build(self):
        left = ttk.Frame(self, padding=(14, 14, 8, 14))
        left.pack(side=tk.LEFT, fill=tk.Y, anchor=tk.N)

        ttk.Label(left, text="Eingaben", font=("TkDefaultFont", 10, "bold")).pack(
            anchor=tk.W, pady=(0, 10))

        self._add_fields(left)

        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Button(left, text="Berechnen", command=self._run_safe).pack(fill=tk.X, pady=(0, 4))
        ttk.Button(left, text="Zuruecksetzen", command=self._reset).pack(fill=tk.X)

        right = ttk.Frame(self, padding=(0, 14, 14, 14))
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._out = scrolledtext.ScrolledText(
            right, state='disabled',
            font=('Courier New', 11) if sys.platform == 'win32' else ('Menlo', 11),
            wrap=tk.NONE, relief=tk.SUNKEN, borderwidth=1,
        )
        self._out.pack(fill=tk.BOTH, expand=True)

        xbar = ttk.Scrollbar(right, orient=tk.HORIZONTAL, command=self._out.xview)
        xbar.pack(fill=tk.X)
        self._out.configure(xscrollcommand=xbar.set)

    def _field(self, parent, key, label, optional=False):
        tag = "  (optional)" if optional else ""
        ttk.Label(parent, text=label + tag).pack(anchor=tk.W)
        var = tk.StringVar()
        # tk.Entry (not ttk) so we can set background color directly
        e = tk.Entry(parent, textvariable=var, width=24,
                     bg=_BG_NORMAL, fg='black', insertbackground='black',
                     relief=tk.GROOVE, bd=2)
        e.pack(fill=tk.X, pady=(2, 8))
        e.bind('<Return>', lambda _ev: self._run_safe())
        self._entries[key]  = var
        self._widgets[key]  = e
        self._optional[key] = optional

        def _on_change(*_):
            raw = var.get().strip()
            if not raw:
                e.config(bg=_BG_NORMAL)
            else:
                try:
                    _parse_raw(raw)
                    e.config(bg=_BG_VALID)
                except ValueError:
                    e.config(bg=_BG_INVALID)

        var.trace_add('write', _on_change)

    def _get(self, key, label, optional=False):
        raw = self._entries[key].get().strip()
        if not raw:
            if optional:
                return None
            raise ValueError("Pflichtfeld leer: %s" % label)
        try:
            return _parse_raw(raw)
        except ValueError:
            raise ValueError("Keine gueltige Zahl im Feld '%s': %s" % (label, raw))

    def _reset(self):
        for key, var in self._entries.items():
            var.set("")
            self._widgets[key].config(bg=_BG_NORMAL)
        self._show("")

    def _show(self, text):
        self._out.config(state='normal')
        self._out.delete('1.0', tk.END)
        self._out.insert(tk.END, text)
        self._out.config(state='disabled')

    def _validate_all(self):
        """Highlight all fields; return True when everything is OK to calculate."""
        ok = True
        for key, var in self._entries.items():
            raw = var.get().strip()
            w = self._widgets[key]
            if not raw:
                if self._optional[key]:
                    w.config(bg=_BG_NORMAL)
                else:
                    w.config(bg=_BG_MISSING)
                    ok = False
            else:
                try:
                    _parse_raw(raw)
                    w.config(bg=_BG_VALID)
                except ValueError:
                    w.config(bg=_BG_INVALID)
                    ok = False
        return ok

    def _run_safe(self):
        if not self._validate_all():
            self._show(
                "Bitte alle Pflichtfelder korrekt ausfuellen.\n\n"
                "  Orange  = Pflichtfeld fehlt\n"
                "  Rot     = ungueltige Eingabe\n"
                "  Gruen   = Wert OK"
            )
            return
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            self._calc()
        except (ValueError, ZeroDivisionError) as e:
            sys.stdout = old
            self._show("Fehler: %s\n\nBitte Eingaben pruefen." % e)
            return
        finally:
            sys.stdout = old
        self._show(buf.getvalue())

    def _add_fields(self, parent):
        raise NotImplementedError

    def _calc(self):
        raise NotImplementedError


# ── Tab-Klassen ──────────────────────────────────────────────────────

class DbTab(CalcTab):
    def _add_fields(self, p):
        self._field(p, "preis", "Verkaufspreis / Stueck [CHF]")
        self._field(p, "vk",    "Variable Kosten / Stueck [CHF]")
        self._field(p, "fk",    "Fixkosten der Periode [CHF]")
        self._field(p, "menge", "Geplante Absatzmenge [Stueck]", optional=True)

    def _calc(self):
        calc_db(
            self._get("preis", "Verkaufspreis"),
            self._get("vk",    "Variable Kosten"),
            self._get("fk",    "Fixkosten"),
            self._get("menge", "Menge", optional=True),
        )


class KalkTab(CalcTab):
    def _add_fields(self, p):
        self._field(p, "ep", "Einstandspreis [CHF]")
        self._field(p, "gk", "Gemeinkosten-Zuschlag [%]")
        self._field(p, "gw", "Gewinn-Zuschlag [%]")
        self._field(p, "sk", "Skonto [%] (auf Zielverkaufspreis)")
        self._field(p, "rb", "Rabatt [%] (auf Bruttoverkaufspreis)")

    def _calc(self):
        calc_kalk(
            self._get("ep", "Einstandspreis"),
            self._get("gk", "Gemeinkosten-Zuschlag"),
            self._get("gw", "Gewinn-Zuschlag"),
            self._get("sk", "Skonto"),
            self._get("rb", "Rabatt"),
        )


class StatischTab(CalcTab):
    def _add_fields(self, p):
        self._field(p, "inv",  "Investitionsbetrag [CHF]")
        self._field(p, "rest", "Restwert am Ende [CHF]")
        self._field(p, "nd",   "Nutzungsdauer [Jahre]")
        self._field(p, "gew",  "Durchschn. Jahresgewinn nach Abschr. [CHF]")

    def _calc(self):
        calc_statisch(
            self._get("inv",  "Investition"),
            self._get("rest", "Restwert"),
            self._get("nd",   "Nutzungsdauer"),
            self._get("gew",  "Jahresgewinn"),
        )


class NpvTab(CalcTab):
    def _add_fields(self, p):
        self._field(p, "inv",  "Investition heute, t=0 [CHF]")
        self._field(p, "cf",   "Jaehrl. Rueckfluss / Cashflow [CHF]")
        self._field(p, "nd",   "Laufzeit [Jahre, max. 50]")
        self._field(p, "rest", "Restwert am Ende [CHF]", optional=True)
        self._field(p, "i",    "Kalkulationszinssatz [%]")

    def _calc(self):
        calc_npv(
            self._get("inv",  "Investition"),
            self._get("cf",   "Cashflow"),
            self._get("nd",   "Laufzeit"),
            self._get("rest", "Restwert", optional=True) or 0.0,
            self._get("i",    "Zinssatz"),
        )


class BilanzTab(CalcTab):
    def _add_fields(self, p):
        self._field(p, "fm",   "Fluessige Mittel (Kasse, Bank) [CHF]")
        self._field(p, "ford", "Forderungen aus L&L [CHF]")
        self._field(p, "vor",  "Vorraete [CHF]")
        self._field(p, "av",   "Anlagevermoegen [CHF]")
        self._field(p, "kfk",  "Kurzfristiges Fremdkapital [CHF]")
        self._field(p, "lfk",  "Langfristiges Fremdkapital [CHF]")
        self._field(p, "ek",   "Eigenkapital [CHF]")

    def _calc(self):
        calc_bilanz(
            self._get("fm",   "Fluessige Mittel"),
            self._get("ford", "Forderungen"),
            self._get("vor",  "Vorraete"),
            self._get("av",   "Anlagevermoegen"),
            self._get("kfk",  "Kurzfr. Fremdkapital"),
            self._get("lfk",  "Langfr. Fremdkapital"),
            self._get("ek",   "Eigenkapital"),
        )


class EoqTab(CalcTab):
    def _add_fields(self, p):
        self._field(p, "d",  "Jahresbedarf D [Stueck/Jahr]")
        self._field(p, "co", "Bestellkosten Co / Bestellung [CHF]")
        self._field(p, "ch", "Lagerkosten Ch / Stueck & Jahr [CHF]")
        self._field(p, "pr", "Produktionsrate P [Stueck/Jahr] (nur EBQ)", optional=True)

    def _calc(self):
        calc_eoq(
            self._get("d",  "Jahresbedarf"),
            self._get("co", "Bestellkosten"),
            self._get("ch", "Lagerkosten"),
            self._get("pr", "Produktionsrate", optional=True),
        )


class LagerTab(CalcTab):
    def _add_fields(self, p):
        self._field(p, "ab",   "Anfangsbestand [Stueck]")
        self._field(p, "eb",   "Endbestand [Stueck]")
        self._field(p, "jv",   "Jahresverbrauch [Stueck]")
        self._field(p, "wert", "Wert pro Stueck [CHF]", optional=True)

    def _calc(self):
        calc_lager(
            self._get("ab",   "Anfangsbestand"),
            self._get("eb",   "Endbestand"),
            self._get("jv",   "Jahresverbrauch"),
            self._get("wert", "Wert/Stueck", optional=True),
        )


class ProdTab(CalcTab):
    def _add_fields(self, p):
        self._field(p, "out", "Output [Einheiten]")
        self._field(p, "inp", "Input [Einheiten, z.B. Stunden]")
        self._field(p, "ert", "Ertrag [CHF]")
        self._field(p, "auf", "Aufwand [CHF]")
        self._field(p, "kap", "Kapitaleinsatz [CHF]")

    def _calc(self):
        calc_prod(
            self._get("out", "Output"),
            self._get("inp", "Input"),
            self._get("ert", "Ertrag"),
            self._get("auf", "Aufwand"),
            self._get("kap", "Kapital"),
        )


# ── Hauptfenster ─────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    root.title("VECO Rechner - Verkehrsoekonomie")
    root.geometry("960x640")
    root.minsize(720, 480)

    style = ttk.Style()
    style.configure("TNotebook.Tab", padding=[10, 4])

    nb = ttk.Notebook(root)
    nb.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    tabs = [
        ("DB & Break-even",   DbTab),
        ("Kalkulation",       KalkTab),
        ("Invest. statisch",  StatischTab),
        ("Invest. NPV",       NpvTab),
        ("Bilanz",            BilanzTab),
        ("EOQ / EBQ",         EoqTab),
        ("Lager",             LagerTab),
        ("Produktivitaet",    ProdTab),
    ]

    for label, cls in tabs:
        tab = cls(nb)
        nb.add(tab, text=label)

    root.mainloop()


if __name__ == "__main__":
    main()
