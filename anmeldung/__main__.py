import pathlib
import time
from bibliothek.scannen_von_buchern import Buch, ScannenVonBüchern


class Haupt:
    _ZIELORDNER: pathlib.Path = pathlib.Path('ausgabe/')

    def laufen() -> None:
        '''The main method.'''

        t0: float = time.time()
        svb: ScannenVonBüchern = ScannenVonBüchern(
            zielordner=Haupt._ZIELORDNER
        )

        for kategorien_basis_url in svb.iter_aus_kategorien():
            bücherset: list[Buch] = []

            for buch_url in svb.aus_den_seiten(kategorien_basis_url):
                buch: Buch = svb.buchinfo_erhalten(buch_url)
                bücherset.append(buch)
                svb.bild_herunterladen(buch.bild_url)
                print(f'Extracted {buch_url.split("/")[-2]} book')

            svb.daten_speichern(bücherset)
            print(f'Saved {kategorien_basis_url.split("/")[-2]} category')

        print(f'{time.time() - t0:.2f}s')


if __name__ == '__main__':
    Haupt.laufen()
