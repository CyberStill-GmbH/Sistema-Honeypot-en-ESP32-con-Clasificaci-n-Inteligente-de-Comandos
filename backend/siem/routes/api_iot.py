from flask import Blueprint, request, jsonify
from backend.siem.models import SessionLocal, Event
from backend.clasificador import clasificar
from backend.logger_csv import get_logger

api_iot = Blueprint("api_iot", __name__)

logger = get_logger()

@api_iot.post("/siem/api/iot/event")
def ingest_event():
    data = request.get_json(silent=True) or {}

    cmd = (data.get("cmd") or "").strip()
    source_ip = request.remote_addr or "iot"

    if not cmd:
        return jsonify({"success": False, "error": "cmd vacío"}), 400

    # 1. Clasificar
    res = clasificar(cmd)

    label = res["label"]
    score = res["score"]
    reason = res["reason"]

    # 2. Guardar en CSV
    logger.log(source_ip, cmd, label, score, reason)

    # 3. Guardar en la BASE DE DATOS (para el dashboard)
    db = SessionLocal()
    try:
        event = Event(
            source_ip=source_ip,
            raw_cmd=cmd,
            label=label,
            score=score,
            reason=reason
        )
        db.add(event)
        db.commit()
    finally:
        db.close()

    # 4. Respuesta al ESP32
    return jsonify({
        "success": True,
        "label": label,
        "score": score,
        "reason": reason
    })
