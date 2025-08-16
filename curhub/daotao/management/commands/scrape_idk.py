import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from daotao.models import TaiLieuHocTap

class Command(BaseCommand):
    help = 'Scrapes documents from the IDK search portal.'

    START_URL = 'https://search.idk.org.vn/Search/Results?type=AllFields&lookfor=%C4%91%E1%BA%A1i%20h%E1%BB%8Dc%20tr%C3%A0%20vinh'

    def add_arguments(self, parser):
        parser.add_argument('--pages', type=int, help='The number of pages to scrape.')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting scraping...'))
        
        pages_to_scrape = options['pages']
        page = 1
        while True:
            if pages_to_scrape and page > pages_to_scrape:
                self.stdout.write(self.style.SUCCESS(f"Finished scraping {pages_to_scrape} pages."))
                break

            self.stdout.write(f"Scraping page {page}...")
            url = f"{self.START_URL}&page={page}"
            
            try:
                response = requests.get(url, timeout=30)
                if response.status_code != 200:
                    self.stderr.write(self.style.ERROR(f'Failed to fetch page {page}. Status code: {response.status_code}'))
                    break

                soup = BeautifulSoup(response.content, 'html.parser')
                results = soup.find_all('div', class_='result')

                if not results:
                    self.stdout.write(self.style.SUCCESS('No more results found.'))
                    break

                for result in results:
                    title_element = result.find('a', class_='title')
                    author_element = result.find('div', class_='author')
                    
                    if title_element:
                        nhan_de = title_element.text.strip()
                        tac_gia = author_element.text.strip() if author_element else 'N/A'
                        
                        # Check if the document already exists
                        if TaiLieuHocTap.objects.filter(nhan_de=nhan_de).exists():
                            self.stdout.write(f"Skipping existing record: {nhan_de}")
                            continue

                        # Create and save the new document
                        TaiLieuHocTap.objects.create(
                            nhan_de=nhan_de,
                            tac_gia=tac_gia,
                            loai_tai_lieu='Sach'  # Default value, can be changed
                        )
                        self.stdout.write(self.style.SUCCESS(f"Successfully saved record: {nhan_de}"))

                page += 1

            except requests.exceptions.RequestException as e:
                self.stderr.write(self.style.ERROR(f'Failed to connect to the server: {e}'))
                break

        self.stdout.write(self.style.SUCCESS('Scraping finished.'))
