

# Projeto Pet Kare

O projeto `Pet Kare` é uma aplicação de gerenciamento de informações sobre animais de estimação, grupos de animais e características dos pets. Ele fornece uma plataforma para cadastrar, visualizar, atualizar e filtrar informações sobre os animais, bem como associar grupos e características aos pets.

### Tecnologias utilizadas

![Badge](https://img.shields.io/badge/Python-3.11.5-green.svg)
![Badge](https://img.shields.io/badge/Django-4.2.6-blue)
![Badge](https://img.shields.io/badge/djangorestframework-3.14.0-orange)

## Índice

1. [Estrutura Básica e Modelagem com DER](#estrutura-básica-e-modelagem-com-der)
2. [Serializers](#serializers)
3. [Rotas e Filtros](#rotas-e-filtros)
4. [Finalizando Rotas](#finalizando-rotas)

## Estrutura Básica e Modelagem com DER

Nesta etapa, desenvolvemos o Diagrama de Entidade Relacionamento (DER) e as models da aplicação. Foram criados três apps: `pets`, `groups` e `traits`, com três models principais: `Pet`, `Group`, e `Trait`. As models seguem as especificações abaixo:

### Model `Pet`

- `name`: string, máximo de 50 caracteres.
- `age`: inteiro.
- `weight`: ponto flutuante.
- `sex`: string, máximo de 20 caracteres, com opções "Male," "Female," e "Not Informed" (valor padrão).
- `group`: relacionamento com a model `Group`.
- `traits`: relacionamento com a model `Trait`.

### Model `Group`

- `scientific_name`: string, máximo de 50 caracteres, único.
- `created_at`: data e hora, preenchida automaticamente na criação.

### Model `Trait`

- `name`: string, máximo de 20 caracteres, único.
- `created_at`: data e hora, preenchida automaticamente na criação.

## Serializers

Nesta etapa, foram criados os serializadores para as models, garantindo consistência nas operações de entrada e saída de dados. Os serializadores seguem as seguintes regras:

### Serializador de `Pet`

- Campos de entrada e saída: `name`, `age`, `weight`, `sex`, `group` (serializador aninhado) e `traits` (serializador aninhado).
- Campos somente de entrada: Nenhum.
- Campos somente de saída: `id`.

### Serializador de `Group`

- Campos de entrada e saída: `scientific_name`.
- Campos somente de entrada: Nenhum.
- Campos somente de saída: `id` e `created_at`.

### Serializador de `Trait`

- Campos de entrada e saída: `trait_name`.
- Campos somente de entrada: Nenhum.
- Campos somente de saída: `id` e `created_at`.

## Rotas e Filtros

As rotas e filtros foram definidos para interagir com os recursos da aplicação:

- **Cadastrar pets**: `POST /api/pets/`
  - Corpo da Requisição:
    ```json
    {
      "name": "Nome do Pet",
      "age": 2,
      "weight": 5.5,
      "sex": "Male",
      "group": {"scientific_name": "Nome Científico do Grupo"},
      "traits": [{"trait_name": "Característica 1"}, {"trait_name": "Característica 2"}]
    }
    ```
  - Corpo da Resposta (Status 201 CREATED):
    ```json
    {
      "id": 1,
      "name": "Nome do Pet",
      "age": 2,
      "weight": 5.5,
      "sex": "Male",
      "group": {
        "id": 1,
        "scientific_name": "Nome Científico do Grupo",
        "created_at": "2023-10-10T10:00:00Z"
      },
      "traits": [
        {"id": 1, "trait_name": "Característica 1", "created_at": "2023-10-10T10:01:00Z"},
        {"id": 2, "trait_name": "Característica 2", "created_at": "2023-10-10T10:02:00Z"}
      ]
    }
    ```

- **Listar pets (com paginação)**: `GET /api/pets/`
  - Corpo da Resposta (Status 200 OK):
    
    ```json
    {
      "count": 8,
      "next": "http://localhost:8000/api/pets/?page=2",
      "previous": null,
      "results": [
        // Lista de pets
      ]
    }
    ```

- **Buscar pet por ID**: `GET /api/pets/{pet_id}/`
  - Corpo da Resposta (Status 200 OK):
    ```json
    {
      // Detalhes do pet
    }
    ```

- **Excluir pet por ID**: `DELETE /api/pets/{pet_id}/`
  - Corpo da Resposta (Status 204 NO CONTENT).

- **Atualizar dados do pet por ID**: `PATCH /api/pets/{pet_id}/`
  - Corpo da Requisição (campos opcionais):
    ```json
    {
      "name": "Novo Nome do Pet",
      "age": 3,
      "sex": "Female",
      "group": {"scientific_name": "Novo Nome Científico do Grupo"},
      "traits": [{"trait_name": "Nova Característica"}]
    }
    ```

- **Filtragem de pets por característica**: `GET /api/pets/?trait=nome_da_trait`
  - Corpo da Resposta (Status 200 OK):
    ```json
    {
      "count": 4,
      "next": "http://localhost:8000/api/pets/?page=2",
      "previous": null,
      "results": [
        // Lista de pets com a característica especificada
      ]
    }
    ```

## Finalizando Rotas

As rotas finais foram implementadas de acordo com as seguintes regras de negócio:

- Todos os campos na requisição de atualização são opcionais.
- Os campos `group` e `traits` devem seguir as regras de reutilização de dados existentes para evitar duplicações.
- A busca por ID, exclusão e atualização de pet não existente retornam um status 404 NOT FOUND.



---
---

### Preparando ambiente para execução dos testes

1. Verifique se os pacotes **pytest**, **pytest-testdox** e/ou **pytest-django** estão instalados globalmente em seu sistema:
```shell
pip list
```

2. Caso eles apareçam na listagem, rode os comandos abaixo para realizar a desinstalação:

```shell
pip uninstall pytest pytest-testdox pytest-django -y
```
3. Após isso, crie seu ambiente virtual:
```shell
python -m venv venv
```

4. Ative seu ambiente virtual:

```shell
# Linux e Mac:
source venv/bin/activate

# Windows (PowerShell):
.\venv\Scripts\activate


# Windows (GitBash):
source venv/Scripts/activate
```

5. Instale as bibliotecas necessárias:

```shell
pip install pytest-testdox pytest-django
```
 

## Para executar `TODOS` os testes:
```shell
pytest --testdox -vvs
```

---
---