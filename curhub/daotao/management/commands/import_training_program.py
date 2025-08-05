import json
from django.core.management.base import BaseCommand, CommandError
from daotao.services import import_program_from_docx

class Command(BaseCommand):
    help = 'Imports training program from a DOCX file using LangExtract and outputs JSON.'

    def add_arguments(self, parser):
        parser.add_argument(
            'docx_file',
            type=str,
            help='Path to the DOCX file containing the training program.'
        )

    def handle(self, *args, **options):
        file_path = options['docx_file']
        try:
            self.stdout.write(self.style.SUCCESS(f"Extracting program data from {file_path}..."))
            program_data = import_program_from_docx(file_path)
            self.stdout.write(self.style.SUCCESS("Extraction result (JSON):"))
            self.stdout.write(json.dumps(program_data, ensure_ascii=False, indent=2))
        except Exception as e:
            raise CommandError(f"Failed to import training program: {e}")