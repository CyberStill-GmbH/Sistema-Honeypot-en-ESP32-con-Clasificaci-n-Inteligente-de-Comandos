import socket, argparse
from clasificador import clasificar
from logger_csv import get_logger

BUFFER_SIZE = 8192

def run_udp_server(host: str = '0.0.0.0', port: int = 9999, ack: bool = True):
    logger = get_logger()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f'Servidor UDP escuchando en {host}:{port}')

    try:
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            source_ip, source_port = addr[0], addr[1]
            try:
                cmd = data.decode('utf-8', errors='ignore')
            except Exception:
                cmd = repr(data)

            res = clasificar(cmd)
            label = res.get('label')
            score = res.get('score', 0.0)
            reason = res.get('reason', '')

            logger.log(source_ip, cmd, label, score, reason)

            if ack:
                ack_msg = f'ACK:{label}:{score:.2f}'
                try:
                    sock.sendto(ack_msg.encode(), addr)
                except Exception:
                    pass
    except KeyboardInterrupt:
        print('Servidor detenido por usuario')
    finally:
        sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=9999, type=int)
    parser.add_argument('--no-ack', dest='ack', action='store_false')
    args = parser.parse_args()
    run_udp_server(args.host, args.port, ack=args.ack)
