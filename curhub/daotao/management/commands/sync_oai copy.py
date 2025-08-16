import requests
import xml.etree.ElementTree as ET
import time
from django.core.management.base import BaseCommand
from daotao.models import TaiLieuHocTap
import json

# Tắt cảnh báo khi thực hiện request HTTPS không xác thực
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Hàm trợ giúp để đăng ký namespace, tránh lặp lại code
def register_namespaces(xml_content):
    """Đăng ký các namespace phổ biến để tránh lỗi khi tìm kiếm."""
    namespaces = {
        'oai': 'http://www.openarchives.org/OAI/2.0/',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }
    for prefix, uri in namespaces.items( ):
        ET.register_namespace(prefix, uri)
    return namespaces

class Command(BaseCommand):
    help = 'Synchronizes documents from an OAI-PMH repository.'

    OAI_ENDPOINT = 'https://opac.tvu.edu.vn:9090/api/oai'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from-date',
            type=str,
            help='Start date for harvesting in YYYY-MM-DD format.'
        )
        parser.add_argument(
            '--until-date',
            type=str,
            help='End date for harvesting in YYYY-MM-DD format.'
        )

    def handle(self, *args, **options ):
        self.stdout.write(self.style.SUCCESS('Starting OAI synchronization...'))
        
        from_date = options.get('from_date')
        until_date = options.get('until_date')

        if not self.identify_repository():
            self.stderr.write(self.style.ERROR('Halting synchronization due to failure in Identify request.'))
            return

        self.list_metadata_formats()
        self.list_sets()
        self.list_records(from_date=from_date, until_date=until_date)

        self.stdout.write(self.style.SUCCESS('OAI synchronization finished.'))

    def _make_request(self, params, retries=3, backoff_factor=0.5):
        """Hàm chung để thực hiện request và xử lý các lỗi cơ bản."""
        last_exception = None
        for attempt in range(retries):
            try:
                # Prepare the request to get the full URL for logging
                req = requests.Request('GET', self.OAI_ENDPOINT, params=params)
                prepared_req = req.prepare()
                self.stdout.write(f"Requesting URL (Attempt {attempt + 1}/{retries}): {prepared_req.url}")

                # Increased timeout to 300 seconds (5 minutes)
                response = requests.get(self.OAI_ENDPOINT, params=params, verify=False, timeout=300)
                response.raise_for_status()  # Ném lỗi cho các status code 4xx/5xx
                return response
            except requests.exceptions.Timeout as e:
                last_exception = e
                self.stdout.write(self.style.WARNING(f"Request timed out. Retrying in {backoff_factor * (2 ** attempt)} seconds..."))
                time.sleep(backoff_factor * (2 ** attempt))
            except requests.exceptions.HTTPError as e:
                self.stderr.write(self.style.ERROR(f'OAI endpoint returned status {e.response.status_code}: {e.response.reason}'))
                # Cố gắng phân tích nội dung lỗi nếu là JSON
                try:
                    error_content = e.response.json()
                    self.stderr.write(self.style.ERROR(f"Error Content: {error_content}"))
                except json.JSONDecodeError:
                    self.stderr.write(self.style.ERROR(f"Response Content: {e.response.text}"))
                last_exception = e
                break # Don't retry on HTTP errors like 4xx/5xx
            except requests.exceptions.RequestException as e:
                last_exception = e
                self.stdout.write(self.style.WARNING(f"Request failed: {e}. Retrying in {backoff_factor * (2 ** attempt)} seconds..."))
                time.sleep(backoff_factor * (2 ** attempt))

        if last_exception:
            self.stderr.write(self.style.ERROR(f'Failed to connect to the OAI endpoint after {retries} attempts: {last_exception}'))
        
        return None

    def identify_repository(self):
        """Gửi yêu cầu Identify và trả về True nếu thành công."""
        self.stdout.write(f"Sending Identify request to: {self.OAI_ENDPOINT}")
        response = self._make_request({'verb': 'Identify'})
        if response:
            try:
                ns = register_namespaces(response.content)
                root = ET.fromstring(response.content)
                repository_name = root.find('.//oai:repositoryName', ns)
                if repository_name is not None:
                    self.stdout.write(self.style.SUCCESS(f"Successfully connected to repository: {repository_name.text}"))
                    return True
            except ET.ParseError:
                self.stdout.write(self.style.WARNING("Could not parse the XML response from Identify request."))
        return False

    def list_metadata_formats(self):
        """Liệt kê các định dạng metadata được hỗ trợ."""
        self.stdout.write("Sending ListMetadataFormats request...")
        response = self._make_request({'verb': 'ListMetadataFormats'})
        if response:
            try:
                ns = register_namespaces(response.content)
                root = ET.fromstring(response.content)
                self.stdout.write(self.style.SUCCESS('Available metadata formats:'))
                for fmt in root.findall('.//oai:metadataFormat', ns):
                    prefix = fmt.find('oai:metadataPrefix', ns).text
                    schema = fmt.find('oai:schema', ns).text
                    self.stdout.write(f"  - Prefix: {prefix}, Schema: {schema}")
            except ET.ParseError:
                self.stdout.write(self.style.WARNING("Could not parse XML for metadata formats."))

    def list_sets(self):
        """Liệt kê các 'set' nếu được hỗ trợ."""
        self.stdout.write("Sending ListSets request...")
        response = self._make_request({'verb': 'ListSets'})
        if response:
            try:
                ns = register_namespaces(response.content)
                root = ET.fromstring(response.content)
                error = root.find('.//oai:error', ns)
                if error is not None:
                    self.stdout.write(self.style.WARNING(f"OAI-PMH info: {error.text} (code: {error.get('code')})"))
                else:
                    self.stdout.write(self.style.SUCCESS('Available sets:'))
                    for s in root.findall('.//oai:set', ns):
                        set_spec = s.find('oai:setSpec', ns).text
                        set_name = s.find('oai:setName', ns).text
                        self.stdout.write(f"  - SetSpec: {set_spec}, SetName: {set_name}")
            except ET.ParseError:
                self.stdout.write(self.style.WARNING("Could not parse XML for sets."))

    def list_records(self, from_date=None, until_date=None):
        """Lấy và lưu các bản ghi từ OAI endpoint."""
        params = {'verb': 'ListRecords', 'metadataPrefix': 'oai_dc'}
        if from_date:
            params['from'] = from_date
        if until_date:
            params['until'] = until_date
        records_processed = 0

        while True:
            self.stdout.write(f"Fetching records with params: {params}")
            response = self._make_request(params)
            if not response:
                break

            try:
                ns = register_namespaces(response.content)
                root = ET.fromstring(response.content)

                error = root.find('.//oai:error', ns)
                if error is not None:
                    self.stdout.write(self.style.WARNING(f"OAI-PMH error: {error.text} (code: {error.get('code')})"))
                    break

                records = root.findall('.//oai:record', ns)
                self.stdout.write(f"Found {len(records)} records on this page.")

                for record in records:
                    header = record.find('oai:header', ns)
                    identifier = header.find('oai:identifier', ns).text
                    
                    if TaiLieuHocTap.objects.filter(oai_identifier=identifier).exists():
                        self.stdout.write(f"Skipping existing record: {identifier}")
                        continue

                    metadata = record.find('oai:metadata', ns)
                    if metadata is not None:
                        dc_metadata = metadata.find('dc:dc', ns)
                        if dc_metadata is not None:
                            title = dc_metadata.find('dc:title', ns)
                            creators = dc_metadata.findall('dc:creator', ns)
                            
                            ten_tai_lieu = title.text if title is not None else 'No Title'
                            tac_gia = ', '.join([c.text for c in creators if c.text])

                            TaiLieuHocTap.objects.create(
                                ten_tai_lieu=ten_tai_lieu,
                                tac_gia=tac_gia,
                                oai_identifier=identifier,
                                loai_tai_lieu='Sach'
                            )
                            records_processed += 1
                            self.stdout.write(self.style.SUCCESS(f"Successfully saved record: {identifier}"))

                resumption_token = root.find('.//oai:resumptionToken', ns)
                resumption_token_element = root.find('.//oai:resumptionToken', ns)
                if resumption_token_element is not None and resumption_token_element.text:
                    # Update params with the new resumptionToken
                    params = {
                        'verb': 'ListRecords',
                        'resumptionToken': resumption_token_element.text
                    }
                    self.stdout.write(f"Found resumption token, fetching next page...")
                else:
                    # No more pages
                    self.stdout.write("No resumption token found, synchronization complete.")
                    break
            except ET.ParseError:
                self.stdout.write(self.style.WARNING("Could not parse the XML response for records."))
                break
        
        self.stdout.write(self.style.SUCCESS(f"Total new records processed: {records_processed}"))
