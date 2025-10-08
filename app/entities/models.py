from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Pet(BaseModel):
    id: Optional[int] = None
    nome: str = Field(..., example = "Snoopy")
    especie: str = Field(..., example = "Cachorro")
    raca: str = Field(..., example = "Poodle")
    data_nascimento: date = Field(..., example = date(2016, 2, 31))
    id_dono: str = Field(..., example = "12345678900")
    deleted: Optional[bool] = False ## Deleção lógica (Soft Delete)