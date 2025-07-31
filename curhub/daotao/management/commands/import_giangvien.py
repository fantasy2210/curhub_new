import csv
from django.core.management.base import BaseCommand
from daotao.models import GiangVien, DonViDaoTao
from datetime import datetime

class Command(BaseCommand):
    help = 'Import giảng viên từ file CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Đường dẫn đến file CSV')

    def handle(self, *args, **options):
        file_path = options['csv_file']
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Bỏ qua dòng mẫu
                if row.get('STT') == 'Mẫu':
                    continue

                # Lấy hoặc tạo đơn vị công tác
                ten_don_vi = row.get('Cơ quan công tác \n(Thành viên ngoài cơ sở)')
                don_vi = None
                if ten_don_vi:
                    # Tạo mã đơn vị từ tên đơn vị để tránh lỗi unique
                    from django.utils.text import slugify
                    ma_don_vi_slug = slugify(ten_don_vi)[:20] # Cắt ngắn slug để vừa với max_length
                    don_vi, created = DonViDaoTao.objects.get_or_create(
                        ma_don_vi=ma_don_vi_slug,
                        defaults={'ten_don_vi': ten_don_vi}
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Đã tạo mới đơn vị: {ten_don_vi}"))

                # Chuyển đổi ngày sinh
                ngay_sinh = None
                try:
                    ngay_sinh_str = row.get('Ngày sinh')
                    if ngay_sinh_str:
                        ngay_sinh = datetime.strptime(ngay_sinh_str, '%d/%m/%Y').date()
                except (ValueError, TypeError):
                    self.stdout.write(self.style.WARNING(f"Không thể chuyển đổi ngày sinh: {row.get('Ngày sinh')} cho giảng viên {row.get('Họ')} {row.get('Tên')}"))
                    pass

                giang_vien_data = {
                    'ho': row.get('Họ'),
                    'ten': row.get('Tên'),
                    'ngay_sinh': ngay_sinh,
                    'so_cccd_ho_chieu': row.get('Số CCCD/ Hộ chiếu'),
                    'quoc_tich': row.get('Quốc tịch'),
                    'gioi_tinh': row.get('Giới tính'),
                    'chuc_vu_cong_tac': row.get('Chức vụ công tác'),
                    'chuc_danh_khoa_hoc': row.get('Chức danh khoa học'),
                    'trinh_do_dao_tao': row.get('Trình độ đào tạo (Cao nhất)'),
                    'chuyen_mon_dao_tao': row.get('Chuyên môn đào tạo'),
                    'email': row.get('Email'),
                    'dien_thoai': row.get('Điện thoại'),
                    'trang_thai_lam_viec': row.get('Trạng thái làm việc', 'Đang làm việc'),
                    'co_quan_cong_tac': don_vi,
                }

                # Tạo hoặc cập nhật giảng viên
                ma_can_bo = row.get('Mã cán bộ')
                if ma_can_bo and ma_can_bo.strip():
                    giang_vien, created = GiangVien.objects.update_or_create(
                        ma_can_bo=ma_can_bo,
                        defaults=giang_vien_data
                    )
                else:
                    # Xử lý trường hợp không có mã cán bộ
                    giang_vien_data['ma_can_bo'] = None
                    # Cố gắng tìm giảng viên dựa trên thông tin khác để tránh trùng lặp
                    filter_kwargs = {
                        'ho': giang_vien_data['ho'],
                        'ten': giang_vien_data['ten'],
                    }
                    if giang_vien_data['ngay_sinh']:
                        filter_kwargs['ngay_sinh'] = giang_vien_data['ngay_sinh']
                    
                    giang_vien, created = GiangVien.objects.update_or_create(
                        **filter_kwargs,
                        defaults=giang_vien_data
                    )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Đã tạo mới giảng viên: {giang_vien.ho_ten}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Đã cập nhật giảng viên: {giang_vien.ho_ten}"))

        self.stdout.write(self.style.SUCCESS('Hoàn tất import giảng viên.'))
