#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import importlib.util
import os

_spec = importlib.util.spec_from_file_location(
    "passwort_checker",
    os.path.join(os.path.dirname(__file__), "passwort_checker.py"),
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
is_save_password = _mod.is_save_password


class TestIsSavePassword(unittest.TestCase):

    def test_zu_kurz_gibt_false(self):
        self.assertFalse(is_save_password("Ab1"))

    def test_kein_grossbuchstabe_gibt_false(self):
        self.assertFalse(is_save_password("abcdefg1"))

    def test_keine_zahl_gibt_false(self):
        self.assertFalse(is_save_password("Abcdefgh"))

    def test_gueltiges_passwort_gibt_true(self):
        self.assertTrue(is_save_password("Sicher12"))

    def test_genau_8_zeichen_mit_allen_anforderungen(self):
        self.assertTrue(is_save_password("Passwor1"))

    def test_mit_leerzeichen(self):
        self.assertFalse(is_save_password("Passwo r1"))

if __name__ == "__main__":
    unittest.main()