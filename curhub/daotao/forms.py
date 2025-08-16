from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, Submit, HTML, Field
from .models import (
    NganhDaoTao, ChuongTrinhDaoTao, HocPhan, ChiTietHocPhanTrongCTDT,
    DonViDaoTao, MucTieuDaoTao, ChuanDauRa, DanhMucKienThuc, DeCuongHocPhan, ChuanDauRaHocPhan, NoiDungChiTietDeCuong, HinhThucDanhGia,
    GiangVien, PhanCongGiangDay, TaiLieuHocTap, DeCuongTaiLieu
)

class NganhDaoTaoForm(forms.ModelForm):
    class Meta:
        model = NganhDaoTao
        fields = '__all__'

class ChuongTrinhDaoTaoModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column(
                    Fieldset(
                        'Thông tin Định danh',
                        Row(
                            Column('ma_nganh_ctdt', css_class='form-group col-md-6 mb-0'),
                            Column('ten_nganh_ctdt', css_class='form-group col-md-6 mb-0'),
                        ),
                        'ten_tieng_anh',
                        css_class='card-body'
                    ),
                    Fieldset(
                        'Thông tin Mô tả',
                        'mo_ta_chung',
                        'doi_tuong_tuyen_sinh',
                        'dieu_kien_tot_nghiep',
                        'chuong_trinh_tham_khao',
                        css_class='card-body'
                    ),
                    css_class='col-lg-8'
                ),
                Column(
                    Fieldset(
                        'Thuộc tính & Phân loại',
                        'don_vi_quan_ly',
                        'nganh_hoc_chung',
                        'trinh_do_dao_tao',
                        'hinh_thuc_dao_tao',
                        'van_bang_tot_nghiep',
                        'so_tin_chi_yeu_cau',
                        'thoi_gian_dao_tao',
                        css_class='card-body'
                    ),
                    Fieldset(
                        'Thông tin Ban hành',
                        'so_quyet_dinh_ban_hanh',
                        'ngay_ban_hanh_qd',
                        'ghi_chu_ctdt',
                        css_class='card-body'
                    ),
                    Submit('submit', 'Lưu Chương Trình', css_class='btn btn-primary w-100'),
                    HTML('<a href="{% url \'daotao:danh_sach_ctdt\' %}" class="btn btn-secondary w-100 mt-2">Hủy</a>'),
                    css_class='col-lg-4'
                )
            )
        )

    class Meta:
        model = ChuongTrinhDaoTao
        fields = [
            'ma_nganh_ctdt', 'ten_nganh_ctdt', 'ten_tieng_anh', 'nganh_hoc_chung',
            'trinh_do_dao_tao', 'hinh_thuc_dao_tao', 'so_tin_chi_yeu_cau',
            'thoi_gian_dao_tao', 'doi_tuong_tuyen_sinh', 'dieu_kien_tot_nghiep',
            'van_bang_tot_nghiep', 'chuong_trinh_tham_khao', 'don_vi_quan_ly',
            'mo_ta_chung', 'so_quyet_dinh_ban_hanh', 'ngay_ban_hanh_qd', 'ghi_chu_ctdt'
        ]
        widgets = {
            # Textarea fields for Summernote
            'mo_ta_chung': forms.Textarea(attrs={'class': 'summernote'}),
            'doi_tuong_tuyen_sinh': forms.Textarea(attrs={'class': 'summernote'}),
            'dieu_kien_tot_nghiep': forms.Textarea(attrs={'class': 'summernote'}),
            'chuong_trinh_tham_khao': forms.Textarea(attrs={'class': 'summernote'}),
            'ghi_chu_ctdt': forms.Textarea(attrs={'rows': 3}),

            # Select fields for Select2
            'nganh_hoc_chung': forms.Select(attrs={'class': 'select2'}),
            'trinh_do_dao_tao': forms.Select(attrs={'class': 'select2'}),
            'hinh_thuc_dao_tao': forms.Select(attrs={'class': 'select2'}),
            'van_bang_tot_nghiep': forms.Select(attrs={'class': 'select2'}),
            'don_vi_quan_ly': forms.Select(attrs={'class': 'select2'}),
            
            # Date picker
            'ngay_ban_hanh_qd': forms.DateInput(attrs={'type': 'date'}),
        }

class HocPhanLibModelForm(forms.ModelForm):
    class Meta:
        model = HocPhan
        fields = '__all__'

class ChiTietHocPhanTrongCTDTModelForm(forms.ModelForm):
    class Meta:
        model = ChiTietHocPhanTrongCTDT
        fields = '__all__'
        exclude = ('chuong_trinh_dao_tao',)
        widgets = {
            # Use standard widgets; they will be replaced/enhanced in __init__
            'hoc_phan_tien_quyet': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'hoc_phan_song_hanh': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'danh_muc_kien_thuc': forms.Select(attrs={'class': 'form-control select2'}),
            'khoi_kien_thuc': forms.Select(attrs={'class': 'form-control select2'}),
        }

    def __init__(self, *args, **kwargs):
        # The ctdt instance is passed from the view
        ctdt = kwargs.pop('ctdt', None)
        # Allow passing a custom queryset for the 'hoc_phan' field
        hoc_phan_qs = kwargs.pop('hoc_phan_queryset', None)
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')

        # --- AJAX for 'hoc_phan' field (main course selection) ---
        # Use the provided queryset if available, otherwise determine it based on the instance
        if hoc_phan_qs is not None:
            final_hoc_phan_queryset = hoc_phan_qs
        else:
            final_hoc_phan_queryset = HocPhan.objects.none()
            if instance and instance.pk and instance.hoc_phan:
                final_hoc_phan_queryset = HocPhan.objects.filter(pk=instance.hoc_phan.pk)

        self.fields['hoc_phan'] = forms.ModelChoiceField(
            queryset=final_hoc_phan_queryset,
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_hoc_phan'})
        )
        if instance and instance.pk:
            self.fields['hoc_phan'].disabled = True

        # --- AJAX for 'hoc_phan_tien_quyet' and 'hoc_phan_song_hanh' fields ---
        # The queryset should contain all possible choices for the dropdowns.
        possible_choices_qs = ChiTietHocPhanTrongCTDT.objects.none()
        if ctdt:
            possible_choices_qs = ChiTietHocPhanTrongCTDT.objects.filter(chuong_trinh_dao_tao=ctdt)
            # If editing, exclude the current instance from being a prerequisite/concurrent of itself
            if instance and instance.pk:
                possible_choices_qs = possible_choices_qs.exclude(pk=instance.pk)

        tien_quyet_queryset = possible_choices_qs
        song_hanh_queryset = possible_choices_qs

        # If editing, we still need to set the initial selected values for the form to render them.
        # The queryset for the field must contain these initial values.
        if instance and instance.pk:
            # Combine the possible choices with the already selected ones to ensure they are in the queryset for validation
            tien_quyet_queryset = (possible_choices_qs | instance.hoc_phan_tien_quyet.all()).distinct()
            song_hanh_queryset = (possible_choices_qs | instance.hoc_phan_song_hanh.all()).distinct()

        # Use a specific class to target these fields with AJAX-powered Select2
        widget_attrs = {
            'class': 'form-control select2-ajax-ctdt',
            'data-ctdt-pk': ctdt.pk if ctdt else ''
        }

        self.fields['hoc_phan_tien_quyet'] = forms.ModelMultipleChoiceField(
            queryset=tien_quyet_queryset,
            widget=forms.SelectMultiple(attrs=widget_attrs),
            required=False
        )
        self.fields['hoc_phan_song_hanh'] = forms.ModelMultipleChoiceField(
            queryset=song_hanh_queryset,
            widget=forms.SelectMultiple(attrs=widget_attrs),
            required=False
        )

class DonViDaoTaoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Thông tin Đơn vị Đào tạo',
                'ma_don_vi',
                'ten_don_vi',
                'don_vi_cha',
                'mo_ta',
                css_class='card-body'
            ),
            Row(
                Column(
                    Submit('submit', 'Lưu Đơn vị', css_class='btn btn-primary w-100'),
                    css_class='col-lg-6'
                ),
                Column(
                    HTML('<a href="{% url \'daotao:danh_sach_don_vi\' %}" class="btn btn-secondary w-100">Hủy</a>'),
                    css_class='col-lg-6'
                )
            )
        )

    class Meta:
        model = DonViDaoTao
        fields = ['ma_don_vi', 'ten_don_vi', 'don_vi_cha', 'mo_ta']
        widgets = {
            'don_vi_cha': forms.Select(attrs={'class': 'select2'}),
            'mo_ta': forms.Textarea(attrs={'class': 'summernote'}),
        }

class MucTieuDaoTaoForm(forms.ModelForm):
    class Meta:
        model = MucTieuDaoTao
        fields = ['ma_muc_tieu', 'noi_dung']
        widgets = {
            'noi_dung': forms.Textarea(attrs={'rows': 4}),
        }

class ChuanDauRaForm(forms.ModelForm):
    dap_ung_muc_tieu = forms.ModelMultipleChoiceField(
        queryset=MucTieuDaoTao.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Đáp ứng Mục tiêu Đào tạo (PO)"
    )

    class Meta:
        model = ChuanDauRa
        fields = ['ma_cdr', 'noi_dung', 'loai_cdr', 'dap_ung_muc_tieu']
        widgets = {
            'noi_dung': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        ctdt = kwargs.pop('ctdt', None)
        super().__init__(*args, **kwargs)
        if ctdt:
            self.fields['dap_ung_muc_tieu'].queryset = MucTieuDaoTao.objects.filter(chuong_trinh_dao_tao=ctdt)

    def clean_ma_cdr(self):
        # This validation is now handled in the view to provide a more specific error message
        # based on the instance and program.
        return self.cleaned_data.get('ma_cdr')

MucTieuDaoTaoFormSet = inlineformset_factory(
    ChuongTrinhDaoTao,
    MucTieuDaoTao,
    form=MucTieuDaoTaoForm,
    fk_name='chuong_trinh_dao_tao',
    extra=1,
    can_delete=True
)

ChuanDauRaFormSet = inlineformset_factory(
    ChuongTrinhDaoTao,
    ChuanDauRa,
    form=ChuanDauRaForm,
    fk_name='chuong_trinh_dao_tao',
    extra=1,
    can_delete=True
)

class UploadHocPhanCTDTForm(forms.Form):
    file = forms.FileField(label="Chọn tệp Excel (.xlsx) hoặc CSV (.csv)")

class DanhMucKienThucForm(forms.ModelForm):
    class Meta:
        model = DanhMucKienThuc
        fields = '__all__'

class DeCuongHocPhanForm(forms.ModelForm):
    # New fields for selecting main and reference documents
    tai_lieu_chinh = forms.ModelMultipleChoiceField(
        queryset=TaiLieuHocTap.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2-ajax-tai-lieu', 'data-placeholder': 'Chọn tài liệu chính...'}),
        required=True,
        label="2.1 Tài liệu chính (yêu cầu ít nhất 1)"
    )
    tai_lieu_tham_khao = forms.ModelMultipleChoiceField(
        queryset=TaiLieuHocTap.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2-ajax-tai-lieu', 'data-placeholder': 'Chọn tài liệu tham khảo...'}),
        required=False,
        label="2.2 Tài liệu tham khảo"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing an existing instance, populate the initial values for the new fields
        if self.instance and self.instance.pk:
            # Get all related documents and categorize them
            main_docs = self.instance.tailieu_lien_ket.filter(loai_lien_ket='MAIN').values_list('tai_lieu_id', flat=True)
            ref_docs = self.instance.tailieu_lien_ket.filter(loai_lien_ket='REFERENCE').values_list('tai_lieu_id', flat=True)
            
            self.initial['tai_lieu_chinh'] = list(main_docs)
            self.initial['tai_lieu_tham_khao'] = list(ref_docs)

            # The queryset for the fields must contain the initial values for validation
            all_selected_ids = list(main_docs) + list(ref_docs)
            self.fields['tai_lieu_chinh'].queryset = TaiLieuHocTap.objects.filter(id__in=all_selected_ids)
            self.fields['tai_lieu_tham_khao'].queryset = TaiLieuHocTap.objects.filter(id__in=all_selected_ids)
        else:
            # For new forms, the queryset should be empty.
            self.fields['tai_lieu_chinh'].queryset = TaiLieuHocTap.objects.none()
            self.fields['tai_lieu_tham_khao'].queryset = TaiLieuHocTap.objects.none()

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            # Existing layout fields...
            # I will add the new fields to the layout in the template directly for now.
        )

    def clean(self):
        cleaned_data = super().clean()
        tai_lieu_chinh = cleaned_data.get("tai_lieu_chinh")
        tai_lieu_tham_khao = cleaned_data.get("tai_lieu_tham_khao")

        if tai_lieu_chinh and tai_lieu_tham_khao:
            # Check for any intersection between the two querysets
            if set(tai_lieu_chinh).intersection(set(tai_lieu_tham_khao)):
                raise forms.ValidationError(
                    "Một tài liệu không thể vừa là tài liệu chính vừa là tài liệu tham khảo."
                )
        
        return cleaned_data

    def save(self, commit=True):
        # Override save to handle the new M2M-like fields
        instance = super().save(commit)
        
        # Clear existing relations
        instance.tailieu_lien_ket.all().delete()
        
        # Add new relations for main documents
        for tai_lieu in self.cleaned_data['tai_lieu_chinh']:
            DeCuongTaiLieu.objects.create(de_cuong=instance, tai_lieu=tai_lieu, loai_lien_ket='MAIN')
            
        # Add new relations for reference documents
        for tai_lieu in self.cleaned_data['tai_lieu_tham_khao']:
            DeCuongTaiLieu.objects.create(de_cuong=instance, tai_lieu=tai_lieu, loai_lien_ket='REFERENCE')
            
        return instance

    class Meta:
        model = DeCuongHocPhan
        fields = [
            'tom_tat_noi_dung',
            'phuong_phap_day_hoc',
            'thang_diem_danh_gia',
            'cac_yeu_cau_khac',
            'quy_dinh_hoc_phan',
            'cac_loai_hoc_lieu_khac',
            'giang_vien_bien_soan',
            # Các trường khác của DeCuongHocPhan có thể được thêm vào đây nếu cần chỉnh sửa trên cùng form
            # Ví dụ: 'ten_de_cuong_phien_ban', 'ngay_ban_hanh', 'la_phien_ban_hien_hanh'
        ]
        widgets = {
            'tom_tat_noi_dung': forms.Textarea(attrs={'class': 'summernote', 'rows': 5}),
            'phuong_phap_day_hoc': forms.Textarea(attrs={'class': 'summernote', 'rows': 4}),
            'thang_diem_danh_gia': forms.Textarea(attrs={'class': 'summernote', 'rows': 4}),
            'cac_yeu_cau_khac': forms.Textarea(attrs={'rows': 3}),
            'quy_dinh_hoc_phan': forms.Textarea(attrs={'class': 'summernote', 'rows': 4}),
            'cac_loai_hoc_lieu_khac': forms.Textarea(attrs={'rows': 3}),
            'giang_vien_bien_soan': forms.SelectMultiple(attrs={'class': 'select2'}),
        }
        labels = {
            'tom_tat_noi_dung': '3. Mô tả học phần (Course description)',
            'phuong_phap_day_hoc': '4. Phương pháp dạy và học',
            'thang_diem_danh_gia': '5. Thang điểm/Cách đánh giá',
            'cac_yeu_cau_khac': '6. Các yêu cầu khác',
            'quy_dinh_hoc_phan': '8. Các quy định',
            'cac_loai_hoc_lieu_khac': '2.3 Các loại học liệu khác', # This field will now be manually placed
            'giang_vien_bien_soan': '9. Giảng viên biên soạn',
        }


class ChuanDauRaHocPhanForm(forms.ModelForm):
    dap_ung_cdr_ctdt = forms.ModelMultipleChoiceField(
        queryset=ChuanDauRa.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'select2', 'data-placeholder': 'Chọn CĐR của CTĐT'}),
        required=False,
        label="Đáp ứng CĐR của CTĐT"
    )

    class Meta:
        model = ChuanDauRaHocPhan
        fields = ['ma_clo', 'noi_dung', 'loai_clo', 'dap_ung_cdr_ctdt', 'trinh_do_nang_luc', 'tua']
        widgets = {
            'ma_clo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CLO.1'}),
            'noi_dung': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'loai_clo': forms.Select(attrs={'class': 'form-control'}),
            'trinh_do_nang_luc': forms.TextInput(attrs={'class': 'form-control'}),
            'tua': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'ma_clo': 'STT',
            'noi_dung': 'Chuẩn đầu ra của học phần',
            'loai_clo': 'Phân loại (ẩn/hiện theo nhóm)',
            'trinh_do_nang_luc': 'Trình độ năng lực',
        }

    def __init__(self, *args, **kwargs):
        # Lấy instance của DeCuongHocPhan từ view để lọc ChuanDauRa (PLO)
        de_cuong_instance = kwargs.pop('de_cuong', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False # Không render a <form> tag
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                Column('ma_clo', css_class='form-group col-md-1 mb-0'),
                Column('noi_dung', css_class='form-group col-md-5 mb-0'),
                Column('dap_ung_cdr_ctdt', css_class='form-group col-md-3 mb-0'),
                Column('trinh_do_nang_luc', css_class='form-group col-md-2 mb-0'),
                Column('tua', css_class='form-group col-md-1 mb-0'),
                # Ẩn trường loai_clo, giá trị của nó sẽ được set bằng JS dựa vào nhóm
                Field('loai_clo', type="hidden"),
            )
        )

        if de_cuong_instance:
            # Tìm các CTĐT có chứa học phần này
            ctdt_pks = ChiTietHocPhanTrongCTDT.objects.filter(
                hoc_phan=de_cuong_instance.hoc_phan
            ).values_list('chuong_trinh_dao_tao_id', flat=True)
            
            if ctdt_pks:
                # Lọc các PLO thuộc các CTĐT đó
                self.fields['dap_ung_cdr_ctdt'].queryset = ChuanDauRa.objects.filter(
                    chuong_trinh_dao_tao_id__in=list(ctdt_pks)
                ).order_by('ma_cdr')

ChuanDauRaHocPhanFormSet = inlineformset_factory(
    DeCuongHocPhan,
    ChuanDauRaHocPhan,
    form=ChuanDauRaHocPhanForm,
    fk_name='de_cuong',
    extra=1,
    can_delete=True
)


class NoiDungChiTietDeCuongForm(forms.ModelForm):
    class Meta:
        model = NoiDungChiTietDeCuong
        fields = ['tuan_hoc_hoac_chu_de', 'noi_dung_giang_day', 'so_gio_ly_thuyet',
                  'so_gio_thuc_hanh', 'so_gio_tu_hoc', 'ky_nang_thai_do', 'chuan_dau_ra_lien_quan']
        widgets = {
            'noi_dung_giang_day': forms.Textarea(attrs={'rows': 2}),
            'ky_nang_thai_do': forms.Textarea(attrs={'rows': 2}),
            'chuan_dau_ra_lien_quan': forms.SelectMultiple(attrs={'class': 'select2'}),
        }

NoiDungChiTietDeCuongFormSet = inlineformset_factory(
    DeCuongHocPhan,
    NoiDungChiTietDeCuong,
    form=NoiDungChiTietDeCuongForm,
    fk_name='de_cuong_hoc_phan',
    extra=1,
    can_delete=True
)

class DoiSanhCTDTForm(forms.Form):
    ctdt1 = forms.ModelChoiceField(
        queryset=ChuongTrinhDaoTao.objects.all().order_by('ten_nganh_ctdt'),
        label="Chọn Chương trình Đào tạo thứ nhất",
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    ctdt2 = forms.ModelChoiceField(
        queryset=ChuongTrinhDaoTao.objects.all().order_by('ten_nganh_ctdt'),
        label="Chọn Chương trình Đào tạo thứ hai",
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('tom_tat_noi_dung', css_class='col-md-12'),
            ),
            Submit('submit', 'Đối sánh', css_class='btn btn-primary mt-3')
        )

class HinhThucDanhGiaForm(forms.ModelForm):
    class Meta:
        model = HinhThucDanhGia
        fields = ['loai_danh_gia', 'ten_hinh_thuc', 'ty_le_diem', 'chuan_dau_ra_danh_gia']
        widgets = {
            'chuan_dau_ra_danh_gia': forms.SelectMultiple(attrs={'class': 'select2'}),
        }

HinhThucDanhGiaFormSet = inlineformset_factory(
    DeCuongHocPhan,
    HinhThucDanhGia,
    form=HinhThucDanhGiaForm,
    fk_name='de_cuong_hoc_phan',
    extra=1,
    can_delete=True
)

class GiangVienForm(forms.ModelForm):
    class Meta:
        model = GiangVien
        fields = '__all__'
        widgets = {
            'ngay_sinh': forms.DateInput(attrs={'type': 'date'}),
            'co_quan_cong_tac': forms.Select(attrs={'class': 'select2'}),
        }

class PhanCongForm(forms.ModelForm):
    class Meta:
        model = PhanCongGiangDay
        fields = ['giang_vien', 'vai_tro']
        widgets = {
            'giang_vien': forms.Select(attrs={'class': 'select2'}),
        }

class TaiLieuHocTapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Thông tin Tài liệu',
                Row(
                    Column('nhan_de', css_class='form-group col-md-12 mb-0'),
                ),
                Row(
                    Column('tac_gia', css_class='form-group col-md-6 mb-0'),
                    Column('ngon_ngu', css_class='form-group col-md-6 mb-0'),
                ),
                Row(
                    Column('nha_xuat_ban', css_class='form-group col-md-6 mb-0'),
                    Column('noi_xuat_ban', css_class='form-group col-md-6 mb-0'),
                ),
                Row(
                    Column('nam_xuat_ban', css_class='form-group col-md-4 mb-0'),
                    Column('dewey', css_class='form-group col-md-4 mb-0'),
                    Column('cutter', css_class='form-group col-md-4 mb-0'),
                ),
                Row(
                    Column('loai_tai_lieu', css_class='form-group col-md-6 mb-0'),
                    Column('duong_dan', css_class='form-group col-md-6 mb-0'),
                ),
                'tom_tat',
                css_class='card-body'
            )
        )

    class Meta:
        model = TaiLieuHocTap
        fields = [
            'nhan_de', 'ngon_ngu', 'tac_gia', 'noi_xuat_ban', 'nha_xuat_ban', 
            'nam_xuat_ban', 'dewey', 'cutter', 'tom_tat', 'loai_tai_lieu', 'duong_dan'
        ]
        widgets = {
            'tom_tat': forms.Textarea(attrs={'rows': 3}),
            'loai_tai_lieu': forms.Select(attrs={'class': 'select2'}),
        }

class DeCuongTaiLieuForm(forms.ModelForm):
    class Meta:
        model = DeCuongTaiLieu
        fields = ['loai_lien_ket', 'tai_lieu']
        widgets = {
            'tai_lieu': forms.Select(attrs={'class': 'select2-ajax-tai-lieu'}),
            'loai_lien_ket': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'tai_lieu': 'Tài liệu',
            'loai_lien_ket': 'Loại học liệu',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        tai_lieu_field = self.fields['tai_lieu']
        
        # This is the key change for AJAX behavior.
        # We ensure the queryset is empty unless there's a specific instance,
        # preventing the dropdown from loading all 7000+ items.
        if self.instance and self.instance.pk and self.instance.tai_lieu:
            # If the form is bound to an existing instance,
            # the queryset must contain the selected item for validation.
            tai_lieu_field.queryset = TaiLieuHocTap.objects.filter(pk=self.instance.tai_lieu.pk)
            # Add a data attribute to the widget to hold the initial text.
            # This is crucial for the frontend to display the initial value.
            tai_lieu_field.widget.attrs['data-initial-text'] = self.instance.tai_lieu.nhan_de
        else:
            # For new forms, the queryset should be empty.
            # The user will use the AJAX search to find and select a document.
            tai_lieu_field.queryset = TaiLieuHocTap.objects.none()

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                Column('loai_lien_ket', css_class='form-group col-md-3 mb-0'),
                Column('tai_lieu', css_class='form-group col-md-9 mb-0'),
            )
        )

DeCuongTaiLieuFormSet = inlineformset_factory(
    DeCuongHocPhan,
    DeCuongTaiLieu,
    form=DeCuongTaiLieuForm,
    fk_name='de_cuong',
    extra=1,
    can_delete=True
)
