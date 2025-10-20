from datetime import date
from typing import List, Optional
import csv
import zipfile
import io
import hashlib
from fastapi.responses import StreamingResponse

from app.database.mini_db import MiniDB
from app.entities.models import Pet, PetPatch

CAMPOS = ["id", "nome", "especie", "raca", "data_nascimento", "id_dono", "deleted"]
db = MiniDB("pets", CAMPOS)


class PetService:
    @staticmethod
    def listar_pets() -> List[Pet]:
        pets = []
        with open(db.arquivo, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for linha in reader:
                if linha["deleted"] == "False":
                    linha["id"] = int(linha["id"])
                    linha["deleted"] = False
                    linha["data_nascimento"] = date.fromisoformat(
                        linha["data_nascimento"]
                    )
                    pets.append(Pet(**linha))
        return pets

    @staticmethod
    def buscar_pet(id_: int) -> Optional[Pet]:
        pet = db.get(id_)
        if pet and pet["deleted"] == "False":
            pet["id"] = int(pet["id"])
            pet["deleted"] = False
            pet["data_nascimento"] = date.fromisoformat(pet["data_nascimento"])
            return Pet(**pet)
        return None

    @staticmethod
    def criar_pet(pet: Pet) -> Pet:
        pet_dict = pet.dict(exclude_unset=True)
        # garantir que deleted seja string no CSV
        pet_dict["deleted"] = "False"
        pet_id = db.insert(pet_dict)
        pet_dict["id"] = pet_id
        pet_dict["deleted"] = False
        return Pet(**pet_dict)

    @staticmethod
    def atualizar_pet(id_: int, novos_dados: dict):
        if not novos_dados:
            return None
        atualizado = db.update(id_, novos_dados)
        if not atualizado:
            return None
        pet_atualizado = db.get(id_)
        pet_atualizado["id"] = int(pet_atualizado["id"])
        pet_atualizado["data_nascimento"] = date.fromisoformat(
            pet_atualizado["data_nascimento"]
        )
        pet_atualizado["deleted"] = pet_atualizado["deleted"] == "True"
        return Pet(**pet_atualizado)

    @staticmethod
    def atualizar_pet_parcial(id_: int, campos: PetPatch) -> Optional[Pet]:
        dados_atualizar = campos.dict(exclude_unset=True)

        if not dados_atualizar:
            return None  # Nenhum campo informado

        atualizado = db.update(id_, dados_atualizar)
        if not atualizado:
            return None

        # Retorna o objeto atualizado
        pet_atualizado = db.get(id_)
        if pet_atualizado:
            pet_atualizado["id"] = int(pet_atualizado["id"])
            pet_atualizado["data_nascimento"] = date.fromisoformat(
                pet_atualizado["data_nascimento"]
            )
            pet_atualizado["deleted"] = pet_atualizado["deleted"] == "True"
            return Pet(**pet_atualizado)

        return None

    @staticmethod
    def deletar_pet(id_: int) -> bool:
        return db.delete(id_)

    @staticmethod
    def compactar_banco() -> None:
        db.vacuum()

    @staticmethod
    def listar_pets_paginado(page: int, size: int) -> List[Pet]:
        pets = []
        start = (page - 1) * size
        end = start + size
        count = 0

        with open(db.arquivo, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for linha in reader:
                if linha["deleted"] == "False":
                    if count >= start and count < end:
                        linha["id"] = int(linha["id"])
                        linha["deleted"] = False
                        linha["data_nascimento"] = date.fromisoformat(
                            linha["data_nascimento"]
                        )
                        pets.append(Pet(**linha))
                    count += 1
                    if count >= end:
                        break
        return pets

    @staticmethod
    def contar_pets() -> int:
        return db.count()

    @staticmethod
    def exportar_zip_streaming():
        def generator():
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                with zip_file.open("pets.csv", "w") as csv_file:
                    csv_file.write(",".join(CAMPOS).encode("utf-8") + b"\n")
                    with open(db.arquivo, "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for linha in reader:
                            if linha["deleted"] == "False":
                                valores = [linha[campo] for campo in CAMPOS]
                                csv_file.write(
                                    ",".join(valores).encode("utf-8") + b"\n"
                                )

            buffer.seek(0)
            yield from buffer

        return StreamingResponse(
            generator(),
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=pets.zip"},
        )

    @staticmethod
    def gerar_hash(dado: str, algoritmo: str) -> str:
        algoritmo = algoritmo.lower()
        if algoritmo == "md5":
            h = hashlib.md5()
        elif algoritmo == "sha1":
            h = hashlib.sha1()
        elif algoritmo == "sha256":
            h = hashlib.sha256()
        else:
            raise ValueError("Algoritmo inválido. Use: MD5, SHA1 ou SHA256.")

        h.update(dado.encode("utf-8"))
        return h.hexdigest()
