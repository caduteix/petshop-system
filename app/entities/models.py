from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Pet(BaseModel):
    id: Optional[int] = None
    nome: str = Field(..., example = "Snoopy")
    especie: str = Field(..., example = "Cachorro")
    raca: str = Field(..., example = "Poodle")
    data_nascimento: date = Field(..., example = date(2016, 2, 28))
    id_dono: str = Field(..., example = "12345678900")
    deleted: Optional[bool] = False ## Deleção lógica (Soft Delete)
    
class PetUpdate(BaseModel):
    nome: Optional[str] = None
    especie: Optional[str] = None
    raca: Optional[str] = None
    data_nascimento: Optional[date] = None
    id_dono: Optional[str] = None
    deleted: Optional[bool] = False
    
class HashRequest(BaseModel):
    dado: str
    algoritmo: str = Field(..., example="MD5")
