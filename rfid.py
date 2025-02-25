import socket
import time
import datetime
import os
import platform


client_ip = "10.0.0.10"
port = 10001


class RF600XML:
    timeout = 2
    ciclo_teste = 15

    def __init__(self, port, host):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(1.0)
        self.port = port
        self.host = host
        self.id = 1
        self.connected = False

        self.greet = [
            "<frame><cmd><id>",
            "</id><hostGreetings><readerType></readerType>"
            "<supportedVersions><version>V2.0</version><version>V2.1</version>"
            "<version>V2.2</version><version>V3.0</version><version>V3.1</version>"
            "<version>V3.2</version></supportedVersions></hostGreetings></cmd></frame>",
        ]
        self.start_stop = [
            "<frame><cmd><id>",
            "</id><triggerSource><sourceName>",
            "</sourceName><triggerMode>",
            "</triggerMode></triggerSource></cmd></frame>",
        ]

        self.connect()

    def ping_antenna(host):
        try:
            sistema = platform.system().lower()
            comando = "ping -n 1" if sistema == "windows" else "ping -c 1"
            resposta = os.system(f"{comando} {host}")
            if resposta == 0:
                return True
            else:
                return False

        except Exception as e:
            return False

    def connect(self):
        """Tenta conectar ao leitor RFID e verificar resposta."""
        try:

            self.client_socket.connect((self.host, self.port))
            self.client_socket.setblocking(0)

            # Envia saudação inicial
            message = self.greet[0] + str(self.id) + self.greet[1]
            self.id += 1
            self.client_socket.send(message.encode("ascii"))
            time.sleep(0.5)

            resposta = self.aguarda_resposta()
            if resposta == "Sem resposta":
                self.client_socket.close()
                return

            self.connected = True
            self.start()

        except Exception as e:
            self.connected = False

    def start(self):
        """Envia comando para iniciar leitura."""
        if not self.connected:
            self.connect()
            return

        message = (
            self.start_stop[0]
            + str(self.id)
            + self.start_stop[1]
            + "Readpoint_1"
            + self.start_stop[2]
            + "Start"
            + self.start_stop[3]
        )
        self.id += 1
        self.client_socket.send(message.encode("ascii"))
        time.sleep(0.5)

        resposta = self.aguarda_resposta()
        if resposta == "Sem resposta":
            pass

    def stop(self):
        """Envia comando para parar leitura."""
        if not self.connected:
            return

        message = (
            self.start_stop[0]
            + str(self.id)
            + self.start_stop[1]
            + "Readpoint_1"
            + self.start_stop[2]
            + "Stop"
            + self.start_stop[3]
        )
        self.id += 1
        self.client_socket.send(message.encode("ascii"))
        time.sleep(0.2)

    def aguarda_resposta(self):
        """Aguarda resposta do leitor."""
        init_time = time.time()
        mensagem = ""

        while time.time() - init_time <= RF600XML.timeout:
            try:
                data = self.client_socket.recv(1)
                if data:
                    init_time = time.time()
                    mensagem += data.decode("ascii")
                    if "</frame>" in mensagem:
                        return mensagem
            except socket.timeout:
                break
            except Exception as e:
                break

        return "Sem resposta"

    def ler_tag(self):
        """Tenta ler uma tag e retorna o ID dela."""
        if not self.connected:
            self.connect()
            return None

        data = self.aguarda_resposta()
        if data == "Sem resposta":
            return None

        try:
            tag = data.split("<tagID>")[1].split("</tagID>")[0]
            return tag
        except IndexError:
            return None


if __name__ == "__main__":
    leitor = RF600XML(port, client_ip)
    while True:
        try:
            tag = leitor.ler_tag()
            if tag:
                print(f"Tag lida: {tag}")
        except KeyboardInterrupt:
            print("\nEncerrando conexão...")
            leitor.stop()
            leitor.client_socket.close()
            print("Conexão fechada com sucesso.")
