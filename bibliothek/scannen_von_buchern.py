from dataclasses import dataclass
from typing import Any, Iterator
import pathlib
from bs4 import BeautifulSoup
import requests


@dataclass
class Buch:
    url_der_produktseite: str
    upc: str
    titel: str
    preis_inklusive_steuern: float
    preis_ohne_steuern: float
    anzahl_verfügbar: int
    produkt_beschreibung: str
    kategorie: str
    bewertung_der_rezension: float
    bild_url: str


class ScannenVonBüchern:
    _BASISURL: str = 'https://books.toscrape.com/'

    def _erhalten(self, url: str) -> requests.Response:
        '''Request an URL and returns the response.

        Args:
            url (str): The URL to request.


        Returns:
            requests.Response: The response if it's status code
                is 200, else None.
        '''

        antwort: requests.Response = requests.get(url)

        try:
            antwort.raise_for_status()
        except requests.HTTPError:
            return None

        return antwort

    def _html_parsen(self, antwort: requests.Response) -> BeautifulSoup:
        '''Parse the body of an HTTP response to a readable format.

        Args:
            antwort (requests.Response): The response to parse.

        Raises:
            ParsingFehler: If the body content is corrumpted.

        Returns:
            BeautifulSoup: The parsed HTML body.
        '''

        try:
            soup: BeautifulSoup = BeautifulSoup(antwort.text, 'html.parser')
        except Exception as e:
            raise ParsingFehler(e)

        return soup

    def _seitenbaum_holen(self, url: str) -> BeautifulSoup:
        '''Request the URL and return the parsed response.

        Args:
            url (str): The URL to request.

        Returns:
            BeautifulSoup: The parsed body response.
        '''

        antwort: requests.Response

        if antwort := self._erhalten(url):
            return self._html_parsen(antwort)

        return None

    def iter_aus_kategorien(self) -> Iterator[str]:
        '''Get all categories URL.

        Returns:
            Iterator[str]: An iterator of categories URLs.
        '''

        soup: BeautifulSoup = self._seitenbaum_holen(
            url='https://books.toscrape.com/index.html'
        )
        kategorien_urls: list[dict[str, Any]] = soup.select(
            'ul > li a[href^="catalogue/category/books/"]'
        )

        for a in kategorien_urls:
            yield self._BASISURL + a['href'][:-10]

    def aus_den_seiten(self, kategorien_basis_url: str) -> Iterator[str]:
        '''Get all books URL from the given category.

        Args:
            kategorien_basis_url (str): The category base url.

        Returns:
            Iterator[str]: The books URL.
        '''

        seitenzähler: int = 1

        while True:
            erstellte_url: str = (
                kategorien_basis_url
                + self._name_der_ressource_abrufen(seitenzähler)
            )
            soup: BeautifulSoup = self._seitenbaum_holen(erstellte_url)

            if not soup:
                break

            buch_urls: list[dict[str, Any]] = soup.select(
                'ol > li > article > div > a'
            )

            for a in buch_urls:
                yield self._BASISURL + 'catalogue/' + a['href'][9:]

            seitenzähler += 1

    def buchinfo_erhalten(self, buch_url: str) -> Buch:
        '''Get the book info from the given URL.

        Args:
            buch_url (str): The book URL.

        Returns:
            Buch: The book dataclass.
        '''

        soup: BeautifulSoup = self._seitenbaum_holen(buch_url)
        upc: str
        titel: str
        preis_inklusive_steuern: float
        preis_ohne_steuern: float
        anzahl_verfügbar: int
        produkt_beschreibung: str
        kategorie: str
        bewertung_der_rezension: float
        bild_url: str

        if spiel := soup.select(
            'table.table.table-striped > tr:nth-of-type(1) > td'
        ):
            upc = spiel[0].text

        if spiel := soup.select('div.product_main > h1'):
            titel = spiel[0].text

        if spiel := soup.select(
            'table.table.table-striped > tr:nth-of-type(4) > td'
        ):
            preis_inklusive_steuern = spiel[0].text

        if spiel := soup.select(
            'table.table.table-striped > tr:nth-of-type(3) > td'
        ):
            preis_ohne_steuern = spiel[0].text

        if spiel := soup.select(
            'table.table.table-striped > tr:nth-of-type(6) > td'
        ):
            anzahl_verfügbar = spiel[0].text

        if spiel := soup.select('#content_inner > article > p'):
            produkt_beschreibung = spiel[0].text

        if spiel := soup.select(
            '#default > div > div > ul > li:nth-child(3) > a'
        ):
            kategorie = spiel[0].text

        if spiel := soup.select('div.product_main > p.star-rating'):
            bewertung_der_rezension = self._bewertung_erhalten(
                spiel[0]['class'][-1]
            )

        if spiel := soup.select('#product_gallery > div > div > div > img'):
            bild_url = self._BASISURL + spiel[0]['src'][6:]

        buch: Buch = Buch(
            url_der_produktseite=buch_url,
            upc=upc,
            titel=titel,
            preis_inklusive_steuern=preis_inklusive_steuern,
            preis_ohne_steuern=preis_ohne_steuern,
            anzahl_verfügbar=anzahl_verfügbar,
            produkt_beschreibung=produkt_beschreibung,
            kategorie=kategorie,
            bewertung_der_rezension=bewertung_der_rezension,
            bild_url=bild_url,
        )

        return buch

    def bild_herunterladen(
        self, bild_url: str, zielordner: pathlib.Path
    ) -> None:
        '''Download and save the image from thea
        given URL.

        Args:
            bild_url (str): The image URL.
            zielordner (pathlib.Path): The path to save the file.
        '''

        antwort: requests.Response = self._erhalten(bild_url)
        dateipfad: pathlib.Path = zielordner / bild_url.split('/')[-1]
        dateipfad.write_bytes(antwort.content)

    def _name_der_ressource_abrufen(self, seitenzahl: int) -> str:
        if seitenzahl == 1:
            return 'index.html'
        else:
            return f'page-{seitenzahl}.html'

    def _bewertung_erhalten(self, litterale_bewertung: str) -> int:
        '''Return the integer equivalant of the given litteral rating.

        Args:
            litterale_bewertung (str): The litteral rating.

        Returns:
            int: The integer equivalant.
        '''

        kartierung: dict[str, int] = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5,
        }

        return kartierung[litterale_bewertung]


class ParsingFehler(Exception):
    ...
