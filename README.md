# 🚀 Portfólio Profissional — Full Stack & Mobile

Aplicação de portfólio moderna e interativa construída com **Nuxt 3 (Vue 3)**, **GSAP**, **Tailwind CSS** no Frontend e **FastAPI** com **PostgreSQL no Neon** no Backend. Arquivos (foto, currículos) ficam no próprio banco e são servidos pela API em `/files/...`.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:
- [Node.js](https://nodejs.org/) (versão `18.x` ou superior)
- [Python](https://www.python.org/) (versão `3.10` ou superior)
- [uv](https://github.com/astral-sh/uv) *(opcional, mas recomendado para gerenciamento do ambiente Python)*

---

## ⚡ Passo a Passo Rápido: Rodando o Frontend (Nuxt 3)

1. **Acesse a pasta do Frontend:**
   ```bash
   cd Frontend
   ```

2. **Instale as dependências:**
   ```bash
   npm install
   ```

3. **Inicie o servidor de desenvolvimento:**
   ```bash
   npm run dev
   ```

4. **Acesse no navegador:**
   👉 `http://localhost:3000`

---

## 🐍 Passo a Passo Rápido: Rodando o Backend (FastAPI)

1. **Configure o `.env`** (copie o `.env.example` e preencha) e crie/atualize as tabelas:
   ```bash
   uv run alembic upgrade head
   ```

2. **Na raiz do projeto, inicie o ambiente virtual e execute o servidor:**
   Com `uv`:
   ```bash
   uv run python -m uvicorn main:app --reload
   ```
   *(Ou ative o seu ambiente virtual `.venv` e rode `uvicorn main:app --reload`)*

3. **Acesse a API e Documentação Interativa:**
   - **API Root**: `http://127.0.0.1:8000`
   - **Swagger Docs**: `http://127.0.0.1:8000/docs`

> Mudou algum Model? Gere a migração com `uv run alembic revision --autogenerate -m "descrição"`, revise o arquivo gerado em `migrations/versions/` e rode `uv run alembic upgrade head`.

---

## 🔐 Login do /admin

O site é de um usuário só. Só o e-mail definido em `ADMIN_EMAIL` (no `.env` do backend) recebe o código de 6 dígitos; qualquer outro e-mail recebe a mesma resposta, mas nenhum código. Sem `SMTP_USER`/`SMTP_PASSWORD` configurados, o código aparece no terminal do backend em vez de ir por e-mail.

---

## 🚚 Migração Supabase → Neon (uma vez só)

1. **Reative o Supabase** (Dashboard → seu projeto → *Restore project*), só pra conseguir tirar os dados de lá.
2. **Crie o banco no Neon** em [neon.tech](https://neon.tech) (região mais próxima, ex: São Paulo). Em *Connect*, ative *Connection pooling* e copie a URL. Coloque no `.env` como `DATABASE_URL`, mas guarde a URL antiga do Supabase (ela está no `DATABASE_URL` atual).
3. **Crie as tabelas no Neon:** `uv run alembic upgrade head`
4. **Copie os dados:** `uv run python -m scripts.copy_database "<URL antiga do Supabase>"`. Ele copia tabela por tabela e confere se a contagem de linhas bate. Teste antes com `--dry-run`, se quiser.
5. **Traga os arquivos pro banco:** `uv run python -m scripts.migrate_storage --dry-run` (lista os arquivos) e depois sem `--dry-run`. Ele baixa cada arquivo do Supabase Storage, salva no Neon e troca as URLs.
6. **Defina `ADMIN_EMAIL`** no `.env` e teste o login em `/admin/login`. Depois disso o Supabase pode ser apagado.

---

## 🛠️ Outros Comandos Úteis do Frontend

| Comando | Descrição |
| :--- | :--- |
| `npm run dev` | Inicia o servidor de desenvolvimento na porta `3000` |
| `npm run build` | Compila a aplicação para produção em `.output` |
| `npm run preview` | Testa o build de produção localmente |

---

## 📁 Estrutura das Pastas

```text
Portfolio/
├── Core/               # Conexão com o banco, sessão e segurança
├── Models/             # Modelos SQLAlchemy da base de dados
├── Routes/             # Rotas REST da FastAPI (projects, skills, etc.)
├── Schemas/            # Schemas Pydantic para validação de dados
├── Services/           # Camada de regras de negócio
├── migrations/         # Migrações do banco (Alembic)
├── scripts/            # Scripts de uso único (cópia do banco, migração dos arquivos)
├── main.py             # Ponto de entrada da API FastAPI
│
└── Frontend/           # Aplicação Nuxt 3 (Vue 3)
    ├── assets/css/     # Design System e estilos globais Tailwind
    ├── components/     # Componentes Vue 3 reutilizáveis (GlowCard, Orbit, etc.)
    ├── composables/    # Logica de estado e consumo de API (usePortfolioApi, useGsap)
    ├── layouts/        # Layout base da aplicação (default.vue)
    ├── pages/          # Rotas Nuxt (index.vue, work.vue, resume.vue)
    └── plugins/        # Efeitos de cliente (Starfield, Cursor Glow, ScrollSpy)
```