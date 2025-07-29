# Essential Commands for CurHub Development

## Windows System Commands
- `dir` - List directory contents
- `cd <path>` - Change directory
- `type <file>` - Display file contents
- `findstr <pattern> <files>` - Search for text patterns
- `git status` - Check git status
- `git add .` - Stage all changes
- `git commit -m "message"` - Commit changes

## Python/Django Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Navigate to Django project
cd curhub
```

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load data (custom commands)
python manage.py import_hocphan
python manage.py import_ctdt
python manage.py import_hoc_phan_ctdt
python manage.py dump_data_utf8
```

### Development Server
```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Access admin interface
# http://localhost:8000/admin/

# Access main application
# http://localhost:8000/daotao/
```

### Utility Commands
```bash
# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Check for issues
python manage.py check
```

## Database Connection
- Ensure MySQL server is running
- Database: `curhub_db`
- Default port: 3306
- Charset: utf8mb4 (for Vietnamese support)