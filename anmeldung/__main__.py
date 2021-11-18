import pathlib
from bibliothek.scannen_von_buchern import Buch, ScannenVonBüchern


class Haupt:
    _ZIELORDNER: pathlib.Path = pathlib.Path('ausgabe/')

    def laufen() -> None:
        '''The main method.'''

        svb: ScannenVonBüchern = ScannenVonBüchern(
            zielordner=Haupt._ZIELORDNER
        )

        for kategorien_basis_url in svb.iter_aus_kategorien():
            kategoriedaten: list[Buch] = []

            for buch_url in svb.aus_den_seiten(kategorien_basis_url):
                buch: Buch = svb.buchinfo_erhalten(buch_url)
                kategoriedaten.append(buch)
                svb.bild_herunterladen(buch.bild_url)

            svb.daten_speichern(kategoriedaten)


if __name__ == '__main__':
    Haupt.laufen()
