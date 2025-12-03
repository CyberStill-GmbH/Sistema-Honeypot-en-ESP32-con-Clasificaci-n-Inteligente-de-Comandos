import os

# Carpeta base del módulo SIEM
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Usamos SQLite como base de datos local
DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'siem.db')

# Clave secreta para Flask (para sesiones, CSRF, etc.)
SECRET_KEY = 'b7c7e8f409d8a1303f77c7639f6ea772a230d442004441f307e0ea1d9abf7b68'

# Modo debug activado mientras desarrollas
DEBUG = True
