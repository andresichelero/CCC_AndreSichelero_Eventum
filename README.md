# 🗓️ Eventum

> Plataforma web para gestão de eventos acadêmicos, construída com **Flask** (backend) e **Vue.js** (frontend), utilizando **PostgreSQL** como banco de dados.  
> Este documento reúne tanto a **documentação técnica e operacional** quanto o **relatório de progresso e análise do projeto**.

---

## 📘 Sobre o projeto

O **Eventum** é uma aplicação web que centraliza o gerenciamento de eventos acadêmicos, permitindo que **organizadores**, **palestrantes/autores** e **participantes** interajam em um único sistema.  

A plataforma foi desenvolvida com base em um processo iterativo e incremental, evoluindo de um template básico Flask para uma aplicação completa e funcional, conforme os requisitos estabelecidos no Documento de Visão do Produto (DVP) elaborado.

**Principais objetivos:**
- Automatizar o cadastro, publicação e gerenciamento de eventos.
- Facilitar o processo de inscrição de participantes.
- Oferecer submissão e avaliação de trabalhos acadêmicos.
- Permitir controle de programação com calendário interativo (atividades, palestras, workshops).
- Assegurar conformidade com a **LGPD** (Lei Geral de Proteção de Dados).

---

## 🚀 Funcionalidades Implementadas

| Módulo | Funcionalidades |
|---------|----------------|
| **Autenticação** | Registro, login e logout de usuários com papéis distintos (Organizador, Autor/Palestrante, Participante). Senhas armazenadas com hash seguro (`werkzeug.security`). |
| **Eventos (RF01)** | CRUD completo: criação, edição, visualização e exclusão de eventos. Apenas organizadores têm permissão para gerenciar eventos. |
| **Inscrições (RF02)** | Participantes podem se inscrever em eventos publicados e dentro do período de inscrição. O sistema evita inscrições duplicadas. Organizadores visualizam a lista de participantes. |
| **Submissões de Trabalhos (RF04)** | Autores podem submeter trabalhos com título e resumo; organizadores podem aprovar ou rejeitar submissões. |
| **Programação (RF03)** | Organizadores podem adicionar, editar e gerenciar atividades com calendário interativo (FullCalendar). Participantes visualizam a programação em grade. Suporte a drag-and-drop para reorganizar horários. |
| **Validação de Regras de Negócio** | Período de inscrição, status de evento (Rascunho/Publicado), validações de data e horário. Calendário impede movimentação para datas passadas ou fora do evento. |

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
|------------|-------------|
| **Backend** | Python 3.10, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF, Flask-Mail |
| **Frontend** | Vue 3, Vuetify, Vue Router, Axios, FullCalendar |
| **Banco de Dados** | PostgreSQL |
| **Containerização** | Docker, Docker Compose |
| **Ferramentas** | Vite (build frontend), Alembic (migrações) |

---

### 🧩 Estrutura de Diretórios

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── configuration.py
│   │   ├── models.py
│   │   ├── forms.py
│   │   ├── views.py
│   │   ├── templates/ (não utilizado, SPA)
│   │   └── static/ (não utilizado, SPA)
│   ├── migrations/
│   ├── requirements.txt
│   ├── Pipfile
│   ├── Pipfile.lock
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── router/
│   │   └── views/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── Dockerfile (backend)
├── frontend/Dockerfile
└── README.md
```

---

## ⚙️ Instalação e Configuração

### Pré-requisitos
- **Docker** e **Docker Compose**
- **Git**

### 1. Clonar o Repositório
```bash
git clone https://github.com/andresichelero/CCC_AndreSichelero_Eventum.git
cd CCC_AndreSichelero_Eventum
```

### 2. Executar com Docker (Recomendado)
```bash
docker-compose up --build
```
- Backend: [http://localhost:5000](http://localhost:5000)
- Frontend: [http://localhost:3000](http://localhost:3000)
- Banco: PostgreSQL em container (porta 5432)

### 3. Instalação Manual (Alternativa)
#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
# Configurar .env com SQLALCHEMY_DATABASE_URI e SECRET_KEY
flask db upgrade
python run.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🧠 Uso

### Principais Rotas da API (Backend)
| Método | Rota | Descrição | Permissão |
|--------|------|-----------|-----------|
| GET | `/api/` | Dashboard com dados do usuário | Logado |
| POST | `/api/register` | Registro de usuário | Público |
| POST | `/api/login` | Login | Público |
| POST | `/api/logout` | Logout | Logado |
| GET | `/api/events` | Lista de eventos publicados | Público |
| GET | `/api/events/<id>` | Detalhes do evento + atividades | Público |
| POST | `/api/events` | Criar evento | Organizador |
| PUT | `/api/events/<id>` | Editar evento | Organizador |
| DELETE | `/api/events/<id>` | Excluir evento | Organizador |
| POST | `/api/events/<id>/inscribe` | Inscrever-se | Participante |
| DELETE | `/api/events/<id>/inscribe` | Cancelar inscrição | Participante |
| POST | `/api/events/<id>/activities` | Adicionar atividade | Organizador |
| PUT | `/api/activities/<id>` | Editar atividade | Organizador |
| DELETE | `/api/activities/<id>` | Excluir atividade | Organizador |
| POST | `/api/events/<id>/submit` | Submeter trabalho | Autor |
| POST | `/api/submissions/<id>/evaluate` | Avaliar submissão | Organizador |

### Páginas do Frontend (Vue Router)
- `/` - Home/Dashboard
- `/login` - Login
- `/register` - Registro
- `/events` - Lista de eventos
- `/events/:id` - Detalhes do evento (com calendário)
- `/events/new` - Criar evento
- `/events/:id/edit` - Editar evento
- `/events/:id/manage-schedule` - Gerenciar programação (calendário editável)
- `/my-inscriptions` - Minhas inscrições
- `/my-submissions` - Minhas submissões
- `/submit/:eventId` - Submeter trabalho

---

## 🧮 Modelos de Banco de Dados

### User
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.SmallInteger, nullable=False, default=3)  # 1=Organizador, 2=Autor, 3=Participante
```

### Event
```python
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    inscription_start_date = db.Column(db.DateTime, nullable=False)
    inscription_end_date = db.Column(db.DateTime, nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.SmallInteger, nullable=False, default=1)  # 1=Rascunho, 2=Publicado
    submission_start_date = db.Column(db.DateTime)
    submission_end_date = db.Column(db.DateTime)
```

### Activity
```python
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(250))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
```

### Submission
```python
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    status = db.Column(db.SmallInteger, default=1)  # 1=Pendente, 3=Aprovado, 4=Rejeitado
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
```

---

## 🧾 Relatório de Progresso do Projeto

### 📍 Status Atual
O **Eventum** implementa **todos os requisitos funcionais principais (RF01–RF04)** e **regras de negócio** descritas no DVP. Os módulos estão funcionalmente integrados, com frontend responsivo e calendário interativo.

### 🧱 Estrutura e Arquitetura
- **Backend**: API REST com Flask, arquitetura MVC, autenticação JWT-like via sessions.
- **Frontend**: SPA com Vue 3, Vuetify para UI, Vue Router para navegação, Axios para API calls.
- **Banco**: PostgreSQL com migrações via Alembic.
- **Containerização**: Docker Compose para desenvolvimento e produção.

---

## 🧩 Próximos Passos (Backlog)

### 1. Melhorias no Calendário
- Adicionar popups com detalhes das atividades ao clicar.
- Suporte a eventos recorrentes ou atividades repetidas.

### 2. Notificações por E-mail Automáticas
- Garantir envio em todas as ações relevantes (registro, inscrição, avaliação de submissões).

---

## 💡 Futuras Melhorias
- Notificações em tempo real (WebSockets para atualizações live).
- Suporte a múltiplos idiomas (i18n).
- Melhorias na UI: tooltips, animações, acessibilidade.
- Relatórios e analytics para organizadores.

---

## 🧰 Desenvolvimento

### Configuração (backend/configuration.py)
```python
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@db:5432/eventumdb"
SECRET_KEY = "your-secret-key"
```

### Validações (forms.py)
- Datas: `end_date > start_date`
- Inscrições: dentro do período
- Atividades: horários válidos e dentro do evento

### Segurança
- Senhas hasheadas (PBKDF2).
- CSRF habilitado.
- Controle de acesso por papéis.

---

## 🧑‍💻 Autor

**André Gasoli Sichelero**  
Universidade de Passo Fundo – Ciência da Computação  
📅 Outubro de 2025  
📧 136235@upf.br  

---

## 🪪 Licença

Este projeto é acadêmico e pode ser reutilizado para fins educacionais.  
Todos os direitos reservados © 2025 – Universidade de Passo Fundo.
