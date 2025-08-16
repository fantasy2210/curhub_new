import requests
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fetches and displays a single record from the OAI-PMH repository for inspection.'

    OAI_ENDPOINT = 'https://opac.tvu.edu.vn:9090/api/oai'
    METADATA_PREFIX = 'oai_dc'

    def add_arguments(self, parser):
        parser.add_argument('record_id', type=str, help='The identifier of the record to fetch.')

    def handle(self, *args, **options):
        record_id = options['record_id']
        self.stdout.write(self.style.SUCCESS(f'Fetching record with identifier: {record_id}'))

        params = {
            'verb': 'GetRecord',
            'metadataPrefix': self.METADATA_PREFIX,
            'identifier': record_id,
        }

        try:
            response = requests.get(self.OAI_ENDPOINT, params=params)
            response.raise_for_status()
            
            # Pretty print the XML
            xml_content = response.content
            root = ET.fromstring(xml_content)
            ET.indent(root)
            pretty_xml = ET.tostring(root, encoding='unicode')

            self.stdout.write(pretty_xml)

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'HTTP request failed: {e}'))
        except ET.ParseError as e:
            self.stderr.write(self.style.ERROR(f'XML parsing failed: {e}'))
