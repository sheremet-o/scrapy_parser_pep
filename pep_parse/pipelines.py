import csv
import datetime as dt

from collections import defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def __init__(self):
        self.result_dir = BASE_DIR / 'results'
        self.result_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.results = defaultdict(int)

    def process_item(self, item, spider):
        self.results[item['status']] += 1
        return item

    def close_spider(self, spider):
        now = dt.datetime.now()
        now_format = now.strftime('%Y-%m-%d_%H-%M-%S')
        filename = 'status_summary_{now_format}.csv'.format(
            now_format=now_format)
        file_path = self.result_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            csv_writer = csv.writer(
                f,
                dialect=csv.unix_dialect(),
                quoting=csv.QUOTE_MINIMAL
            )
            csv_writer.writerows([
                ['Статус,Количество'],
                *self.statuses.items(),
                ['Total', sum(self.statuses.values())]
            ])
