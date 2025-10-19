from fastapi import FastAPI, HTTPException
from typing import List

from app.entities.models import Pet, PetUpdate, HashRequest
from app.services.pet_service import PetService

app = FastAPI(
    title="PetShop System",
    description="API REST para gerenciamento de um PetShop com persistência em CSV.",
)


# Direciona à Home
@app.get("/", tags=["Home"])
def read_root():
    return {"mensagem": "Bem-vindo à API de Pets!"}


# Lista todos os pets
@app.get(
    "/pets/all",
    response_model=List[Pet],
    tags=["Pets"],
    summary="Listar todos os pets",
)
def listar_pets():
    return PetService.listar_pets()


# Paginação dos Pets
@app.get(
    "/pets/page",
    response_model=List[Pet],
    tags=["Pets"],
    summary="Listar pets paginados",
)
def listar_pets_paginado(page: int = 1, size: int = 10):
    if page < 1 or size < 1:
        raise HTTPException(
            status_code=400, detail="Parâmetros page e size devem ser positivos."
        )

    pets = PetService.listar_pets_paginado(page, size)
    if not pets:
        raise HTTPException(
            status_code=404, detail="Nenhum pet encontrado para esta página."
        )
    return pets


# Contar quantos pets existem (Número)
@app.get(
    "/pets/count", tags=["Estatísticas"], summary="Retorna o total de pets armazenados"
)
def contar_pets():
    total = PetService.contar_pets()
    return {"total_pets": total}


# Exporta para o ZIP
@app.get("/pets/export", tags=["Pets"], summary="Exportar pets ativos em formato ZIP")
def exportar_pets_zip():
    return PetService.exportar_zip_streaming()


# Busca um pet em específico pelo ID
@app.get(
    "/pets/{pet_id}", response_model=Pet, tags=["Pets"], summary="Buscar pet por ID"
)
def buscar_pet(pet_id: int):
    pet = PetService.buscar_pet(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return pet


# Cria novo pet
@app.post("/pets/", response_model=Pet, tags=["Pets"], summary="Criar novo pet")
def criar_pet(pet: Pet):
    return PetService.criar_pet(pet)


# Atualiza informações do Pet
@app.put(
    "/pets/{pet_id}",
    response_model=Pet,
    tags=["Pets"],
    summary="Atualizar informações de um pet",
)
def atualizar_pet(pet_id: int, novos_dados: PetUpdate):
    pet_atualizado = PetService.atualizar_pet(
        pet_id, novos_dados.dict(exclude_unset=True)
    )
    if not pet_atualizado:
        raise HTTPException(
            status_code=404, detail="Pet não encontrado para atualização"
        )
    return pet_atualizado


# Deleta o pet
@app.delete("/pets/{pet_id}", tags=["Pets"], summary="Excluir um pet")
def deletar_pet(pet_id: int):
    deletado = PetService.deletar_pet(pet_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Pet não encontrado para deleção")
    return {"mensagem": f"Pet {pet_id} deletado com sucesso"}


# Remove os deletados
@app.post("/pets/vacuum", tags=["Pets"], summary="Compactar banco (remover deletados)")
def compactar_banco():
    PetService.compactar_banco()
    return {"mensagem": "Banco compactado com sucesso"}


# Gera o hash para o dado enviado
@app.post(
    "/hash", tags=["Utilidades"], summary="Gerar hash (MD5, SHA1 ou SHA256) de um dado"
)
def gerar_hash(request: HashRequest):
    try:
        resultado = PetService.gerar_hash(request.dado, request.algoritmo)
        return {"hash": resultado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
