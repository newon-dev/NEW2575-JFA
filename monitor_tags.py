from rfid import RF600XML
import time

def monitorar_tags():
    # Definir os leitores com IPs diferentes
    leitores = [
        RF600XML(port=10001, host="10.0.0.10"),
        RF600XML(port=10001, host="10.0.0.11")
    ]
    
    try:
        while True:
            for i, leitor in enumerate(leitores):
                tag = leitor.ler_tag()
                if tag:
                    print(f"Leitor {i+1} (IP: {leitor.host}) - Tag lida: {tag}")
            
            time.sleep(0.5)  # Aguarda um tempo antes de ler novamente
    except KeyboardInterrupt:
        print("\nEncerrando monitoramento...")
        for leitor in leitores:
            leitor.stop()
            leitor.client_socket.close()
        print("Conexões fechadas com sucesso.")

if __name__ == "__main__":
    monitorar_tags()
