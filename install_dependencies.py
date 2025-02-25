import os
import subprocess
import sys

class VirtualEnvManager:
    """
    Uso: python install_dependencies.py nome_do_ambiente_virtual, ele usa o arquivo requirements.txt para instalar as 
    dependências.
    """
    def __init__(self, venv_name):
        self.venv_name = venv_name
        self.pip_path = None
        self.activate_path = None
        self._set_paths()

    def _set_paths(self):
        if os.name == "nt":  # Windows
            self.pip_path = os.path.join(self.venv_name, "Scripts", "pip")
            self.activate_path = os.path.join(self.venv_name, "Scripts", "activate")
        else:  # Linux/macOS
            self.pip_path = os.path.join(self.venv_name, "bin", "pip")
            self.activate_path = os.path.join(self.venv_name, "bin", "activate")
    
    def create_venv(self):
        subprocess.run([sys.executable, "-m", "venv", self.venv_name])
    
    def install_dependencies(self):
        subprocess.run([self.pip_path, "install", "-r", "requirements.txt"])
    
    def display_instructions(self):
        activation_cmd = f"source {self.activate_path}" if os.name != "nt" else f"{self.activate_path}.bat"
        print(f"Ambiente virtual '{self.venv_name}' criado e dependências instaladas.")
        print(f"Para ativar o ambiente, use:\n{activation_cmd}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Para executar utilize python install_dependencies.py (Nome do ambiente virtual)")
        sys.exit(1)
    
    venv_name = sys.argv[1]
    manager = VirtualEnvManager(venv_name)
    manager.create_venv()
    manager.install_dependencies()
    manager.display_instructions()
