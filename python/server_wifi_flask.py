from flask import Flask, request, jsonify
from clasificador import clasificar
from logger_csv import get_logger

app = Flask(__name__)
logger = get_logger()

@app.route('/cmd', methods=['POST'])
def cmd():
    data = request.get_json(silent=True) or {}
    cmd_text = data.get('cmd') or request.form.get('cmd') or ''
    source = request.remote_addr
    res = clasificar(cmd_text)
    logger.log(source, cmd_text, res.get('label'), res.get('score', 0.0), res.get('reason', ''))
    return jsonify({'status': 'ok', 'label': res.get('label'), 'score': res.get('score')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
