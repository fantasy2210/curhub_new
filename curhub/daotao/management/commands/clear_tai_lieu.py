from django.core.management.base import BaseCommand
from daotao.models import TaiLieuHocTap

class Command(BaseCommand):
    help = 'Clears all records from the TaiLieuHocTap table.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Clearing all records from TaiLieuHocTap...'))
        count, _ = TaiLieuHocTap.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} records.'))
