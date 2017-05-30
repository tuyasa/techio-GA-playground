# coding: utf-8
import unittest
from unittest.mock import patch
from ddt import ddt, data, unpack
import os

import sys
from io import StringIO
from contextlib import contextmanager

@contextmanager
def capture(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = out
        
def test_is_chromosome(cls, chrom, size):
    cls.assertIsInstance(chrom, bytearray, "le chromosome n'a pas le bon type")
    cls.assertEqual(len(chrom), size, "le chromosome n'a pas la bonne taille")
            
_ = lambda x: bytearray(x,"ascii")

@ddt
class SelectionTest(unittest.TestCase):
    
    def test_selection(self):
        os.environ["SECRET_KEY"] = "blop"
        
        blob = [_("truc"), _("plop"), _("caca"), _("chei"), _("tric"), _("fuck")]
        
        import selection
        import secret
        
        select = selection.selection(blob)
        for x in select:
            self.assertIn(x, blob, "création de nouveaux chromosomes interdite")
        
        self.assertTrue(len(select) >= 2, "pas assez de chromosomes selectionnés")
        self.assertTrue(len(select) < len(blob), "trop de chromosomes selectionnés")
        self.assertTrue(secret.get_mean_rang(select) >= secret.get_mean_rang(blob), "la selection n'est pas assez bonne")
        
@ddt
class CroisementTest(unittest.TestCase):
    @data((_("abcd"), _("efgh")),(_("abcde"), _("fghij")))
    @unpack
    def test_croisement(self, chrom1, chrom2):
        import croisement
        chrom3 = croisement.croisement(chrom1, chrom2)
        
        test_is_chromosome(self, chrom3, len(chrom1)):
        
        from1 = 0
        from2 = 0
        for x, a, b in zip(chrom3, chrom1, chrom2):
            self.assertTrue(x == a or x == b, "création de nouveaux gènes interdite")
            if x == a:
                from1 += 1
            if x == b:
                from2 += 1
        self.assertTrue(from1 + from2 >= len(chrom3), "création de nouveaux gènes interdite")
        self.assertNotEqual(chrom1, chrom3, "le chromosome est identique à l'un des parents")
        self.assertNotEqual(chrom2, chrom3, "le chromosome est identique à l'un des parents")
        
@ddt
class MutationTest(unittest.TestCase):
    @data(_("jkdjsfo"), _("jinailnfoe"))
    def test_mutation(self, chrom2):
    
        import copy
        import mutation
        
        chrom1 = copy.copy(chrom2)
        mutation.mutation(chrom2)
        
        test_is_chromosome(self, chrom2, len(chrom1)):
        
        score = 0
        for a, b in zip(chrom1, chrom2):
            if a != b:
                score += 1
                
        self.assertFalse(score > 1, "trop de mutations effectuées")
        self.assertFalse(score == 0, "le chromosome n'a pas subi de mutations")
        