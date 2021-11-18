import pathlib
import csv
from bibliothek.scannen_von_buchern import Buch, ScannenVonBüchern


class Haupt:
    ZIELORDNER: pathlib.Path = pathlib.Path('ausgabe/')

    def laufen() -> None:
        '''The main method.'''

        zielordner_bild: pathlib.Path = Haupt.ZIELORDNER / 'img'
        zielordner_bild.mkdir(exist_ok=True)
        svb: ScannenVonBüchern = ScannenVonBüchern()

        for kategorien_basis_url in svb.iter_aus_kategorien():
            kategoriedaten: list[Buch] = []

            for buch_url in svb.aus_den_seiten(kategorien_basis_url):
                buch: Buch = svb.buchinfo_erhalten(buch_url)
                kategoriedaten.append(buch)
                svb.bild_herunterladen(buch.bild_url, zielordner_bild)

            Haupt.in_csv_speichern(kategoriedaten)

    def in_csv_speichern(kategoriedaten: list[Buch]) -> None:
        '''Save the books data to csv.

        Args:
            kategoriedaten (list[Buch]): The books data.
        '''

        csv_ordnerpfad: pathlib.Path = Haupt.ZIELORDNER / 'csv'
        csv_ordnerpfad.mkdir(exist_ok=True)

        if kategoriedaten:
            csv_pfad: pathlib.Path = (
                csv_ordnerpfad
                / f'{kategoriedaten[0].kategorie.lower().replace(" ", "_")}'
                f'_bücher.csv'
            )

            with csv_pfad.open('w', encoding='utf-8') as csv_datei:
                schriftsteller: csv.DictWriter = csv.DictWriter(
                    csv_datei, list(kategoriedaten[0].__dict__.keys())
                )
                schriftsteller.writeheader()
                schriftsteller.writerows(
                    [buch.__dict__ for buch in kategoriedaten]
                )


if __name__ == '__main__':
    Haupt.laufen()
