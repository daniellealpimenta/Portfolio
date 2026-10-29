<div align="center">

# 🗂️ Portfolio API

**O conteúdo do meu portfólio, servido por uma API.**

Backend em FastAPI que guarda projetos, experiências, certificados, habilidades e
recomendações num PostgreSQL (Supabase), e um frontend em HTML/CSS/JS puro que consome essa
API para montar as páginas do portfólio.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2-D71F00?logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2-E92063?logo=pydantic&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-3ECF8E?logo=supabase&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?logo=uv&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-vanilla-F7DF1E?logo=javascript&logoColor=black)

</div>

---

## ✨ O que ele faz

| | |
|---|---|
| 🧩 **8 recursos** | Usuário, projetos, imagens de projeto, ferramentas, habilidades, experiências, certificados e recomendações |
| 🔁 **CRUD completo** | `POST`, `GET`, `PATCH` e `DELETE` para cada recurso (48 rotas) |
| 🏷️ **Filtro por categoria** | `GET /projects/category/{category}` (`Mobile`, `BackEnd`, `GameDev`...) |
| 🔗 **Relacionamentos** | Projeto ↔ ferramentas (N:N via `project_tool`), projeto → imagens, tudo ligado ao usuário |
| ✅ **Validação** | Schemas Pydantic na entrada e na saída; erros de negócio viram `400`/`404` |
| 🕒 **Auditoria** | `created_at` e `updated_at` mantidos por *trigger* no banco |
| 🌐 **Frontend sem build** | Páginas *Home*, *Work* e *Resume* em HTML/JS puro, com dados de exemplo se a API estiver fora |
| 📖 **Docs automáticas** | Swagger em `/docs` e ReDoc em `/redoc` |

## 🧱 Arquitetura

Camadas separadas por responsabilidade: a rota não fala com o banco, e o repositório não conhece
HTTP.

```
Routes/        endpoints FastAPI (um router por recurso)       → HTTP
   ▼
Services/      regras de negócio e erros (HTTPException)      → validações entre recursos
   ▼
Repositories/  acesso a dados com SQLAlchemy                  → queries e commits
   ▼
Models/        tabelas ORM          Schemas/  DTOs Pydantic (Create / Update / Response)
Core/          conexão (engine, SessionLocal, get_db)
schema.sql     DDL completo para o Supabase (tabelas, FKs, triggers)
Frontend/      index.html · work.html · resume.html + js/api.js, ui.js, main.js
```

## 🚀 Primeiros passos

### 1. Banco

Crie um projeto no [Supabase](https://supabase.com) e rode o [`schema.sql`](schema.sql) no
*SQL Editor*.

### 2. Configuração

```bash
cp .env.example .env
# preencha com os parâmetros de conexão do Supabase
```

> [!CAUTION]
> O `.env` tem a senha do banco. Ele já está no `.gitignore`: **nunca o commite**.

### 3. Rodar

```bash
uv sync
uv run uvicorn main:app --reload        # API: http://127.0.0.1:8000/docs
```

Para o frontend, sirva a pasta `Frontend/` (ele aponta para `http://127.0.0.1:8000`):

```bash
cd Frontend && python3 -m http.server 5500   # http://localhost:5500
```

## 🔌 Exemplos

```bash
# listar projetos
curl http://127.0.0.1:8000/projects/

# projetos mobile
curl http://127.0.0.1:8000/projects/category/Mobile

# atualizar só o título
curl -X PATCH http://127.0.0.1:8000/projects/<uuid> \
     -H "Content-Type: application/json" -d '{"title": "Croak"}'
```

## 🗺️ Roadmap

- [x] Modelo de dados e `schema.sql`
- [x] CRUD dos 8 recursos em camadas
- [x] Frontend consumindo a API, com dados de exemplo
- [ ] 🔑 Autenticação (JWT ou API key) nas rotas de escrita
- [ ] Restringir o CORS ao domínio do portfólio
- [ ] Migrações com Alembic no lugar do `create_all`
- [ ] Testes com `pytest` + `TestClient`
- [ ] Deploy (Render / Fly.io) e frontend no GitHub Pages

## 📝 Licença

MIT. Veja [`LICENSE`](LICENSE).
