import requests
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
import json
from ..suggestion_service import get_ai_suggestions, generate_syllabus_suggestions, evaluate_cdr_with_llm
from ..models import (
    NganhDaoTao, ChuongTrinhDaoTao, HocPhan, ChiTietHocPhanTrongCTDT,
    DonViDaoTao, MucTieuDaoTao, ChuanDauRa, DanhMucKienThuc, DeCuongHocPhan, ChuanDauRaHocPhan, NoiDungChiTietDeCuong, HinhThucDanhGia,
    GiangVien, PhanCongGiangDay, TaiLieuHocTap, DeCuongTaiLieu
)
from ..forms import (
    NganhDaoTaoForm, ChuongTrinhDaoTaoModelForm, HocPhanLibModelForm,
    ChiTietHocPhanTrongCTDTModelForm, DonViDaoTaoForm, MucTieuDaoTaoFormSet,
    ChuanDauRaFormSet, UploadHocPhanCTDTForm, ChuanDauRaForm, MucTieuDaoTaoForm,
    DanhMucKienThucForm, DeCuongHocPhanForm, ChuanDauRaHocPhanFormSet,
    NoiDungChiTietDeCuongFormSet, HinhThucDanhGiaFormSet, DoiSanhCTDTForm
)
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import re

@login_required
@require_POST
def get_suggestions_api(request):
    """
    API view to get AI-powered suggestions for the syllabus.
    """
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        course_name = data.get('course_name', '')
        course_description = data.get('course_description', '')
        clo_category = data.get('clo_category', '')

        if not prompt and not course_name:
            return JsonResponse({'error': 'Prompt or course name is required.'}, status=400)

        # If specific parameters are provided, use the specialized function
        if course_name and clo_category:
            suggestions = generate_syllabus_suggestions(course_name, course_description, clo_category)
        else:
            # Fall back to the general prompt-based function
            suggestions = get_ai_suggestions(prompt)
        
        return JsonResponse({'suggestions': suggestions})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
@permission_required('daotao.change_chitiethocphantrongctdt', raise_exception=True)
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

        # Type conversion and validation
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
            # For numeric fields
            try:
                # Handle potential float values for credits
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
        
        # Security check: only allow updating specific fields
        allowed_fields = ['ma_muc_tieu', 'noi_dung']
        if field not in allowed_fields:
            return JsonResponse({'status': 'error', 'message': 'Trường không được phép chỉnh sửa.'})

        # Check if CTDT is in DRAFT status
        if po.chuong_trinh_dao_tao.trang_thai != 'DRAFT':
            return JsonResponse({'status': 'error', 'message': 'Chỉ có thể sửa khi CTĐT ở trạng thái "Bản nháp".'})

        setattr(po, field, value)
        po.save(update_fields=[field])
        
        return JsonResponse({'status': 'success', 'message': 'Cập nhật thành công!', 'new_value': value})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
        
@require_http_methods(["POST"])
@permission_required('daotao.add_muctieudaotao', raise_exception=True)
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

def api_get_po_details(request, pk_po):
    """
    API endpoint to get details of a specific MucTieuDaoTao (PO) as JSON.
    """
    po = get_object_or_404(MucTieuDaoTao, pk=pk_po)
    data = {
        'pk': po.pk,
        'ma_muc_tieu': po.ma_muc_tieu,
        'noi_dung': po.noi_dung,
    }
    return JsonResponse(data)

@require_http_methods(["POST"])
@permission_required('daotao.add_chuandaura', raise_exception=True)
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

def api_get_plo_details(request, pk_cdr):
    """
    API endpoint to get details of a specific ChuanDauRa (PLO) as JSON.
    """
    plo = get_object_or_404(ChuanDauRa, pk=pk_cdr)
    data = {
        'pk': plo.pk,
        'ma_cdr': plo.ma_cdr,
        'noi_dung': plo.noi_dung,
        'loai_cdr': plo.loai_cdr,
        'dap_ung_muc_tieu': list(plo.dap_ung_muc_tieu.values_list('pk', flat=True))
    }
    return JsonResponse(data)

@require_http_methods(["POST"])
@permission_required('daotao.change_chuandaura', raise_exception=True)
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
            # Search within the context of a specific CTDT
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
        # Fallback to global search if no ctdt_pk is provided
        queryset = HocPhan.objects.all().order_by('ma_hoc_phan')
        if search_term:
            queryset = queryset.filter(
                Q(ma_hoc_phan__icontains=search_term) |
                Q(ten_hoc_phan__icontains=search_term)
            )

    paginator = Paginator(queryset, 30)  # 30 results per page
    try:
        hoc_phan_page = paginator.page(page)
    except PageNotAnInteger:
        hoc_phan_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
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

def get_hoc_phan_details(request, pk_hoc_phan):
    """
    API endpoint to get default details for a specific HocPhan.
    """
    try:
        hoc_phan = get_object_or_404(HocPhan, pk=pk_hoc_phan)
        data = {
            'tin_chi_ly_thuyet_apdung': hoc_phan.tin_chi_ly_thuyet_goc,
            'tin_chi_thuc_hanh_apdung': hoc_phan.tin_chi_thuc_hanh_goc,
            'so_gio_ly_thuyet_apdung': hoc_phan.so_gio_ly_thuyet_goc,
            'so_gio_thuc_hanh_apdung': hoc_phan.so_gio_thuc_hanh_goc,
            'so_gio_tu_hoc_apdung': hoc_phan.so_gio_tu_hoc_goc,
            # Add any other fields you want to auto-populate
        }
        return JsonResponse(data)
    except Http404:
        return JsonResponse({'error': 'HocPhan not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def search_hoc_phan_in_ctdt_api(request, pk_ctdt):
    """
    API endpoint for Select2 to search for courses (ChiTietHocPhanTrongCTDT)
    within a specific curriculum (CTDT).
    """
    search_term = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    
    try:
        ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
        
        # Query ChiTietHocPhanTrongCTDT objects related to the specific CTDT
        queryset = ChiTietHocPhanTrongCTDT.objects.filter(
            chuong_trinh_dao_tao=ctdt
        ).select_related('hoc_phan').order_by('hoc_phan__ma_hoc_phan')
        
        if search_term:
            queryset = queryset.filter(
                Q(hoc_phan__ma_hoc_phan__icontains=search_term) |
                Q(hoc_phan__ten_hoc_phan__icontains=search_term)
            )
            
        # Exclude the current course being edited, if its PK is provided
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

def api_get_de_cuong_chi_tiet(request, pk_hoc_phan):
    """
    API endpoint to get the detailed content of the active syllabus for a course.
    """
    # Find the active syllabus for the given course
    de_cuong = get_object_or_404(
        DeCuongHocPhan.objects.select_related('hoc_phan', 'hoc_phan__don_vi_quan_ly_goc'), 
        hoc_phan__pk=pk_hoc_phan, 
        la_phien_ban_hien_hanh=True
    )
    
    hoc_phan = de_cuong.hoc_phan

    # Serialize the main syllabus data
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

    # Serialize related CLOs (ChuanDauRaHocPhan)
    clos = de_cuong.chuan_dau_ra_cua_de_cuong.all().order_by('ma_clo')
    for clo in clos:
        data['chuan_dau_ra'].append({
            'ma_clo': clo.ma_clo,
            'noi_dung': clo.noi_dung,
            'muc_do_bloom': clo.get_muc_do_bloom_display()
        })

    # Serialize detailed content (NoiDungChiTietDeCuong)
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

    # Serialize evaluation methods (HinhThucDanhGia)
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
    """
    API endpoint to provide data for the Mermaid.js program flowchart.
    """
    def clean_mermaid_id(text):
        # Remove any character that is not a letter, number, or underscore
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
        
        # Use a set to keep track of added nodes to avoid duplicates
        added_nodes = set()

        for detail in details:
            # Use the original ma_hoc_phan for mapping, but a cleaned version for Mermaid ID
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

            # Add prerequisite edges
            for tien_quyet_detail in detail.hoc_phan_tien_quyet.all():
                source_id = clean_mermaid_id(tien_quyet_detail.hoc_phan.ma_hoc_phan)
                edges.append({
                    'source': source_id,
                    'target': hp_mermaid_id,
                    'type': 'tienquyet'
                })

            # Add concurrent edges
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

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
def danh_gia_cdr_api(request):
    # This function is intended for LLM-based evaluation.
    # For now, we'll return a placeholder success message.
    # In a real scenario, this would involve processing input,
    # calling an LLM, and returning evaluation results.
    try:
        data = json.loads(request.body)
        # Process data here, e.g., extract CDR content for LLM evaluation
        cdr_text = data.get('cdr_text', '') # Extract cdr_text from the received data
        
        # Call the LLM evaluation function
        evaluation_result = evaluate_cdr_with_llm(cdr_text)

        # Prepare the response based on the structured evaluation_result
        if isinstance(evaluation_result, dict):
            response_data = {
                "status": "success",
                "message": "CDR evaluation completed.",
                "cdr_text": cdr_text,
                "evaluation_results": {
                    "structural_analysis": {
                        "verb": evaluation_result.get("structural_analysis", {}).get("verb", "N/A"),
                        "knowledge": evaluation_result.get("structural_analysis", {}).get("knowledge", "N/A"),
                        "context": evaluation_result.get("structural_analysis", {}).get("context", "N/A"),
                    },
                    "evaluation": {
                        "relevance_level": evaluation_result.get("evaluation", {}).get("relevance_level", "N/A"),
                        "clarity": evaluation_result.get("evaluation", {}).get("clarity", "N/A"),
                    },
                    "improvement_suggestions": "\n".join(evaluation_result.get("improvement_suggestions", ["Không có đề xuất."])), # Join array into a single string
                    "cdr_cai_thien": evaluation_result.get("suggested_rewrite", "") # New field for suggested rewrite
                }
            }
        else:
            # Handle cases where LLM response was not a dict (e.g., error message)
            response_data = {
                "status": "error",
                "message": "LLM evaluation failed or returned an unexpected format.",
                "cdr_text": cdr_text,
                "evaluation_result_raw": evaluation_result # Include raw output for debugging
            }
        return JsonResponse(response_data)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
def get_ollama_status(request):
    """
    Checks the status of the Ollama server.
    """
    OLLAMA_API_URL = "http://172.250.4.30:11434/api/tags" 
    try:
        response = requests.get(OLLAMA_API_URL, timeout=5)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        # If we get here, the connection was successful
        data = response.json()
        return JsonResponse({
            'status': 'ok',
            'details': data
        })

    except requests.exceptions.Timeout:
        return JsonResponse({
            'status': 'error',
            'message': 'Connection timed out. The Ollama server is not responding.'
        }, status=504)
    except requests.exceptions.ConnectionError:
        return JsonResponse({
            'status': 'error',
            'message': 'Connection failed. Could not connect to the Ollama server. Is it running?'
        }, status=503)
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An unexpected error occurred: {str(e)}'
        }, status=500)

def api_suggest_tai_lieu(request, pk_de_cuong):
    return JsonResponse({})

def get_teaching_method_suggestions(request):
    return JsonResponse({})

def api_suggest_teaching_methods_from_clos(request):
    return JsonResponse({})

def api_suggest_summary(request):
    return JsonResponse({})

def api_search_giang_vien_chua_tham_gia(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    search_term = request.GET.get('q', '')
    
    queryset = GiangVien.objects.exclude(chuongtrinhdaotao=ctdt)
    if search_term:
        queryset = queryset.filter(
            Q(ho__icontains=search_term) |
            Q(ten__icontains=search_term) |
            Q(ma_can_bo__icontains=search_term)
        )
    
    results = [
        {'id': gv.pk, 'text': gv.ho_ten}
        for gv in queryset[:50]
    ]
    
    return JsonResponse({'results': results})

from django.http import HttpResponse

def check_api_connection_view(request):
    """
    A simple view to diagnose the connection to the external API from the web server process.
    """
    API_URL = 'http://172.16.2.92:8000/search'
    html = "<html><body><h1>API Connection Test</h1>"
    html += f"<p>Attempting to connect to API at: {API_URL}</p>"
    
    try:
        params = {'keyword': 'Zotero', 'limit': 1}
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        html += '<p style="color:green;">Connection successful!</p>'
        html += f"<p>The API responded with status code: {response.status_code}</p>"
        
        try:
            data = response.json()
            html += "<p>Successfully decoded JSON response.</p>"
            html += f"<p>Found {len(data)} item(s) in response.</p>"
            html += f"<pre>{json.dumps(data, indent=2)}</pre>"
        except ValueError:
            html += '<p style="color:red;">Failed to decode JSON from the response.</p>'

    except requests.exceptions.Timeout:
        html += '<p style="color:red;"><b>Connection timed out.</b> The API server is not responding.</p>'
        html += "<p>This confirms the Django web server process cannot reach the API server. Please check for firewalls or network configuration issues that might be blocking the connection for the web server.</p>"
    except requests.exceptions.ConnectionError as e:
        html += '<p style="color:red;"><b>Connection failed.</b> Could not connect to the API server.</p>'
        html += f"<p>Error details: {e}</p>"
        html += "<p>This is likely a network issue (e.g., firewall, DNS, incorrect IP) between the Django server and the API server.</p>"
    except Exception as e:
        html += f'<p style="color:red;">An unexpected error occurred: {e}</p>'
        
    html += "</body></html>"
    return HttpResponse(html)

def api_get_giang_vien_da_tham_gia(request, pk_ctdt):
    ctdt = get_object_or_404(ChuongTrinhDaoTao, pk=pk_ctdt)
    
    giang_vien_list = ctdt.giang_vien_tham_gia.all().order_by('ten', 'ho')
    
    results = [
        {'id': gv.pk, 'text': gv.ho_ten}
        for gv in giang_vien_list
    ]
    
    return JsonResponse({'results': results})

def api_get_phan_cong_form(request, pk_ctdt, pk_gv):
    return JsonResponse({})

def api_luu_phan_cong(request, pk_ctdt):
    return JsonResponse({})
    
@permission_required('daotao.change_muctieudaotao', raise_exception=True)
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

import requests

@login_required
def api_search_tai_lieu(request):
    search_term = request.GET.get('q', '').strip()
    # 1. Add a minimum length check for the search term
    if len(search_term) < 3:
        return JsonResponse({'results': []})

    # --- Combined Search Logic ---
    found_pks = set()

    # Step 1: Search locally and collect primary keys
    local_queryset = TaiLieuHocTap.objects.filter(
        Q(nhan_de__icontains=search_term) |
        Q(tac_gia__icontains=search_term)
    )[:50]
    for item in local_queryset:
        found_pks.add(item.pk)

    # Step 2: Search external API
    API_URL = 'http://172.16.2.92:8000/search'
    params = {'keyword': search_term, 'limit': 50}
    
    try:
        # 2. Increase the timeout to 30 seconds
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        api_results = response.json()

        for item in api_results:
            if not item.get('bib_id'):
                continue
            
            # Sync with local DB
            obj, created = TaiLieuHocTap.objects.update_or_create(
                bib_id=item.get('bib_id'),
                defaults={
                    'nhan_de': item.get('nhan_de'),
                    'tac_gia': item.get('tac_gia'),
                    'nam_xuat_ban': item.get('nam_xuat_ban'),
                    'duong_dan': item.get('duong_dan'),
                    'nha_xuat_ban': item.get('nha_xuat_ban'),
                    'loai_tai_lieu': 'SACH'
                }
            )
            found_pks.add(obj.pk)
            
    except requests.exceptions.RequestException as e:
        # Log the error but don't stop. This allows local results to still be returned.
        print(f"API search failed: {e}")

    # Step 3: Query all unique results from the local DB and format for Select2
    final_queryset = TaiLieuHocTap.objects.filter(pk__in=list(found_pks))
    results = [
        {
            'id': tl.pk,
            'text': f"{tl.nhan_de} ({tl.tac_gia}, {tl.nam_xuat_ban or 'N/A'})",
        }
        for tl in final_queryset
    ]
    
    return JsonResponse({'results': results})
