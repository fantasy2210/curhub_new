# daotao/navigation.py

def get_menu_items(user):
    """
    Trả về một danh sách các mục menu dựa trên quyền của người dùng.
    Mỗi mục là một dict với các key: 'name', 'url', 'icon', 'required_perm'.
    """
    all_menus = [
        {
            'name': 'Quản lý CTĐT',
            'url': 'daotao:danh_sach_ctdt',
            'icon': 'fas fa-sitemap',
            'required_perm': 'daotao.view_chuongtrinhdaotao',
        },
        {
            'name': 'Quản lý Học phần',
            'url': 'daotao:danh_sach_hoc_phan',
            'icon': 'fas fa-book',
            'required_perm': 'daotao.view_hocphan',
        },
        {
            'name': 'Quản lý Đơn vị',
            'url': 'daotao:danh_sach_don_vi',
            'icon': 'fas fa-university',
            'required_perm': 'daotao.view_donvidaotao',
        },
        {
            'name': 'Danh mục Kiến thức',
            'url': 'daotao:danh_sach_danh_muc_kien_thuc',
            'icon': 'fas fa-list-alt',
            'required_perm': 'daotao.view_danhmuckienthuc',
        },
        {
            'name': 'Đối sánh CTĐT',
            'url': 'daotao:doi_sanh_ctdt',
            'icon': 'fas fa-balance-scale',
            'required_perm': None,
        },
    ]

    visible_menus = []
    for menu in all_menus:
        if menu['required_perm'] is None or user.has_perm(menu['required_perm']):
            visible_menus.append(menu)
    
    return visible_menus
