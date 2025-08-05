from django.db import transaction
from .models import (
    ChuongTrinhDaoTao, MucTieuDaoTao, 
    ChuanDauRa, ChiTietHocPhanTrongCTDT,
    HocPhan
)
import pandas as pd

# Business logic functions will be defined here
def clone_chuong_trinh_dao_tao(original_ctdt_pk: int) -> ChuongTrinhDaoTao:
    """
    Tạo một phiên bản mới (clone) từ một CTĐT đã có.
    """
    pass

def process_uploaded_courses_file(file, ctdt) -> (int, int, list):
    """
    Xử lý file upload học phần và thêm vào CTĐT.
    Trả về: (success_count, error_count, errors_list)
    """
    pass
