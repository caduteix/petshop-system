from faker import Faker
from app.database.mini_db import MiniDB
from datetime import date
import random

fake = Faker("pt_BR")

CAMPOS = ["id", "nome", "especie", "raca", "data_nascimento", "id_dono", "deleted"]
db = MiniDB("pets", CAMPOS)

species_breeds = {
    "Cachorro": ["Poodle", "Labrador", "Bulldog", "Pastor Alemão", "Vira-lata"],
    "Gato": ["Siamês", "Persa", "Maine Coon", "Angorá", "SRD"],
    "Pássaro": ["Calopsita", "Canário", "Papagaio", "Periquito"],
    "Coelho": ["Mini Rex", "Lion Head", "Holland Lop", "Angorá Inglês"],
}

for _ in range(1000):
    especie = random.choice(list(species_breeds.keys()))
    raca = random.choice(species_breeds[especie])
    nascimento = fake.date_between(start_date="-15y", end_date="today")

    pet = {
        "nome": fake.first_name(),
        "especie": especie,
        "raca": raca,
        "data_nascimento": nascimento.isoformat(),
        "id_dono": fake.name(),
    }

    db.insert(pet)

print(f"Banco de dados populado com sucesso (1000 pets) em '{db.arquivo}'")
