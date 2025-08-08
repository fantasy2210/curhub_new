import json
import re
import ollama
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from ..models import (
    ChuongTrinhDaoTao, MucTieuDaoTao, ChuanDauRa, ChiTietHocPhanTrongCTDT,
    DanhMucKienThuc, HocPhan, DeCuongHocPhan, GiangVien, PhanCongGiangDay
)
from ..forms import MucTieuDaoTaoForm, ChuanDauRaForm

client = ollama.Client(host='http://172.250.4.30:11434')

@csrf_exempt
@require_http_methods(["GET"])
def get_ollama_status(request):
    try:
        response = client.list()
        return JsonResponse({'status': 'ok', 'details': response})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Không thể kết nối đến Ollama: {e}'}, status=503)

@csrf_exempt
@require_http_methods(["POST"])
def danh_gia_cdr_api(request):
    try:
        # Step 1: Parse the incoming request from the browser
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            error_message = f"Lỗi giải mã JSON từ request: {e}. Dữ liệu nhận được: '{request.body.decode('utf-8', errors='ignore')}'"
            return JsonResponse({'error': error_message}, status=400)

        cdr_text = data.get('cdr_text', '')
        if not cdr_text:
            return JsonResponse({'error': 'Không có văn bản CĐR nào được cung cấp.'}, status=400)

        # Step 2: Prepare and send the request to Ollama
        prompt = f"""
Bạn là một chuyên gia về đo lường và đánh giá trong giáo dục đại học, am hiểu sâu sắc về thang đo nhận thức Bloom và cách viết chuẩn đầu ra (CĐR) hiệu quả.
Một CĐR tốt ở Bậc 3 (Vận dụng) theo thang Bloom thường có cấu trúc 3 phần:
1.  **Động từ hành động (Action Verb):** Động từ mạnh, có thể quan sát, đo lường được (ví dụ: Vận dụng, Áp dụng, Giải quyết, Xây dựng...).
2.  **Đối tượng kiến thức (Knowledge Object):** Nội dung kiến thức/kỹ năng cụ thể cần sử dụng.
3.  **Bối cảnh/Mục đích (Context):** Tình huống hoặc mục tiêu áp dụng kiến thức đó.
Bây giờ, hãy đánh giá câu phát biểu chuẩn đầu ra chương trình đào tạo sau đây:
"{cdr_text}"
Hãy thực hiện các yêu cầu sau và trả lời dưới định dạng JSON:
1.  **Phân rã CĐR** trên thành 3 thành phần: "dong_tu_hanh_dong", "doi_tuong_kien_thuc", "boi_canh_muc_dich". Nếu thành phần nào không rõ hoặc thiếu, hãy ghi "Không xác định".
2.  **Đánh giá động từ** theo mức độ phù hợp với Bậc 3 (Vận dụng). Giá trị là một trong các chuỗi: "Rất phù hợp", "Phù hợp", "Không phù hợp". Gán vào trường "muc_do_phu_hop_dong_tu".
3.  **Đánh giá tính rõ ràng** của CĐR. Giá trị là một trong các chuỗi: "Rất rõ ràng", "Tương đối rõ ràng", "Chung chung, cần cải thiện". Gán vào trường "tinh_ro_rang_CDR".
4.  **Đưa ra nhận xét tổng quan** và đề xuất cải thiện (nếu có) để câu CĐR trở nên rõ ràng và hiệu quả hơn. Gán vào trường "de_xuat_cai_thien".
5.  **Viết lại CĐR đã cải thiện** (nếu cần). Gán vào trường "cdr_cai_thien". Nếu CĐR gốc đã tốt, trả về chuỗi rỗng.

Ví dụ định dạng JSON đầu ra:
{{
  "phan_tich_cau_truc": {{
    "dong_tu_hanh_dong": "Vận dụng",
    "doi_tuong_kien_thuc": "các nguyên lý marketing",
    "boi_canh_muc_dich": "để xây dựng một kế hoạch truyền thông cơ bản"
  }},
  "danh_gia": {{
    "muc_do_phu_hop_dong_tu": "Phù hợp",
    "tinh_ro_rang_CDR": "Tương đối rõ ràng"
  }},
  "de_xuat_cai_thien": "CĐR có thể rõ ràng hơn bằng cách cụ thể hóa 'kế hoạch truyền thông cơ bản'.",
  "cdr_cai_thien": "Vận dụng các nguyên lý marketing để xây dựng một kế hoạch truyền thông cơ bản cho một sản phẩm giả định."
}}

QUAN TRỌNG: Chỉ trả về đối tượng JSON hợp lệ, không có bất kỳ văn bản nào khác trước hoặc sau nó.
"""
        
        response = client.generate(
            model='llama3.1:8b',
            prompt=prompt,
            format='json',
            options={'temperature': 0.2}
        )

        # Step 3: Parse the response from Ollama
        llm_json_response_str = response.get('response', '').strip()

        if not llm_json_response_str:
            return JsonResponse({'error': 'Ollama đã trả về một phản hồi rỗng.'}, status=500)

        # Attempt to extract a valid JSON object from the string
        try:
            # Find the start and end of the JSON object
            start_index = llm_json_response_str.find('{')
            end_index = llm_json_response_str.rfind('}')
            
            if start_index != -1 and end_index != -1 and end_index > start_index:
                json_str_to_parse = llm_json_response_str[start_index:end_index+1]
                llm_json_response = json.loads(json_str_to_parse)
            else:
                # If no JSON object is found, raise an error
                raise json.JSONDecodeError("Không tìm thấy đối tượng JSON trong phản hồi.", llm_json_response_str, 0)

        except json.JSONDecodeError as e:
            error_message = f"Lỗi giải mã JSON từ Ollama: {e}. Dữ liệu nhận được: '{llm_json_response_str}'"
            return JsonResponse({'error': error_message}, status=500)

        return JsonResponse(llm_json_response)

    except ollama.ResponseError as e:
        return JsonResponse({'error': f'Lỗi từ Ollama: {e.error}'}, status=e.status_code)
    except Exception as e:
        return JsonResponse({'error': f'Lỗi không xác định: {e}'}, status=500)


@require_http_methods(["POST"])
def update_chi_tiet_hoc_phan_inline(request):
    try:
        pk = request.POST.get('pk')
        field = request.POST.get('field')
        value = request.POST.get('value')

        chi_tiet_hp = get_object_or_404(ChiTietHocPhanTrongCTDT, pk=pk)

        if chi_tiet_hp.chuong_trinh_dao_tao.trang_thai != 'DRAFT':
            return JsonResponse({'status': 'error', 'message': 'Chỉ có thể chỉnh sửa khi CTĐT ở trạng thái "Bản nháp".'}, status=403)

        allowed_fields = [
            'hoc_ky_du_kien', 'tin_chi_ly_thuyet_apdung', 'tin_chi_thuc_hanh_apdung',
            'so_gio_ly_thuyet_apdung', 'so_gio_thuc_hanh_apdung', 'la_bat_buoc', 'danh_muc_kien_thuc'
        ]

        if field not in allowed_fields:
            return JsonResponse({'status': 'error', 'message': f'Trường "{field}" không được phép chỉnh sửa.'}, status=400)

        if field == 'danh_muc_kien_thuc':
            if value:
                value = get_object_or_404(DanhMucKienThuc, pk=value)
            else:
                value = None
        elif field == 'la_bat_buoc':
            value = value.lower() in ['true', '1']
        elif value == '':
             value = None
        else:
            try:
                if 'tin_chi' in field:
                    value = float(value)
                else:
                    value = int(value)
            except (ValueError, TypeError):
                return JsonResponse({'status': 'error', 'message': 'Giá trị không hợp lệ.'}, status=400)

        setattr(chi_tiet_hp, field, value)
        chi_tiet_hp.save(update_fields=[field])

        return JsonResponse({'status': 'success', 'message': 'Cập nhật thành công!'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["POST"])
def update_muc_tieu_dao_tao_inline(request):
    pk = request.POST.get('pk')
    field = request.POST.get('field')
    value = request.POST.get('value')

    try:
        po = get_object_or_404(MucTieuDaoTao, pk=pk)
        
        allowed_fields = ['ma_muc_tieu', 'noi_dung']
        if field not in allowed_fields:
            return JsonResponse({'status': 'error', 'message': 'Trường không được phép chỉnh sửa.'})

        if po.chuong_trinh_dao_tao.trang_thai != 'DRAFT':
            return JsonResponse({'status': 'error', 'message': 'Chỉ có thể sửa khi CTĐT ở trạng thái "Bản nháp".'})

        setattr(po, field, value)
        po.save(update_fields=[field])
        
        return JsonResponse({'status': 'success', 'message': 'Cập nhật thành công!', 'new_value': value})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_http_methods(["POST"])
def api_them_po(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    if ctdt.trang_thai != 'DRAFT':
        return JsonResponse({'status': 'error', 'message': "Chỉ có thể thêm khi CTĐT ở trạng thái 'Bản nháp'."}, status=403)
    
    form = MucTieuDaoTaoForm(request.POST)
    if form.is_valid():
        po = form.save(commit=False)
        po.chuong_trinh_dao_tao = ctdt
        po.save()
        return JsonResponse({'status': 'success', 'message': 'Đã thêm Mục tiêu Đào tạo thành công!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Dữ liệu không hợp lệ.', 'errors': form.errors}, status=400)

@require_http_methods(["POST"])
def sua_muc_tieu_dao_tao(request, pk_po):
    po = get_object_or_404(MucTieuDaoTao, pk=pk_po)
    ctdt = po.chuong_trinh_dao_tao

    if ctdt.trang_thai != 'DRAFT':
        return JsonResponse({'status': 'error', 'message': "Chỉ có thể sửa khi CTĐT ở trạng thái 'Bản nháp'."}, status=403)

    form = MucTieuDaoTaoForm(request.POST, instance=po)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success', 'message': 'Đã cập nhật Mục tiêu Đào tạo thành công!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Dữ liệu không hợp lệ.', 'errors': form.errors}, status=400)

def api_get_po_details(request, pk_po):
    po = get_object_or_404(MucTieuDaoTao, pk=pk_po)
    data = {
        'pk': po.pk,
        'ma_muc_tieu': po.ma_muc_tieu,
        'noi_dung': po.noi_dung,
    }
    return JsonResponse(data)

@require_http_methods(["POST"])
def api_them_plo(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    if ctdt.trang_thai != 'DRAFT':
        return JsonResponse({'status': 'error', 'message': "Chỉ có thể thêm khi CTĐT ở trạng thái 'Bản nháp'."}, status=403)
    
    form = ChuanDauRaForm(request.POST, ctdt=ctdt)
    if form.is_valid():
        plo = form.save(commit=False)
        plo.chuong_trinh_dao_tao = ctdt
        plo.save()
        form.save_m2m()
        return JsonResponse({'status': 'success', 'message': 'Đã thêm Chuẩn Đầu ra thành công!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Dữ liệu không hợp lệ.', 'errors': form.errors}, status=400)

@require_http_methods(["POST"])
def api_sua_plo(request, pk_cdr):
    plo = get_object_or_404(ChuanDauRa, pk=pk_cdr)
    ctdt = plo.chuong_trinh_dao_tao

    if ctdt.trang_thai != 'DRAFT':
        return JsonResponse({'status': 'error', 'message': "Chỉ có thể sửa khi CTĐT ở trạng thái 'Bản nháp'."}, status=403)

    form = ChuanDauRaForm(request.POST, instance=plo, ctdt=ctdt)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success', 'message': 'Đã cập nhật Chuẩn Đầu ra thành công!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Dữ liệu không hợp lệ.', 'errors': form.errors}, status=400)

def api_get_plo_details(request, pk_cdr):
    plo = get_object_or_404(ChuanDauRa, pk=pk_cdr)
    data = {
        'pk': plo.pk,
        'ma_cdr': plo.ma_cdr,
        'noi_dung': plo.noi_dung,
        'loai_cdr': plo.loai_cdr,
        'dap_ung_muc_tieu': list(plo.dap_ung_muc_tieu.values_list('pk', flat=True))
    }
    return JsonResponse(data)

def get_nganh_dao_tao_options(request):
    return JsonResponse([], safe=False)

def get_don_vi_dao_tao_options(request):
    return JsonResponse([], safe=False)

def search_hoc_phan_api(request):
    search_term = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    ctdt_pk = request.GET.get('ctdt_pk')

    if ctdt_pk:
        try:
            ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=ctdt_pk)
            queryset = ChiTietHocPhanTrongCTDT.objects.filter(chuong_trinh_dao_tao=ctdt).order_by('hoc_phan__ma_hoc_phan')
            
            if search_term:
                queryset = queryset.filter(
                    Q(hoc_phan__ma_hoc_phan__icontains=search_term) |
                    Q(hoc_phan__ten_hoc_phan__icontains=search_term)
                )
        except ChuongTrinhDaoTao.DoesNotExist:
            return JsonResponse({'results': [], 'pagination': {'more': False}}, status=404)
    else:
        queryset = HocPhan.objects.all().order_by('ma_hoc_phan')
        if search_term:
            queryset = queryset.filter(
                Q(ma_hoc_phan__icontains=search_term) |
                Q(ten_hoc_phan__icontains=search_term)
            )

    paginator = Paginator(queryset, 30)
    try:
        hoc_phan_page = paginator.page(page)
    except PageNotAnInteger:
        hoc_phan_page = paginator.page(1)
    except EmptyPage:
        hoc_phan_page = paginator.page(paginator.num_pages)

    results = []
    for hoc_phan in hoc_phan_page:
        results.append({
            'id': hoc_phan.pk,
            'text': f"{hoc_phan.ma_hoc_phan} - {hoc_phan.ten_hoc_phan}"
        })

    return JsonResponse({
        'results': results,
        'pagination': {
            'more': hoc_phan_page.has_next()
        }
    })

def search_hoc_phan_in_ctdt_api(request, pk_ctdt):
    search_term = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    
    try:
        ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
        
        queryset = ChiTietHocPhanTrongCTDT.objects.filter(
            chuong_trinh_dao_tao=ctdt
        ).select_related('hoc_phan').order_by('hoc_phan__ma_hoc_phan')
        
        if search_term:
            queryset = queryset.filter(
                Q(hoc_phan__ma_hoc_phan__icontains=search_term) |
                Q(hoc_phan__ten_hoc_phan__icontains=search_term)
            )
            
        exclude_pk = request.GET.get('exclude_pk')
        if exclude_pk:
            queryset = queryset.exclude(pk=exclude_pk)

        paginator = Paginator(queryset, 30)
        try:
            results_page = paginator.page(page)
        except (EmptyPage, PageNotAnInteger):
            results_page = paginator.page(paginator.num_pages)

        results = [
            {
                'id': chi_tiet.pk,
                'text': f"{chi_tiet.hoc_phan.ma_hoc_phan} - {chi_tiet.hoc_phan.ten_hoc_phan}"
            }
            for chi_tiet in results_page
        ]

        return JsonResponse({
            'results': results,
            'pagination': {'more': results_page.has_next()}
        })

    except ChuongTrinhDaoTao.DoesNotExist:
        return JsonResponse({'results': [], 'pagination': {'more': False}}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_hoc_phan_details(request, pk_hoc_phan):
    try:
        hoc_phan = get_object_or_404(HocPhan, pk=pk_hoc_phan)
        data = {
            'tin_chi_ly_thuyet_apdung': hoc_phan.tin_chi_ly_thuyet_goc,
            'tin_chi_thuc_hanh_apdung': hoc_phan.tin_chi_thuc_hanh_goc,
            'so_gio_ly_thuyet_apdung': hoc_phan.so_gio_ly_thuyet_goc,
            'so_gio_thuc_hanh_apdung': hoc_phan.so_gio_thuc_hanh_goc,
            'so_gio_tu_hoc_apdung': hoc_phan.so_gio_tu_hoc_goc,
        }
        return JsonResponse(data)
    except Http404:
        return JsonResponse({'error': 'HocPhan not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def api_get_de_cuong_chi_tiet(request, pk_hoc_phan):
    de_cuong = get_object_or_404(
        DeCuongHocPhan.objects.select_related('hoc_phan', 'hoc_phan__don_vi_quan_ly_goc'), 
        hoc_phan__pk=pk_hoc_phan, 
        la_phien_ban_hien_hanh=True
    )
    
    hoc_phan = de_cuong.hoc_phan
    data = {
        'ten_hoc_phan': hoc_phan.ten_hoc_phan,
        'ma_hoc_phan': hoc_phan.ma_hoc_phan,
        'so_tin_chi': hoc_phan.tong_so_tin_chi_goc,
        'don_vi_quan_ly': hoc_phan.don_vi_quan_ly_goc.ten_don_vi if hoc_phan.don_vi_quan_ly_goc else "N/A",
        'ten_de_cuong_phien_ban': de_cuong.ten_de_cuong_phien_ban,
        'ngay_ban_hanh': de_cuong.ngay_ban_hanh.strftime('%d/%m/%Y'),
        'muc_tieu_hoc_phan': de_cuong.muc_tieu_hoc_phan,
        'tom_tat_noi_dung': de_cuong.tom_tat_noi_dung,
        'phuong_phap_day_hoc': de_cuong.phuong_phap_day_hoc,
        'nhiem_vu_sinh_vien': de_cuong.nhiem_vu_sinh_vien,
        'thang_diem_danh_gia': de_cuong.thang_diem_danh_gia,
        'tai_lieu_hoc_tap': de_cuong.tai_lieu_hoc_tap,
        'cac_yeu_cau_khac': de_cuong.cac_yeu_cau_khac,
        'chuan_dau_ra': [],
        'noi_dung_chi_tiet': [],
        'hinh_thuc_danh_gia': []
    }
    clos = de_cuong.chuan_dau_ra_cua_de_cuong.all().order_by('ma_clo')
    for clo in clos:
        data['chuan_dau_ra'].append({
            'ma_clo': clo.ma_clo,
            'noi_dung': clo.noi_dung,
            'muc_do_bloom': clo.get_muc_do_bloom_display()
        })
    noi_dungs = de_cuong.noi_dung_chi_tiet.prefetch_related('chuan_dau_ra_lien_quan').order_by('tuan_hoc_hoac_chu_de')
    for nd in noi_dungs:
        data['noi_dung_chi_tiet'].append({
            'tuan_hoc_hoac_chu_de': nd.tuan_hoc_hoac_chu_de,
            'noi_dung_giang_day': nd.noi_dung_giang_day,
            'so_gio_ly_thuyet': nd.so_gio_ly_thuyet,
            'so_gio_thuc_hanh': nd.so_gio_thuc_hanh,
            'so_gio_tu_hoc': nd.so_gio_tu_hoc,
            'chuan_dau_ra_lien_quan': [clo.ma_clo for clo in nd.chuan_dau_ra_lien_quan.all()]
        })
    danh_gias = de_cuong.hinh_thuc_danh_gia.prefetch_related('chuan_dau_ra_danh_gia').order_by('loai_danh_gia')
    for dg in danh_gias:
        data['hinh_thuc_danh_gia'].append({
            'ten_hinh_thuc': dg.ten_hinh_thuc,
            'loai_danh_gia': dg.get_loai_danh_gia_display(),
            'ty_le_diem': dg.ty_le_diem,
            'chuan_dau_ra_danh_gia': [clo.ma_clo for clo in dg.chuan_dau_ra_danh_gia.all()]
        })
    return JsonResponse(data)

def api_program_flowchart_data(request, pk_ctdt):
    def clean_mermaid_id(text):
        return re.sub(r'[^a-zA-Z0-9_]', '', text)

    try:
        ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
        details = ChiTietHocPhanTrongCTDT.objects.filter(
            chuong_trinh_dao_tao=ctdt
        ).select_related('hoc_phan', 'danh_muc_kien_thuc').prefetch_related(
            'hoc_phan_tien_quyet__hoc_phan', 'hoc_phan_song_hanh__hoc_phan'
        )

        nodes = []
        edges = []
        added_nodes = set()

        for detail in details:
            original_hp_id = detail.hoc_phan.ma_hoc_phan
            hp_mermaid_id = clean_mermaid_id(original_hp_id)
            
            if hp_mermaid_id not in added_nodes:
                nodes.append({
                    'id': hp_mermaid_id,
                    'original_id': original_hp_id,
                    'name': detail.hoc_phan.ten_hoc_phan,
                    'tin_chi': detail.tong_so_tin_chi_apdung,
                    'khoi_kien_thuc': detail.danh_muc_kien_thuc.ten_danh_muc if detail.danh_muc_kien_thuc else "Chưa phân loại"
                })
                added_nodes.add(hp_mermaid_id)

            for tien_quyet_detail in detail.hoc_phan_tien_quyet.all():
                source__id = clean_mermaid_id(tien_quyet_detail.hoc_phan.ma_hoc_phan)
                edges.append({
                    'source': source_id,
                    'target': hp_mermaid_id,
                    'type': 'tienquyet'
                })

            for song_hanh_detail in detail.hoc_phan_song_hanh.all():
                source_id = clean_mermaid_id(song_hanh_detail.hoc_phan.ma_hoc_phan)
                edges.append({
                    'source': source_id,
                    'target': hp_mermaid_id,
                    'type': 'songhanh'
                })

        return JsonResponse({'nodes': nodes, 'edges': edges})

    except ChuongTrinhDaoTao.DoesNotExist:
        return JsonResponse({'error': 'Program not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def api_search_giang_vien_chua_tham_gia(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    search_term = request.GET.get('q', '')

    # Lấy danh sách ID của giảng viên đã tham gia
    assigned_gv_ids = ctdt.giang_vien_tham_gia.values_list('id', flat=True)
    
    # Lấy danh sách giảng viên chưa tham gia
    giang_vien_list = GiangVien.objects.exclude(id__in=assigned_gv_ids)

    if search_term:
        giang_vien_list = giang_vien_list.filter(
            Q(ho_ten__icontains=search_term) | 
            Q(ma_can_bo__icontains=search_term)
        )
    
    html = render_to_string(
        'daotao/partials/_giang_vien_chua_tham_gia_list.html',
        {
            'giang_vien_chua_tham_gia': giang_vien_list,
            'ctdt': ctdt,
            'is_draft': ctdt.trang_thai == 'DRAFT',
            'perms': request.user.get_all_permissions()
        }
    )
    return JsonResponse({'html': html})


def api_get_giang_vien_da_tham_gia(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    search_term = request.GET.get('q', '')

    # Lấy danh sách giảng viên đã tham gia
    giang_vien_list = ctdt.giang_vien_tham_gia.all()

    if search_term:
        giang_vien_list = giang_vien_list.filter(
            Q(ho_ten__icontains=search_term) | 
            Q(ma_can_bo__icontains=search_term)
        )

    html = render_to_string(
        'daotao/partials/_giang_vien_da_tham_gia_list.html',
        {
            'giang_vien_da_tham_gia': giang_vien_list,
            'ctdt': ctdt,
            'is_draft': ctdt.trang_thai == 'DRAFT',
            'perms': request.user.get_all_permissions()
        }
    )
    return JsonResponse({'html': html})

def api_get_phan_cong_form(request, pk_ctdt, pk_gv):
    return JsonResponse({})

def api_luu_phan_cong(request, pk_ctdt):
    return JsonResponse({})
