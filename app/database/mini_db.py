import csv
import os
from typing import Dict, List, Optional
from .sequencer import Sequencia


class MiniDB:
    def __init__(self, nome_arquivo: str, campos: List[str]):
        self.arquivo = (
            nome_arquivo if nome_arquivo.endswith(".csv") else f"{nome_arquivo}.csv"
        )
        self.seq = Sequencia(nome_arquivo)
        self.campos = campos

        if not os.path.exists(self.arquivo):
            with open(self.arquivo, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.campos)
                writer.writeheader()

    def insert(self, dados: Dict) -> int:
        dados["id"] = self.seq.next_id()
        # padronizar como string (evita tipo misto)
        dados["deleted"] = "False"

        with open(self.arquivo, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.campos)
            writer.writerow(dados)

        return dados["id"]

    def get(self, id_: int) -> Optional[Dict]:
        with open(self.arquivo, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for line in reader:
                if int(line["id"]) == id_ and line["deleted"] == "False":
                    return line
        return None

    def update(self, id_: int, novos_dados: Dict) -> bool:
        atualizado = False
        temp = self.arquivo + ".tmp"

        with (
            open(self.arquivo, "r", newline="", encoding="utf-8") as entrada,
            open(temp, "w", newline="", encoding="utf-8") as saida,
        ):
            reader = csv.DictReader(entrada)
            writer = csv.DictWriter(saida, fieldnames=self.campos)
            writer.writeheader()

            for linha in reader:
                if int(linha["id"]) == id_ and linha["deleted"] == "False":
                    # atualiza apenas campos válidos
                    for k, v in novos_dados.items():
                        if k in self.campos and k not in ["id", "deleted"]:
                            linha[k] = v
                    atualizado = True
                writer.writerow(linha)

        os.replace(temp, self.arquivo)
        return atualizado

    def delete(self, id_: int) -> bool:
        deletado = False
        temp = self.arquivo + ".tmp"

        with (
            open(self.arquivo, "r", newline="", encoding="utf-8") as entrada,
            open(temp, "w", newline="", encoding="utf-8") as saida,
        ):
            reader = csv.DictReader(entrada)
            writer = csv.DictWriter(saida, fieldnames=self.campos)
            writer.writeheader()

            for linha in reader:
                if int(linha["id"]) == id_ and linha["deleted"] == "False":
                    linha["deleted"] = "True"
                    deletado = True
                writer.writerow(linha)

        os.replace(temp, self.arquivo)
        return deletado

    def count(self) -> int:
        total = 0
        with open(self.arquivo, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for linha in reader:
                if linha["deleted"] == "False":
                    total += 1
        return total

    def vacuum(self):
        temp = self.arquivo + ".vacuum"

        with (
            open(self.arquivo, "r", newline="", encoding="utf-8") as entrada,
            open(temp, "w", newline="", encoding="utf-8") as saida,
        ):
            reader = csv.DictReader(entrada)
            writer = csv.DictWriter(saida, fieldnames=self.campos)
            writer.writeheader()

            for linha in reader:
                if linha["deleted"] == "False":
                    writer.writerow(linha)

        os.replace(temp, self.arquivo)
