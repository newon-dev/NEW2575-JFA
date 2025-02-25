import subprocess
import time
import threading
import signal
import logging
from pathlib import Path


""""Definir o nome do arquivo de logs a ser usado, por padrão será usado NewOnDaemonLogs"""
LOG_FILE = "NewonDaemonLogs.log"


class ScriptMonitor:
    """
    Módulo Newon responsável por executar e acomapnhar execução de um código de forma contínua. Daemon
    :param: Scripts array contendo strings com os nomes dos scripts a serem executados.
    """

    def __init__(self, scripts: list, MAX_ATTEMPTS=3, TIME_WINDOW=300) -> None:
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.scripts = scripts
        self.attempts = {script: {"count": 0, "last_failure": 0} for script in scripts}
        self.processes = {}
        self.MAX_ATTEMPTS = MAX_ATTEMPTS
        self.TIME_WINDOW = TIME_WINDOW
        self.stop_event = threading.Event()
        signal.signal(signal.SIGINT, self.handle_exit)

    def handle_exit(self, signum: None, frame: None) -> None:
        """
        Responsável por realizar o encerramento do processo, e loggin do fechamento
        """
        logging.info("Monitoramento interrompido pelo usuário.")
        print("Monitoramento interrompido pelo usuário.")
        self.stop_event.set()

    def run_script(self, script: str) -> None:
        """
        Responsável por realizar a execução do script
        :param: Script String contento o nome do arquivo. Deve estar na mesma pasta.
        """
        script_path = Path(__file__).parent / script
        if not script_path.exists():
            logging.error(f"Arquivo {script} não encontrado!")
            print(f"Erro: Arquivo {script} não encontrado!")
            return

        while self.attempts[script]["count"] < self.MAX_ATTEMPTS:
            if self.stop_event.is_set():
                return

            try:
                logging.info(f"Iniciando {script}...")
                print(f"Iniciando {script}...")
                process = subprocess.Popen(
                    ["python", str(script_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                self.processes[script] = process
                process.wait()

                logging.error(f"{script} falhou.")
                print(f"{script} falhou.")
                self.attempts[script]["count"] += 1
                self.attempts[script]["last_failure"] = time.time()

                if self.attempts[script]["count"] >= self.MAX_ATTEMPTS:
                    current_time = time.time()
                    if (
                        current_time - self.attempts[script]["last_failure"]
                        <= self.TIME_WINDOW
                    ):
                        logging.error(
                            f"{script} falhou {self.MAX_ATTEMPTS} vezes em {self.TIME_WINDOW} segundos. Parando..."
                        )
                        print(
                            f"Erro: {script} falhou {self.MAX_ATTEMPTS} vezes em {self.TIME_WINDOW} segundos. Parando..."
                        )
                        return
                    else:
                        self.attempts[script]["count"] = 0

            except Exception as e:
                logging.error(f"Erro ao executar {script}: {e}")
                print(f"Erro ao executar {script}: {e}")

            time.sleep(2)

    def start_monitoring(self) -> None:
        """
        Responsável por iniciar o monitoramento dos processos utilizados
        """
        threads = []
        for script in self.scripts:
            thread = threading.Thread(
                target=self.run_script, args=(script,), daemon=True
            )
            threads.append(thread)
            thread.start()

        try:
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            self.handle_exit(None, None)


if __name__ == "__main__":
    scripts = ["track_new.py", "api.py"]
    monitor = ScriptMonitor(scripts)
    monitor.start_monitoring()
