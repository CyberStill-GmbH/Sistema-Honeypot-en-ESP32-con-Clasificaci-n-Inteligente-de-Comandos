import socket
from clasificador import clasificar
from logger_csv import get_logger

BUFFER_SIZE = 8192

def run_udp_server(host: str = '192.168.18.41', port: int = 6000, ack: bool = True):
    logger = get_logger()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))  # Escucha en la IP y puerto especificados
    print(f'Servidor UDP escuchando en {host}:{port}')

    try:
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)  # Espera a recibir datos
            source_ip, source_port = addr[0], addr[1]  # Dirección de origen

            try:
                cmd = data.decode('utf-8', errors='ignore')  # Decodifica el comando recibido
            except Exception:
                cmd = repr(data)  # Si hay un error en la decodificación, muestra los datos sin procesar

            # Clasifica el comando recibido
            res = clasificar(cmd)
            label = res.get('label')
            score = res.get('score', 0.0)
            reason = res.get('reason', '')

            # Registra la acción en el archivo de logs
            logger.log(source_ip, cmd, label, score, reason)

            if ack:
                ack_msg = f'ACK:{label}:{score:.2f}'  # Prepara un mensaje de confirmación
                try:
                    sock.sendto(ack_msg.encode(), addr)  # Envía el ACK de vuelta al origen
                except Exception:
                    pass
    except KeyboardInterrupt:
        print('Servidor detenido por usuario')
    finally:
        sock.close()  # Cierra el socket cuando termine

if __name__ == '__main__':
    run_udp_server(host='192.168.18.41', port=6000)  # Especifica la IP y puerto al iniciar
