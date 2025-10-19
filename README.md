# Projeto Petshop - Sistema de Gerenciamento com FastAPI

## 🎯 Objetivo do Projeto

Este projeto consiste em um sistema de gerenciamento para petshops. O sistema permite cadastrar, listar, atualizar, remover (soft delete) e gerenciar pets, clientes e serviços, utilizando **FastAPI** e persistência de dados em **arquivos CSV**.

---

## 🧰 Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI**
* **Uvicorn** (servidor ASGI)
* **Pydantic**
* **CSV como banco de dados**
* **Swagger UI** para documentação automática

---

## 🔧 Como Executar o Projeto

### 1️⃣ Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd petshop-system
```

### 2️⃣ Criar e Ativar Ambiente Virtual

```bash
python -m venv .venv
```

#### Ativar no Windows:

```bash
.venv\Scripts\activate
```

#### Ativar no Linux/Mac:

```bash
source .venv/bin/activate
```

### 3️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Executar a API

```bash
uvicorn main:app --reload
```

### 5️⃣ Acessar Documentação da API

* ➤ Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Testando no Swagger

1. Acesse `/docs`
2. Escolha um endpoint
3. Clique em **Try it out**
4. Preencha os dados e clique em **Execute**


## 📌 Observações Importantes

* O campo `deleted` é utilizado para Soft Delete, conforme exigência da disciplina
* O método `PUT` aceita requisições utilizando `PetUpdate`, permitindo atualização parcial
