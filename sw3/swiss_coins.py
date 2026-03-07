#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 06.03.2026 10:42
@author: marcwelz
@project: mo25
"""
from dataclasses import dataclass, field
from typing import override

@dataclass
class Money:
    def value(self) -> float:
        raise NotImplementedError

@dataclass
class Coin(Money):
    _value: float = 0.0
    material: str = "Metal"

    @override
    def value(self) -> float:
        return self._value

@dataclass
class BankNote(Money):
    _value: int = 0
    material: str = "Paper"

    @override
    def value(self) -> float:
        return float(self._value)

class FiveCentsCoin(Coin):
    def __init__(self): super().__init__(0.05)

class TenCentsCoin(Coin):
    def __init__(self): super().__init__(0.10)

class TwentyCentsCoin(Coin):
    def __init__(self): super().__init__(0.20)

class FiftyCentsCoin(Coin):
    def __init__(self): super().__init__(0.50)

class OneCHFCoin(Coin):
    def __init__(self): super().__init__(1.00)

class TwoCHFCoin(Coin):
    def __init__(self): super().__init__(2.00)

class FiveCHFCoin(Coin):
    def __init__(self): super().__init__(5.00)

class TenCHFNote(BankNote):
    def __init__(self): super().__init__(10)

class TwentyCHFNote(BankNote):
    def __init__(self): super().__init__(20)

class FiftyCHFNote(BankNote):
    def __init__(self): super().__init__(50)

class HundertCHFNote(BankNote):
    def __init__(self): super().__init__(100)

class TwoHundertCHFNote(BankNote):
    def __init__(self): super().__init__(200)

class ThousandCHFNote(BankNote):
    def __init__(self): super().__init__(1000)

@dataclass
class Wallet(Money):
    contents: list[Coin | BankNote] = field(default_factory=list)

    @override
    def value(self) -> float:
            return sum(item.value() for item in self.contents)

hn10 = TenCHFNote()
hn100 = HundertCHFNote()
hn50 = FiftyCHFNote()
c50 = FiftyCentsCoin()
c200 = TwentyCentsCoin()

wallet = Wallet(contents=[
    hn10, hn100,hn50, c50, c200])
print(wallet.value())