import requests
import json
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Searches for documents using the custom book search API.'

    # The API endpoint confirmed by the user.
    API_BASE_URL = 'http://172.16.2.92:8000'

    def add_arguments(self, parser):
        parser.add_argument(
            'keyword',
            type=str,
            help='The keyword to search for.'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Maximum number of results to return.'
        )
        parser.add_argument(
            '--skip',
            type=int,
            default=0,
            help='Number of results to skip for pagination.'
        )

    def handle(self, *args, **options):
        keyword = options['keyword']
        limit = options['limit']
        skip = options['skip']

        self.stdout.write(self.style.SUCCESS(f"Searching for keyword: '{keyword}' with limit={limit}, skip={skip}"))

        params = {
            "keyword": keyword,
            "skip": skip,
            "limit": limit,
        }

        try:
            search_url = f"{self.API_BASE_URL}/search"
            self.stdout.write(f"Requesting URL: {search_url} with params: {params}")
            
            # Set a timeout for the request
            response = requests.get(search_url, params=params, timeout=20)
            
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()
            
            results = response.json()

            if not results:
                self.stdout.write(self.style.WARNING("No results found."))
                return

            self.stdout.write(self.style.SUCCESS(f"Found {len(results)} results:"))
            
            # Pretty print the JSON results
            for i, doc in enumerate(results, 1):
                self.stdout.write(f"\n--- Result {i} ---")
                self.stdout.write(f"  Nhan đề: {doc.get('nhan_de', 'N/A')}")
                self.stdout.write(f"  Tác giả: {doc.get('tac_gia', 'N/A')}")
                self.stdout.write(f"  Năm XB: {doc.get('nam_xuat_ban', 'N/A')}")
                self.stdout.write(f"  Link: {doc.get('duong_dan', 'N/A')}")

        except requests.exceptions.Timeout:
            self.stderr.write(self.style.ERROR(
                f"The request to the search API timed out. "
                f"Please check if the service at {self.API_BASE_URL} is responsive."
            ))
        except requests.exceptions.ConnectionError:
            self.stderr.write(self.style.ERROR(
                f"Could not connect to the search API at {self.API_BASE_URL}. "
                f"Please ensure the service is running and the address is correct."
            ))
        except requests.exceptions.HTTPError as e:
            self.stderr.write(self.style.ERROR(
                f"The API returned an HTTP error: {e.response.status_code} {e.response.reason}"
            ))
            try:
                # Try to print the error content from the API
                self.stderr.write(f"Error details: {e.response.text}")
            except:
                pass
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("Failed to decode the JSON response from the API."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
