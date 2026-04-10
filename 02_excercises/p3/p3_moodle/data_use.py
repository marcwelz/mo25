#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10.04.2026 10:54
@author: marcwelz
@project: mo25
"""

import pandas as pd
from dataclasses import dataclass, field
from datetime import datetime
from OnlineData import get_chf_rate

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

MAX_YOUTH_AGE: int = 25

BANK_NAME: str = "Clientis Spar- und Leihkasse"

ACCOUNTS: list[dict] = [
    {"type": "BankAccount", "owner": "Anna Müller", "account_id": "CH-001", "currency": "CHF"},
    {"type": "BankAccount", "owner": "John Smith", "account_id": "CH-002", "currency": "USD"},
    {"type": "SavingsAccount", "owner": "Maria Rossi", "account_id": "CH-003", "currency": "EUR",
     "interest_rate": 0.02},
    {"type": "YouthAccount", "owner": "Tom Meier", "account_id": "CH-004", "currency": "GBP", "owner_age": 19},
]

TRANSACTIONS: list[dict] = [
    {"account_id": "CH-001", "type": "deposit", "amount": 5000.00, "description": "Lohneingang"},
    {"account_id": "CH-001", "type": "withdraw", "amount": 1200.00, "description": "Miete"},
    {"account_id": "CH-002", "type": "deposit", "amount": 3000.00, "description": "Salary"},
    {"account_id": "CH-002", "type": "withdraw", "amount": 500.00, "description": "Shopping"},
    {"account_id": "CH-003", "type": "deposit", "amount": 8000.00, "description": "Stipendio"},
    {"account_id": "CH-003", "type": "apply_interest"},
    {"account_id": "CH-004", "type": "deposit", "amount": 800.00, "description": "Taschengeld"},
    {"account_id": "CH-004", "type": "withdraw", "amount": 150.00, "description": "Einkauf"},
]

# ---------------------------------------------------------------------------
# dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Transaction:
    amount: float
    currency: str
    description: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

@dataclass
class BankAccount:
    owner: str
    account_id: str
    currency: str = "CHF"
    balance: float = 0.0
    transactions: list[Transaction] = field(default_factory=list)

    def deposit(self, amount: float, description: str = "Einzahlung") -> None:
        if amount <= 0:
            raise ValueError("Einzahlungsbetrag muss positiv sein.")
        self.balance += amount
        self.transactions.append(Transaction(amount, self.currency, description))

    def withdraw(self, amount: float, description: str = "Abhebung") -> None:
        if amount <= 0:
            raise ValueError("Abhebungsbetrag muss positiv sein.")
        if amount > self.balance:
            raise ValueError(f"Ungenügend Guthaben: {self.balance:.2f} {self.currency}")
        self.balance -= amount
        self.transactions.append(Transaction(-amount, self.currency, description))

    def get_transactions_df(self) -> pd.DataFrame:
        if not self.transactions:
            return pd.DataFrame(columns=["timestamp", "description", "amount", "currency"])
        return pd.DataFrame([
            {
                "timestamp":   t.timestamp,
                "description": t.description,
                "amount":      t.amount,
                "currency":    t.currency,
            }
            for t in self.transactions
        ])

    def account_type(self) -> str:
        return "Konto"

    def __str__(self) -> str:
        return (f"[{self.account_type()}] {self.account_id} | "
                f"Inhaber: {self.owner} | "
                f"Saldo: {self.balance:.2f} {self.currency}")

@dataclass
class SavingsAccount(BankAccount):
    interest_rate: float = 0.015

    def apply_interest(self) -> None:
        interest: float = round(self.balance * self.interest_rate, 2)
        self.deposit(interest, description=f"Zinsgutschrift ({self.interest_rate*100:.2f}%)")
        print(f"  Zinsen gutgeschrieben: +{interest:.2f} {self.currency}")

    def account_type(self) -> str:
        return "Sparkonto"


@dataclass
class YouthAccount(BankAccount):
    owner_age: int = 0

    def __post_init__(self) -> None:
        if self.owner_age > MAX_YOUTH_AGE:
            raise ValueError(
                f"Jugendkonto nur bis {MAX_YOUTH_AGE} Jahre. "
                f"Alter angegeben: {self.owner_age}"
            )

    def account_type(self) -> str:
        return "Jugendkonto"


class BankApplication:
    def __init__(self, bank_name: str = "Clientis Spar- und Leihkasse AG") -> None:
        self.bank_name: str = bank_name
        self._accounts: dict[str, BankAccount] = {}

    def open_account(self, account: BankAccount) -> None:
        if account.account_id in self._accounts:
            raise ValueError(f"Konto-ID '{account.account_id}' bereits vorhanden.")
        self._accounts[account.account_id] = account
        print(f"  Konto eröffnet: {account}")

    def get_account(self, account_id: str) -> BankAccount:
        if account_id not in self._accounts:
            raise KeyError(f"Konto '{account_id}' nicht gefunden.")
        return self._accounts[account_id]

    def list_accounts(self) -> pd.DataFrame:
        """Gibt alle Konten als DataFrame zurück."""
        rows: list[dict] = [
            {
                "Konto-ID":  acc.account_id,
                "Typ":       acc.account_type(),
                "Inhaber":   acc.owner,
                "Saldo":     acc.balance,
                "Währung":   acc.currency,
            }
            for acc in self._accounts.values()
        ]
        return pd.DataFrame(rows)

    @property
    def accounts(self) -> list[BankAccount]:
        return list(self._accounts.values())


class TaxReport:
    def __init__(self, app: BankApplication) -> None:
        self.app: BankApplication = app
        self.report_date: str = datetime.now().strftime("%Y-%m-%d")

    def _to_chf(self, amount: float, currency: str) -> float:
        if currency == "CHF":
            return amount
        rate: float = get_chf_rate(currency)
        chf_amount: float = amount / rate
        print(f"    Konvertierung: {amount:.2f} {currency} ÷ {rate:.4f} "
              f"(1 CHF = {rate:.4f} {currency}) = {chf_amount:.2f} CHF")
        return chf_amount

    def generate(self) -> pd.DataFrame:
        print(f"\n{'='*60}")
        print(f"  STEUERBERICHT – {self.app.bank_name}")
        print(f"  Datum: {self.report_date} | Alle Beträge in CHF")
        print(f"{'='*60}")

        rows: list[dict] = []

        for acc in self.app.accounts:
            print(f"\n  Konto {acc.account_id} ({acc.owner}) [{acc.account_type()}]")

            balance_chf: float = self._to_chf(acc.balance, acc.currency)

            df_tx: pd.DataFrame = acc.get_transactions_df()
            total_in_chf: float = 0.0
            total_out_chf: float = 0.0

            if not df_tx.empty:
                einzahlungen: float = df_tx[df_tx["amount"] > 0]["amount"].sum()
                abhebungen: float   = df_tx[df_tx["amount"] < 0]["amount"].sum()
                total_in_chf  = self._to_chf(einzahlungen, acc.currency)
                total_out_chf = self._to_chf(abs(abhebungen), acc.currency)

            rows.append({
                "Konto-ID":        acc.account_id,
                "Inhaber":         acc.owner,
                "Typ":             acc.account_type(),
                "Orig. Währung":   acc.currency,
                "Saldo (orig.)":   round(acc.balance, 2),
                "Saldo (CHF)":     round(balance_chf, 2),
                "Einzahlungen CHF": round(total_in_chf, 2),
                "Abhebungen CHF":  round(total_out_chf, 2),
            })

        report_df: pd.DataFrame = pd.DataFrame(rows)

        print(f"\n{'='*60}")
        print("  ZUSAMMENFASSUNG")
        print(f"{'='*60}")
        print(report_df.to_string(index=False))
        total_chf: float = report_df["Saldo (CHF)"].sum()
        print(f"\n  Gesamtvermögen: {total_chf:.2f} CHF")
        print(f"{'='*60}\n")

        return report_df


if __name__ == "__main__":
    print("=" * 60)
    print(f"  {BANK_NAME}")
    print("=" * 60)

    app: BankApplication = BankApplication(BANK_NAME)

    print("\n[1] Konten eröffnen")
    _account_constructors: dict[str, type] = {
        "BankAccount": BankAccount,
        "SavingsAccount": SavingsAccount,
        "YouthAccount": YouthAccount,
    }
    for cfg in ACCOUNTS:
        cfg_copy: dict = {k: v for k, v in cfg.items() if k != "type"}
        account_class: type = _account_constructors[cfg["type"]]
        app.open_account(account_class(**cfg_copy))

    print("\n[2] Transaktionen")
    for tx in TRANSACTIONS:
        acc: BankAccount = app.get_account(tx["account_id"])
        match tx["type"]:
            case "deposit":
                acc.deposit(tx["amount"], tx.get("description", "Einzahlung"))
            case "withdraw":
                acc.withdraw(tx["amount"], tx.get("description", "Abhebung"))
            case "apply_interest":
                acc.apply_interest()  # type: ignore[attr-defined]

    print("\n[3] Kontoübersicht")
    print(app.list_accounts().to_string(index=False))

    print("\n[4] Transaktionsdetail Konto CH-002 (USD)")
    print(app.get_account("CH-002").get_transactions_df().to_string(index=False))

    print("\n[5] Steuerbericht generieren (alle Beträge → CHF)")
    report: TaxReport = TaxReport(app)
    report.generate()