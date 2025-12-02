from siem.app import create_app

# Creamos la app del SIEM y la levantamos
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)
