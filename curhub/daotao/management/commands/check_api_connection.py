import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Checks the connection to the external book search API.'

    API_URL = 'http://172.16.2.92:8000/search'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Attempting to connect to API at: {self.API_URL}"))
        
        try:
            # We use a simple keyword that we know should work
            params = {'keyword': 'Zotero', 'limit': 1}
            response = requests.get(self.API_URL, params=params, timeout=10)
            
            # Check if the request was successful
            response.raise_for_status()
            
            self.stdout.write(self.style.SUCCESS("Connection successful!"))
            self.stdout.write("The API responded with status code: " + str(response.status_code))
            
            try:
                data = response.json()
                self.stdout.write("Successfully decoded JSON response.")
                self.stdout.write(f"Found {len(data)} item(s) in response.")
            except ValueError:
                self.stderr.write(self.style.ERROR("Failed to decode JSON from the response."))

        except requests.exceptions.Timeout:
            self.stderr.write(self.style.ERROR(
                "Connection timed out. The API server is not responding."
            ))
            self.stderr.write("Please ensure the service is running and that there is no firewall blocking the connection from this server.")
        except requests.exceptions.ConnectionError as e:
            self.stderr.write(self.style.ERROR(
                "Connection failed. Could not connect to the API server."
            ))
            self.stderr.write(f"Error details: {e}")
            self.stderr.write("This is likely a network issue (e.g., firewall, DNS, incorrect IP) between the server running this command and the API server.")
        except requests.exceptions.HTTPError as e:
            self.stderr.write(self.style.ERROR(
                f"The API returned an HTTP error: {e.response.status_code} {e.response.reason}"
            ))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
