import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
     self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_konstruktori_negatiivinen_tilavuus(self):
        varasto = Varasto(-1)
        self.assertAlmostEqual(varasto.tilavuus, 0.0)

    def test_konstruktori_negatiivinen_alku_saldo(self):
        varasto = Varasto(10, -5)
        self.assertAlmostEqual(varasto.saldo, 0.0)

    def test_konstruktori_alku_saldo_yli_tilavuuden(self):
        varasto = Varasto(10, 15)
        self.assertAlmostEqual(varasto.saldo, 10.0)

    def test_lisaa_varastoon_negatiivinen_maara(self):
        alkuperainen_saldo = self.varasto.saldo
        self.varasto.lisaa_varastoon(-5)
        self.assertAlmostEqual(self.varasto.saldo, alkuperainen_saldo)

    def test_lisaa_varastoon_yli_tilavuuden(self):
        self.varasto.lisaa_varastoon(15)
        self.assertAlmostEqual(self.varasto.saldo, 10.0)

    def test_ota_varastosta_negatiivinen_maara(self):
        self.varasto.lisaa_varastoon(5)
        saatu_maara = self.varasto.ota_varastosta(-3)
        self.assertAlmostEqual(saatu_maara, 0.0)
        self.assertAlmostEqual(self.varasto.saldo, 5.0)

    def test_ota_varastosta_enemman_kuin_saldoa(self):
        self.varasto.lisaa_varastoon(5)
        saatu_maara = self.varasto.ota_varastosta(8)
        self.assertAlmostEqual(saatu_maara, 5.0)
        self.assertAlmostEqual(self.varasto.saldo, 0.0)

    def test_str_metodi(self):
        self.varasto.lisaa_varastoon(3)
        expected = "saldo = 3, vielä tilaa 7"
        self.assertEqual(str(self.varasto), expected)
