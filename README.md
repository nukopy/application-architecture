# Application Architecture

Implementation examples of various application architetures with Python/TypeScript.

- Structure of Application
- Architecture List
  - Backend
  - Frontend
- Build & Start up application

## Structure of Application

- backend
  - Python
    - Web Framework: FastAPI
    - ORM: SQLAlchemy
- frontend
  - TypeScript
    - Framework: React

---

## Architecture List

- backend
  - MVC
    - いろんな亜種
  - MVVM
  - Layered Architecture
  - Clean Architecture
- frontend
  - MVC
  - MVVM
  - Flux

### Backend

For development backend API, use following Python packages:

- FastAPI
- mypy
  - static type check in Python
- pydantic
  - type check, or data validation "at runtime" in Python
  - enforce type hints "at runtime" and user friendly erros when data is invalid

### Frontend

Base source code is implemented with TypeScript/React.

---

## Build & Start up application

Start containers

```sh
$ make build
$ make up
```

You can see containers in `docker-compose.yml`.

- containers
  - Backend
    - `nginx`
    - `app`
    - `db(MySQL)`
  - Frontend
    - `frontend`
