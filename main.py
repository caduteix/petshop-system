from fastapi import FastAPI, HTTPException
from typing import List

from app.entities.models import Pet
from app.services.pet_service import PetService

app = FastAPI(title="PetShop System", description="macbook air m2")

# ------------------- ROTAS -------------------

@app.get("/", tags=["Home"])
def read_root():
    return {"mensagem": "Bem-vindo à API de Pets!"}

@app.get("/pets/", response_model=List[Pet], tags=["Pets"])
def listar_pets():
    return PetService.listar_pets()

@app.get("/pets/{pet_id}", response_model=Pet, tags=["Pets"])
def buscar_pet(pet_id: int):
    pet = PetService.buscar_pet(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return pet

@app.post("/pets/", response_model=Pet, tags=["Pets"])
def criar_pet(pet: Pet):
    return PetService.criar_pet(pet)

@app.put("/pets/{pet_id}", response_model=Pet, tags=["Pets"])
def atualizar_pet(pet_id: int, novos_dados: Pet):
    pet_atualizado = PetService.atualizar_pet(pet_id, novos_dados)
    if not pet_atualizado:
        raise HTTPException(status_code=404, detail="Pet não encontrado para atualização")
    return pet_atualizado

@app.delete("/pets/{pet_id}", tags=["Pets"])
def deletar_pet(pet_id: int):
    deletado = PetService.deletar_pet(pet_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Pet não encontrado para deleção")
    return {"mensagem": f"Pet {pet_id} deletado com sucesso"}

@app.post("/pets/vacuum", tags=["Pets"])
def compactar_banco():
    PetService.compactar_banco()
    return {"mensagem": "Banco compactado com sucesso"}
