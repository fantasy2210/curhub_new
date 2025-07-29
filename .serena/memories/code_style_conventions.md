# Code Style and Conventions

## Language and Naming
- **Primary Language**: Vietnamese for user-facing content
- **Code Comments**: Mixed Vietnamese and English
- **Variable Names**: Vietnamese with underscores (snake_case)
  - `ten_hoc_phan` (course name)
  - `ma_hoc_phan` (course code)
  - `chuong_trinh_dao_tao` (training program)
  - `don_vi_dao_tao` (training unit)

## Django Conventions
- **Models**: PascalCase class names with Vietnamese context
  - `ChuongTrinhDaoTao`, `HocPhan`, `DonViDaoTao`
- **Views**: Function-based views with descriptive Vietnamese names
  - `danh_sach_ctdt`, `them_hoc_phan`, `sua_don_vi`
- **URLs**: Kebab-case with Vietnamese terms
  - `danh-sach-ctdt`, `hoc-phan/them`, `don-vi/sua`
- **Templates**: Organized in app-specific directories
  - `templates/daotao/danh_sach_*.html`

## Database Design
- **Field Names**: Vietnamese snake_case
- **Relationships**: Clear foreign key naming
- **Meta Classes**: Vietnamese verbose names and plurals
- **UTF-8 Support**: All text fields support Vietnamese characters

## Template Structure
- **Base Template**: `templates/base.html`
- **AdminLTE Integration**: Bootstrap 5 + AdminLTE theme
- **Form Rendering**: Crispy Forms with Bootstrap 5
- **Partials**: Reusable components in `partials/` directories

## File Organization
- **Static Files**: Organized by plugin/library in `static/adminlte/plugins/`
- **Templates**: App-specific organization
- **Management Commands**: Custom commands for data import/export
- **Migrations**: Sequential numbering with descriptive names

## Best Practices
- Use Django's built-in authentication system
- Implement proper error handling
- Follow Django's security best practices
- Maintain UTF-8 encoding throughout the application