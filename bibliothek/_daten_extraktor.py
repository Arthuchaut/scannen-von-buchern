from bs4 import BeautifulSoup


class _DatenExtraktor:
    def __init__(self, soup: BeautifulSoup) -> None:
        self._soup: BeautifulSoup = soup

    def upc_extrahieren(self) -> str:
        '''Extract the UPC info from the HTML tree.

        Returns:
            str: The UPC info. None if no data found.
        '''

        spiel: list[BeautifulSoup]

        if spiel := self._soup.select(
            'table.table.table-striped > tr:nth-of-type(1) > td'
        ):
            return spiel[0].text

    def titel_extrahieren(self) -> str:
        '''Extract the title info from the HTML tree.

        Returns:
            str: The title info. None if no data found.
        '''

        spiel: list[BeautifulSoup]

        if spiel := self._soup.select('div.product_main > h1'):
            return spiel[0].text

    def preis_inklusive_steuern_extrahieren(self) -> str:
        '''Extract the price incl taxes info from the HTML tree.

        Returns:
            str: The price incl taxes info. None if no data found.
        '''

        spiel: list[BeautifulSoup]

        if spiel := self._soup.select(
            'table.table.table-striped > tr:nth-of-type(4) > td'
        ):
            return spiel[0].text

    def preis_ohne_steuern_extrahieren(self) -> str:
        '''Extract the price excl taxes info from the HTML tree.

        Returns:
            str: The price excl taxes info. None if no data found.
        '''

        spiel: list[BeautifulSoup]

        if spiel := self._soup.select(
            'table.table.table-striped > tr:nth-of-type(3) > td'
        ):
            return spiel[0].text

    def anzahl_verfügbar_extrahieren(self) -> str:
        '''Extract the book availability info from the HTML tree.

        Returns:
            str: The book availability info. None if no data found.
        '''

        spiel: list[BeautifulSoup]

        if spiel := self._soup.select(
            'table.table.table-striped > tr:nth-of-type(6) > td'
        ):
            return spiel[0].text

    def produkt_beschreibung_extrahieren(self) -> str:
        '''Extract the book description info from the HTML tree.

        Returns:
            str: The book description info. None if no data found.
        '''

        spiel: list[BeautifulSoup]

        if spiel := self._soup.select('#content_inner > article > p'):
            return spiel[0].text

    def kategorie_extrahieren(self) -> str:
        '''Extract the book category info from the HTML tree.

        Returns:
            str: The book category info. None if no data found.
        '''

        spiel: list[BeautifulSoup]

        if spiel := self._soup.select(
            '#default > div > div > ul > li:nth-child(3) > a'
        ):
            return spiel[0].text

    def bewertung_der_rezension_extrahieren(self) -> str:
        '''Extract the book rating info from the HTML tree.

        Returns:
            str: The book rating info. None if no data found.
        '''

        spiel: list[BeautifulSoup]

        if spiel := self._soup.select('div.product_main > p.star-rating'):
            return spiel[0]['class'][-1]

    def bild_url_extrahieren(self) -> str:
        '''Extract the book image URL info from the HTML tree.

        Returns:
            str: The book image URL info. None if no data found.
        '''

        spiel: list[BeautifulSoup]

        if spiel := self._soup.select(
            '#product_gallery > div > div > div > img'
        ):
            return spiel[0]['src'][6:]
