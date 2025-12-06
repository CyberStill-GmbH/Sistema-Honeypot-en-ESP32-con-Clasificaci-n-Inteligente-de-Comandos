from flask import Flask, jsonify
from werkzeug.security import generate_password_hash
import secrets
from flask_cors import CORS

from .config_siem import SECRET_KEY, DEBUG, DATABASE_URI
from .models import init_db, SessionLocal, AdminUser, ApiToken

# Importar blueprints (rutas API)
from backend.siem.routes.api_auth import api_auth
from backend.siem.routes.api_admin import api_admin
from backend.siem.routes.api_stats import api_stats
from backend.siem.routes.api_ingest import api_ingest
from backend.siem.routes.api_tokens import api_tokens
from backend.siem.routes.api_iot import api_iot

# ============================================================
#   CREAR ADMIN + TOKEN POR DEFECTO
# ============================================================

def _ensure_default_admin_and_token():
    db = SessionLocal()
    try:
        # ADMIN
        admin = db.query(AdminUser).filter_by(username="admin").first()
        if not admin:
            admin = AdminUser(
                username="admin",
                password_hash=generate_password_hash("admin123"),
                is_active=True,
            )
            db.add(admin)
            db.commit()
            print("=== SIEM: Admin creado (admin/admin123) ===")

        # TOKEN DEFAULT
        token = db.query(ApiToken).filter_by(owner="default").first()
        if not token:
            raw = secrets.token_hex(32)
            token = ApiToken(
                token=raw,
                owner="default",
                active=True,
            )
            db.add(token)
            db.commit()
            print(f"=== SIEM: Token por defecto creado: {raw} ===")

    finally:
        db.close()


# ============================================================
#   FACTORY PRINCIPAL DE FLASK
# ============================================================

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = DEBUG

    CORS(app)

    # Inicializar DB
    init_db()
    _ensure_default_admin_and_token()

    # Endpoint mínimo de salud
    @app.route("/")
    def health():
        return jsonify({"status": "ok", "message": "SIEM backend running"})

    # Registrar blueprints
    app.register_blueprint(api_auth)     # /siem/api/auth/...
    app.register_blueprint(api_admin)    # /siem/api/admin/...
    app.register_blueprint(api_stats)    # /siem/api/stats/...
    app.register_blueprint(api_ingest)   # /siem/api/ingest
    app.register_blueprint(api_tokens)  # /siem/api/tokens/...
    app.register_blueprint(api_iot)     # /siem/api/events/...
    return app


# ============================================================
#   MAIN
# ============================================================

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=DEBUG)