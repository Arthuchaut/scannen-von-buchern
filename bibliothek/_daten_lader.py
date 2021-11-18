import pathlib
import csv


class _DatenLader:
    def in_csv_speichern(
        self, bücherset: list[object], csv_pfad: pathlib.Path
    ) -> None:
        '''Save a list of books to a csv file.

        Args:
            bücherset (list[Buch]): The books list.
            csv_pfad (pathlib.Path): The csv file path.
        '''

        if bücherset:
            with csv_pfad.open('w', encoding='utf-8') as csv_datei:
                schriftsteller: csv.DictWriter = csv.DictWriter(
                    csv_datei, list(bücherset[0].__dict__.keys())
                )
                schriftsteller.writeheader()
                schriftsteller.writerows([buch.__dict__ for buch in bücherset])
