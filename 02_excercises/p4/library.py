#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 18.04.2026 10:59
@author: marcwelz
@project: mo25
"""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

# CONFIG

LOAN_DAYS_BOOKS: int = 28 #days
LOAN_DAYS_DVD: int = 7 #days
LOAN_DAYS_MAGAZINE: int = 14 #days

BIB_CONFIG: dict = {
    "library_name": "City Library",
    "members": [
        {"name": "Alice", "member_id": 101},
        {"name": "Bob", "member_id": 102},
        {"name": "Charlie", "member_id": 103},
    ],
    "media": [
        {"type": "Book", "title": "Clean Code", "media_id": 1},
        {"type": "Book", "title": "The Pragmatic Programmer", "media_id": 2},
        {"type": "Book", "title": "Design Patterns", "media_id": 3},
        {"type": "DVD", "title": "Inception", "media_id": 4},
        {"type": "DVD", "title": "Interstellar", "media_id": 5},
        {"type": "Magazine", "title": "Tech Monthly", "media_id": 6},
        {"type": "Magazine", "title": "Science Weekly", "media_id": 7},
    ],
}

@dataclass
class Media:
    title: str
    media_id: int
    is_borrowed: bool = False
    due_date: Optional[date] = None
    borrower_id: Optional[int] = None
    loan_days: int = 0

    def get_status(self) -> str:
        if not self.is_borrowed:
            return f"'{self.title}' [{type(self).__name__}] – available"
        return (
            f"'{self.title}' [{type(self).__name__}] – borrowed until {self.due_date} "
            f"(member ID {self.borrower_id})"
        )

    def borrow(self, member_id: int, borrow_date: Optional[date] = None) -> None:
        if borrow_date is None:
            borrow_date = date.today()
        assert not self.is_borrowed, f"'{self.title}' is already borrowed."
        self.is_borrowed = True
        self.borrower_id = member_id
        self.due_date = borrow_date + timedelta(days=self.loan_days)

    def return_item(self) -> None:
        assert self.is_borrowed, f"'{self.title}' is not currently borrowed."
        self.is_borrowed = False
        self.due_date = None
        self.borrower_id = None

    def days_overdue(self, check_date: Optional[date] = None) -> int:
        if check_date is None:
            check_date = date.today()
        if not self.is_borrowed or self.due_date is None:
            return 0
        delta: int = (check_date - self.due_date).days
        return max(delta, 0)

@dataclass
class Book(Media):
    def __post_init__(self) -> None:
        self.loan_days = LOAN_DAYS_BOOKS


@dataclass
class DVD(Media):
    def __post_init__(self) -> None:
        self.loan_days = LOAN_DAYS_DVD


@dataclass
class Magazine(Media):
    extendable: bool = False

    def __post_init__(self) -> None:
        self.loan_days = LOAN_DAYS_MAGAZINE
        self.extendable = False

@dataclass
class Member:
    name: str
    member_id: int
    borrowed_media_ids: list[int] = field(default_factory=list)
    _max_borrow: int = field(default=3, init=False, repr=False)

    def can_borrow(self) -> bool:
        return len(self.borrowed_media_ids) < self._max_borrow

    def add_borrowed(self, media_id: int) -> None:
        if not self.can_borrow():
            raise Exception(
                f"Member '{self.name}' already has {self._max_borrow} items borrowed. "
                f"Return one before borrowing another."
            )
        self.borrowed_media_ids.append(media_id)

    def remove_borrowed(self, media_id: int) -> None:
        assert media_id in self.borrowed_media_ids, (
            f"Media ID {media_id} is not in '{self.name}'s borrowed list."
        )
        self.borrowed_media_ids.remove(media_id)

    def info(self) -> str:
        return (
            f"Member '{self.name}' (ID {self.member_id}) – "
            f"borrowed: {len(self.borrowed_media_ids)}/{self._max_borrow} items"
        )

@dataclass
class Library:
    name: str
    media_catalog: list[Media] = field(default_factory=list)
    members: list[Member] = field(default_factory=list)

    def _find_media(self, media_id: int) -> Media:
        for item in self.media_catalog:
            if item.media_id == media_id:
                return item
        raise Exception(f"No media found with ID {media_id}.")

    def _find_member(self, member_id: int) -> Member:
        for member in self.members:
            if member.member_id == member_id:
                return member
        raise Exception(f"No member found with ID {member_id}.")

    def add_media(self, media: Media) -> None:
        existing_ids: list[int] = [m.media_id for m in self.media_catalog]
        assert media.media_id not in existing_ids, (
            f"Media with ID {media.media_id} already exists in catalog."
        )
        self.media_catalog.append(media)
        print(f"  [+] Added: '{media.title}' ({type(media).__name__}, ID {media.media_id})")

    def get_media_status(self, media_id: int) -> None:
        media: Media = self._find_media(media_id)
        print(f"  Status: {media.get_status()}")

    def search_by_title(self, search_term: str) -> list[Media]:
        results: list[Media] = [
            m for m in self.media_catalog
            if search_term.lower() in m.title.lower()
        ]
        if not results:
            print(f"  No results for '{search_term}'.")
        return results

    def register_member(self, member: Member) -> None:
        existing_ids: list[int] = [m.member_id for m in self.members]
        assert member.member_id not in existing_ids, (
            f"Member with ID {member.member_id} is already registered."
        )
        self.members.append(member)
        print(f"  [+] Registered: '{member.name}' (ID {member.member_id})")

    def borrow_media(
            self,
            member_id: int,
            media_id: int,
            borrow_date: Optional[date] = None,
    ) -> None:
        if borrow_date is None:
            borrow_date = date.today()
        member: Member = self._find_member(member_id)
        media: Media = self._find_media(media_id)
        # add_borrowed raises Exception when limit is reached
        member.add_borrowed(media_id)
        media.borrow(member_id, borrow_date)
        print(
            f"  [{member.name}] borrowed '{media.title}' "
            f"({type(media).__name__}) – due {media.due_date}"
        )

    def return_media(self, member_id: int, media_id: int) -> None:
        member: Member = self._find_member(member_id)
        media: Media = self._find_media(media_id)
        media.return_item()
        member.remove_borrowed(media_id)
        print(f"  [{member.name}] returned '{media.title}'")

    def check_reminders(self, check_date: Optional[date] = None) -> None:
        if check_date is None:
            check_date = date.today()
        print(f"\n  === Reminder check ({check_date}) ===")
        reminder_sent: bool = False
        for media in self.media_catalog:
            overdue_days: int = media.days_overdue(check_date)
            if overdue_days > 5:
                member: Member = self._find_member(media.borrower_id)
                print(
                    f"  ⚠  REMINDER → '{media.title}' is {overdue_days} days overdue. "
                    f"Member: {member.name} (ID {member.member_id}), due was {media.due_date}"
                )
                reminder_sent = True
        if not reminder_sent:
            print("  No reminders needed.")


def init_library(config: dict) -> "Library":
    lib: Library = Library(name=config["library_name"])

    print(f"\n  Create '{lib.name}'...")
    for m in config["members"]:
        lib.register_member(Member(name=m["name"], member_id=m["member_id"]))

    for item in config["media"]:
        media_class: type = MEDIA_TYPE_MAP[item["type"].lower()]
        lib.add_media(media_class(title=item["title"], media_id=item["media_id"]))

    return lib


MEDIA_TYPE_MAP: dict[str, type] = {
    "book": Book,
    "dvd": DVD,
    "magazine": Magazine,
}

if __name__ == "__main__":
    lib: Library = init_library(BIB_CONFIG)

    print("\n[1] Borrowing media:")
    lib.borrow_media(101, 1)
    lib.borrow_media(101, 4)
    lib.borrow_media(101, 6)

    print("\n[2] Alice attempts to borrow a 4th item:")
    try:
        lib.borrow_media(101, 2)
    except Exception as e:
        print(f"  ✗  Error caught: {e}")

    print("\n[3] Bob borrows:")
    lib.borrow_media(102, 2)
    lib.borrow_media(102, 5)

    print("\n[4] Media status check:")
    for m in lib.media_catalog:
        lib.get_media_status(m.media_id)

    print("\n[5] Returning media:")
    lib.return_media(101, 4)
    lib.get_media_status(4)

    print("\n[6] Duplicate registration tests:")
    try:
        lib.add_media(Book(title="Duplicate Book", media_id=1))
    except AssertionError as e:
        print(f"  ✗  AssertionError: {e}")

    try:
        lib.register_member(Member(name="Alice Again", member_id=101))
    except AssertionError as e:
        print(f"  ✗  AssertionError: {e}")

    print("\n[7] Simulating overdue items:")
    lib.borrow_media(
        member_id=103,
        media_id=3,
        borrow_date=date(2025, 1, 1),
    )
    lib.check_reminders(check_date=date.today())

    print("\n[8] Search for 'code':")
    results: list[Media] = lib.search_by_title("code")
    for r in results:
        print(f"  Found: {r.title} ({type(r).__name__})")
