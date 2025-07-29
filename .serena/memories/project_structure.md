# Project Structure

## Root Directory
```
curhub_new/
├── curhub/                    # Main Django project
├── daotao/                    # Legacy/duplicate daotao app
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
├── *.csv                     # Data files
└── *.txt                     # Documentation files
```

## Main Django Project (curhub/)
```
curhub/
├── manage.py                 # Django management script
├── curhub/                   # Project settings package
│   ├── settings.py          # Main configuration
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py & asgi.py    # WSGI/ASGI applications
├── daotao/                   # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # URL patterns
│   ├── forms.py             # Form definitions
│   ├── admin.py             # Admin interface
│   ├── management/commands/ # Custom Django commands
│   ├── migrations/          # Database migrations
│   ├── templates/daotao/    # HTML templates
│   └── templatetags/        # Custom template tags
├── templates/               # Global templates
├── static/                  # Static files (CSS, JS, images)
└── Lession/                 # Documentation/lessons
```

## Key Applications
- **daotao**: Main application handling curriculum management
- **curhub.curhub**: Project configuration package

## Important Files
- `manage.py`: Django's command-line utility
- `settings.py`: Database, static files, and app configuration
- `models.py`: Database schema definitions
- `urls.py`: URL routing configuration