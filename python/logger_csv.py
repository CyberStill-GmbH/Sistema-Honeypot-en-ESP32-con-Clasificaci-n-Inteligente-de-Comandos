import csv, os
from datetime import datetime
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

LOG_FILE = os.path.join(os.path.dirname(__file__), 'events.csv')
FIELDNAMES = ['timestamp', 'source_ip', 'raw_cmd', 'label', 'score', 'reason']

def _color_for_label(label: str) -> str:
    label = (label or '').lower()
    if label == 'normal':
        return Fore.GREEN
    if label in ('sospechoso', 'suspicious', 'desconocido'):
        return Fore.YELLOW
    if label == 'exploit':
        return Fore.RED + Style.BRIGHT
    if label == 'empty':
        return Fore.CYAN
    return Fore.WHITE

class CsvLogger:
    def __init__(self, logfile: str = LOG_FILE):
        self.logfile = logfile
        if not os.path.exists(self.logfile):
            with open(self.logfile, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writeheader()

    def log(self, source_ip: str, raw_cmd: str, label: str, score: float, reason: str):
        row = {
            'timestamp': datetime.utcnow().isoformat(),
            'source_ip': source_ip,
            'raw_cmd': raw_cmd,
            'label': label,
            'score': score,
            'reason': reason,
        }
        with open(self.logfile, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writerow(row)

        color = _color_for_label(label)
        print(color + f"[{row['timestamp']}] {source_ip} -> {label} (score={score:.2f}) : {raw_cmd}")
        if label == 'exploit':
            print(Fore.RED + 'ALERTA: Posible exploit detectado!')
        elif label == 'sospechoso':
            print(Fore.YELLOW + 'ALERTA: Comando sospechoso')

_default_logger = CsvLogger()

def get_logger():
    return _default_logger
