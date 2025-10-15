from datetime import date
from typing import List, Optional
import csv

from app.database.mini_db import MiniDB
from app.entities.models import Pet

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
                    linha["data_nascimento"] = date.fromisoformat(linha["data_nascimento"])
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
        pet_id = db.insert(pet_dict)
        pet_dict["id"] = pet_id
        return Pet(**pet_dict)

    @staticmethod
    def atualizar_pet(id_: int, novos_dados: Pet) -> Optional[Pet]:
        dados_dict = novos_dados.dict(exclude_unset=True)
        atualizado = db.update(id_, dados_dict)
        if not atualizado:
            return None
        pet_atualizado = db.get(id_)
        pet_atualizado["id"] = int(pet_atualizado["id"])
        pet_atualizado["data_nascimento"] = date.fromisoformat(pet_atualizado["data_nascimento"])
        return Pet(**pet_atualizado)

    @staticmethod
    def deletar_pet(id_: int) -> bool:
        return db.delete(id_)

    @staticmethod
    def compactar_banco() -> None:
        db.vacuum()
