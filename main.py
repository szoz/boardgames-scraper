from requests_html import HTMLSession, HTML, Element
import boto3
from typing import List
from json import dump, dumps
from datetime import date

FILE_NAME = f'results_top_{date.today().isoformat()}.json'


class Game:
    """Boardgame object."""
    list_view_selector = 'tr#row_'

    def __init__(self, container: Element) -> None:
        """Populate object attributes based on given HTML element."""
        self.id = container.find('a.primary', first=True).absolute_links.pop().split('/')[4]
        self.rank = int(container.find('td.collection_rank', first=True).text)
        self.geek_rating = container.find('td.collection_bggrating')[0].text
        self.avg_rating = container.find('td.collection_bggrating')[1].text

    def export(self) -> dict:
        """Return dict with objects attribute values."""
        return self.__dict__

    @classmethod
    def many_from_document(cls, document: HTML) -> List['Game']:
        """Create many objects based on given HTML document."""
        return [cls(element) for element
                in document.find(cls.list_view_selector)]


def scrape_data(max_page: int = 10) -> List[dict]:
    """Collect data from website and return it in serialised form."""
    session = HTMLSession()
    games = []
    for page in range(1, max_page + 1):
        response = session.get(f'https://boardgamegeek.com/browse/boardgame/page/{page}')
        games.extend(Game.many_from_document(response.html))

    return [game.export() for game in games]


def dump_data(payload: List[dict]) -> None:
    """Save given payload into JSON file."""
    with open(FILE_NAME, 'w') as f:
        dump(payload, f, indent=4, ensure_ascii=False)


def dump_data_s3(payload: List[dict]) -> None:
    """Save given payload into AWS S3 bucket."""
    payload_dump = dumps(payload, indent=4, ensure_ascii=False).encode("utf-8")

    bucket_name = "bg-scraper-bucket"
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).put_object(Key=FILE_NAME, Body=payload_dump)


def main() -> None:
    """Main function for local execution."""
    results = scrape_data()
    dump_data(results)


def lambda_handler(event: dict, context: 'LambdaContext') -> None:
    """Main lambda function."""
    results = scrape_data()
    dump_data_s3(results)


if __name__ == '__main__':
    main()
