import os

class Sequencia: 
    """Gerenciar o arquivo seq"""

    def __init__(self, filename: str):
        self.filename = filename if filename.endswith(".seq") else f"{filename}.seq"

        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write("0")
    
    def next_id(self) -> int:
        """Ver o último ID, incrementa e salva o valor"""
        with open(self.filename, "r+", encoding="utf-8") as f:
            valor_atual = int(f.read().strip() or 0)
            novo_valor = valor_atual + 1
            f.seek(0)
            f.write(str(novo_valor))
            f.truncate()
        return novo_valor