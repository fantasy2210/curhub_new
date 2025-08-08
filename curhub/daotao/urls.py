from django.urls import path
from .views import (
    ctdt_views,
    hoc_phan_views,
    don_vi_views,
    giang_vien_views,
    api_views
)

app_name = 'daotao'

urlpatterns = [
    path('', ctdt_views.index, name='index'),
    path('nganh/them/', ctdt_views.them_nganh_dao_tao, name='them_nganh_dao_tao'),
    path('ctdt/danh-sach/', ctdt_views.danh_sach_ctdt, name='danh_sach_ctdt'),
    path('ctdt/them/', ctdt_views.them_chuong_trinh_dao_tao, name='them_ctdt'),
    path('ctdt/<int:pk_ctdt>/chi-tiet/', ctdt_views.chi_tiet_ctdt, name='chi_tiet_ctdt'),
    path('ctdt/<int:pk_ctdt>/sua/', ctdt_views.sua_ctdt, name='sua_ctdt'),
    path('ctdt/<int:pk_ctdt>/xoa/', ctdt_views.xoa_ctdt, name='xoa_ctdt'),
    path('ctdt/<int:pk_ctdt>/gui-duyet/', ctdt_views.gui_duyet_ctdt, name='gui_duyet_ctdt'),
    path('ctdt/<int:pk_ctdt>/xu-ly-duyet/', ctdt_views.xu_ly_duyet_ctdt, name='xu_ly_duyet_ctdt'),
    path('ctdt/<int:pk_ctdt>/tao-phien-ban-moi/', ctdt_views.tao_phien_ban_moi_ctdt, name='tao_phien_ban_moi_ctdt'),
    path('ctdt/doi-sanh/', ctdt_views.doi_sanh_ctdt, name='doi_sanh_ctdt'),
    path('ctdt/luu-tru/', ctdt_views.luu_tru_ctdt, name='luu_tru_ctdt'),
    path('hoc-phan/danh-sach/', hoc_phan_views.danh_sach_hoc_phan, name='danh_sach_hoc_phan'),
    path('hoc-phan/<int:pk_hoc_phan>/chi-tiet/', hoc_phan_views.chi_tiet_hoc_phan, name='chi_tiet_hoc_phan'),
    path('hoc-phan/<int:pk_hoc_phan>/sua/', hoc_phan_views.sua_hoc_phan, name='sua_hoc_phan'),
    path('hoc-phan/<int:pk_hoc_phan>/xoa/', hoc_phan_views.xoa_hoc_phan, name='xoa_hoc_phan'),
    path('hoc-phan/download-template/', hoc_phan_views.download_hoc_phan_ctdt_template, name='download_hoc_phan_ctdt_template'),
    path('ctdt/<int:pk_ctdt>/hoc-phan/them-hang-loat/', ctdt_views.them_hoc_phan_hang_loat, name='them_hoc_phan_hang_loat'),
    path('ctdt/<int:pk_ctdt>/hoc-phan/upload/', ctdt_views.upload_hoc_phan_ctdt, name='upload_hoc_phan_ctdt'),
    path('ctdt/<int:pk_ctdt>/hoc-phan/danh-sach/', ctdt_views.danh_sach_hoc_phan_theo_ctdt, name='danh_sach_hoc_phan_theo_ctdt'),
    path('ctdt/<int:pk_ctdt>/them_hoc_phan_vao_ctdt/', ctdt_views.them_hoc_phan_vao_ctdt, name='them_hoc_phan_vao_ctdt'),
    path('ctdt/hoc-phan/<int:pk_chi_tiet_hp>/chi-tiet/', ctdt_views.chi_tiet_hoc_phan_trong_ctdt, name='chi_tiet_hoc_phan_trong_ctdt'),
    path('ctdt/hoc-phan/<int:pk_chi_tiet_hp>/sua/', ctdt_views.sua_chi_tiet_hp_trong_ctdt, name='sua_chi_tiet_hp_trong_ctdt'),
    path('ctdt/hoc-phan/<int:pk_chi_tiet_hp>/sua-ctdt/', ctdt_views.sua_hoc_phan_ctdt, name='sua_hoc_phan_ctdt'),
    path('ctdt/hoc-phan/<int:pk_chi_tiet_hp>/xoa/', ctdt_views.xoa_chi_tiet_hp_trong_ctdt, name='xoa_chi_tiet_hp_trong_ctdt'),
    path('ctdt/hoc-phan/<int:pk_chi_tiet_hp>/xoa-ctdt/', ctdt_views.xoa_hoc_phan_ctdt, name='xoa_hoc_phan_ctdt'),
    path('api/ctdt/hoc-phan/update-inline/', api_views.update_chi_tiet_hoc_phan_inline, name='update_chi_tiet_hoc_phan_inline'),
    path('ctdt/muc-tieu-dao-tao/update-inline/', api_views.update_muc_tieu_dao_tao_inline, name='update_muc_tieu_dao_tao_inline'),
    path('don-vi/danh-sach/', don_vi_views.danh_sach_don_vi, name='danh_sach_don_vi'),
    path('don-vi/them/', don_vi_views.them_don_vi, name='them_don_vi'),
    path('don-vi/<int:pk>/sua/', don_vi_views.sua_don_vi, name='sua_don_vi'),
    path('don-vi/<int:pk>/xoa/', don_vi_views.xoa_don_vi, name='xoa_don_vi'),
    path('ctdt/<int:pk_ctdt>/chuan-dau-ra/them/', ctdt_views.them_chuan_dau_ra, name='them_chuan_dau_ra'),
    path('ctdt/chuan-dau-ra/<int:pk_cdr>/sua/', ctdt_views.sua_chuan_dau_ra, name='sua_chuan_dau_ra'),
    path('ctdt/chuan-dau-ra/<int:pk_cdr>/xoa/', ctdt_views.xoa_chuan_dau_ra, name='xoa_chuan_dau_ra'),
    path('ctdt/<int:pk_ctdt>/muc-tieu-dao-tao/them/', ctdt_views.them_muc_tieu_dao_tao, name='them_muc_tieu_dao_tao'),
    path('ctdt/muc-tieu-dao-tao/<int:pk_po>/xoa/', ctdt_views.xoa_muc_tieu_dao_tao, name='xoa_muc_tieu_dao_tao'),

    # URLs for modal-based CRUD for PO and PLO
    path('api/ctdt/<int:pk_ctdt>/po/them/', api_views.api_them_po, name='api_them_po'),
    path('api/po/<int:pk_po>/sua/', api_views.sua_muc_tieu_dao_tao, name='api_sua_po'),
    path('api/po/<int:pk_po>/chi-tiet/', api_views.api_get_po_details, name='api_get_po_details'),
    path('api/ctdt/<int:pk_ctdt>/plo/them/', api_views.api_them_plo, name='api_them_plo'),
    path('api/plo/<int:pk_cdr>/sua/', api_views.api_sua_plo, name='api_sua_plo'),
    path('api/plo/<int:pk_cdr>/chi-tiet/', api_views.api_get_plo_details, name='api_get_plo_details'), # New API endpoint

    path('api/nganh-dao-tao-options/', api_views.get_nganh_dao_tao_options, name='get_nganh_dao_tao_options'),
    path('api/don-vi-dao-tao-options/', api_views.get_don_vi_dao_tao_options, name='get_don_vi_dao_tao_options'),
    path('api/search-hoc-phan/', api_views.search_hoc_phan_api, name='search_hoc_phan_api'),
    path('api/ctdt/<int:pk_ctdt>/search-hoc-phan/', api_views.search_hoc_phan_in_ctdt_api, name='search_hoc_phan_in_ctdt_api'),
    path('api/hoc-phan-details/<int:pk_hoc_phan>/', api_views.get_hoc_phan_details, name='get_hoc_phan_details'),
    # Danh Muc Kien Thuc
    path('danh-muc-kien-thuc/', hoc_phan_views.danh_sach_danh_muc_kien_thuc, name='danh_sach_danh_muc_kien_thuc'),
    path('danh-muc-kien-thuc/them/', hoc_phan_views.them_danh_muc_kien_thuc, name='them_danh_muc_kien_thuc'),
    path('danh-muc-kien-thuc/<int:pk>/sua/', hoc_phan_views.sua_danh_muc_kien_thuc, name='sua_danh_muc_kien_thuc'),
    path('danh-muc-kien-thuc/<int:pk>/xoa/', hoc_phan_views.xoa_danh_muc_kien_thuc, name='xoa_danh_muc_kien_thuc'),

    # De Cuong Hoc Phan
    path('hoc-phan/<int:pk_hoc_phan>/de-cuong/', hoc_phan_views.danh_sach_de_cuong, name='danh_sach_de_cuong'),
    path('hoc-phan/<int:pk_hoc_phan>/de-cuong/them/', hoc_phan_views.them_de_cuong, name='them_de_cuong'),
    path('de-cuong/<int:pk_de_cuong>/sua/', hoc_phan_views.sua_de_cuong, name='sua_de_cuong'),
    path('de-cuong/<int:pk_de_cuong>/xoa/', hoc_phan_views.xoa_de_cuong, name='xoa_de_cuong'),
    # API for getting course details
    path('api/de-cuong-chi-tiet/<int:pk_hoc_phan>/', api_views.api_get_de_cuong_chi_tiet, name='api_get_de_cuong_chi_tiet'),
    # API for program flowchart data
    path('api/ctdt/<int:pk_ctdt>/flowchart-data/', api_views.api_program_flowchart_data, name='api_program_flowchart_data'),

    # Giảng viên
    path('giang-vien/danh-sach/', giang_vien_views.danh_sach_giang_vien, name='danh_sach_giang_vien'),
    path('ctdt/<int:pk_ctdt>/quan-ly-giang-vien/', giang_vien_views.quan_ly_giang_vien_ctdt, name='quan_ly_giang_vien_ctdt'),
    path('ctdt/<int:pk_ctdt>/cap-nhat-giang-vien/', giang_vien_views.cap_nhat_giang_vien_ctdt, name='cap_nhat_giang_vien_ctdt'),
    path('ctdt/<int:pk_ctdt>/load-giang-vien-tab/', giang_vien_views.load_giang_vien_tab, name='load_giang_vien_tab'),
    path('api/ctdt/<int:pk_ctdt>/search-giang-vien/', api_views.api_search_giang_vien_chua_tham_gia, name='api_search_giang_vien_chua_tham_gia'),
    path('api/ctdt/<int:pk_ctdt>/get-assigned-giang-vien/', api_views.api_get_giang_vien_da_tham_gia, name='api_get_giang_vien_da_tham_gia'),
    path('api/ctdt/<int:pk_ctdt>/giang-vien/<int:pk_gv>/phan-cong-form/', api_views.api_get_phan_cong_form, name='api_get_phan_cong_form'),
    path('api/ctdt/<int:pk_ctdt>/luu-phan-cong/', api_views.api_luu_phan_cong, name='api_luu_phan_cong'),

    # URL for LLM-based evaluation
    path('api/cdr/danh-gia/', api_views.danh_gia_cdr_api, name='danh_gia_cdr_api'),
    path('api/ollama-status/', api_views.get_ollama_status, name='get_ollama_status'),
]
