import csv
from django.core.management.base import BaseCommand
from daotao.models import HocPhan

class Command(BaseCommand):
    help = 'Export list of courses with credits and theory hours to courses_export.csv'

    def handle(self, *args, **options):
        output_file = 'courses_export.csv'
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Header: course_code, course_name, credits, theory_hours
            writer.writerow(['course_code', 'course_name', 'credits', 'theory_hours'])
            for course in HocPhan.objects.all():
                writer.writerow([
                    course.ma_hoc_phan,
                    course.ten_hoc_phan,
                    course.tong_so_tin_chi_goc,
                    course.so_gio_ly_thuyet_goc
                ])
        self.stdout.write(self.style.SUCCESS(f'Courses exported to {output_file}'))