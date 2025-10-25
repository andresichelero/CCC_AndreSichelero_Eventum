# 🗓️ Eventum

> Plataforma web para gestão de eventos acadêmicos, construída com **Flask** e **PostgreSQL**.  
> Este documento reúne tanto a **documentação técnica e operacional** quanto o **relatório de progresso e análise do projeto**.

---

## 📘 Sobre o projeto

O **Eventum** é uma aplicação web que centraliza o gerenciamento de eventos acadêmicos, permitindo que **organizadores**, **palestrantes/autores** e **participantes** interajam em um único sistema.  

A plataforma foi desenvolvida com base em um processo iterativo e incremental, evoluindo de um template básico Flask para uma aplicação completa e funcional, conforme os requisitos estabelecidos no Documento de Visão do Produto (DVP) elaborado.

**Principais objetivos:**
- Automatizar o cadastro, publicação e gerenciamento de eventos.
- Facilitar o processo de inscrição de participantes.
- Oferecer submissão e avaliação de trabalhos acadêmicos.
- Permitir controle de programação (atividades, palestras, workshops).
- Assegurar conformidade com a **LGPD** (Lei Geral de Proteção de Dados).

---

## 🚀 Funcionalidades Implementadas até o momento

| Módulo | Funcionalidades |
|---------|----------------|
| **Autenticação** | Registro, login e logout de usuários com papéis distintos (Organizador, Autor/Palestrante, Participante). Senhas armazenadas com hash seguro (`werkzeug.security`). |
| **Eventos (RF01)** | CRUD completo: criação, edição, visualização e exclusão de eventos. Apenas organizadores têm permissão para gerenciar eventos. |
| **Inscrições (RF02)** | Participantes podem se inscrever em eventos publicados e dentro do período de inscrição. O sistema evita inscrições duplicadas. Organizadores visualizam a lista de participantes. |
| **Submissões de Trabalhos (RF04)** | Autores podem submeter trabalhos com título e resumo; organizadores podem aprovar ou rejeitar submissões. |
| **Programação (RF03)** | Organizadores podem adicionar atividades à programação de um evento. Atividades são validadas quanto ao horário e período do evento. |
| **Validação de Regras de Negócio** | Período de inscrição, status de evento (Rascunho/Publicado), e validações de data e horário são realizadas no `forms.py`. |

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
|------------|-------------|
| Linguagem | Python 3.8/3.10 |
| Framework | Flask |
| Banco de Dados | PostgreSQL (via Docker) |
| ORM | Flask-SQLAlchemy |
| Migrações | Flask-Migrate |
| Autenticação | Flask-Login |
| Formulários | Flask-WTF |
| Frontend | Flask-Bootstrap + Jinja2 |
| E-mail (pendente) | Flask-Mail |
| Containerização | Docker / Docker Compose |

---

### 🧩 Estrutura de Diretórios

```
backend/
 ├── app/
 │   ├── __init__.py
 │   ├── configuration.py
 │   ├── models.py
 │   ├── forms.py
 │   ├── views.py
 │   ├── templates/
 │   └── static/
 ├── migrations/
 ├── requirements.txt
 ├── Pipfile
 ├── Pipfile.lock
 └── run.py
frontend/
 ├── src/
 ├── public/
 ├── package.json
 └── vite.config.js
```

---

## ⚙️ Instalação e Configuração

### 1. Pré-requisitos

- **Python 3.10+**
- **Docker** e **Docker Compose**
- **PostgreSQL (local ou containerizado)**

### 2. Clonar o Repositório

```bash
git clone https://github.com/seuusuario/eventum.git
cd eventum
```

### 3. Configurar o Banco de Dados (Docker)

Crie um container PostgreSQL local:

```bash
docker run --name eventum-db -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
```

### 4. Criar e Ativar Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 5. Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

### 6. Configurar Variáveis de Ambiente


```python
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost/postgres"
SECRET_KEY = "password"
```

### 7. Inicializar o Banco de Dados

```bash
cd backend
flask db upgrade
```

### 8. Executar a Aplicação

```bash
python run.py
```

Acesse em: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧠 Uso

### Principais Rotas

| Rota | Descrição | Permissão |
|------|------------|------------|
| `/register` | Registro de novo usuário | Público |
| `/login` | Login de usuário | Público |
| `/logout` | Logout | Logado |
| `/events` | Lista de eventos publicados | Público |
| `/event/new` | Criação de evento | Organizador |
| `/event/<id>` | Detalhes do evento, inscrições, submissões | Público / Logado |
| `/event/edit/<id>` | Edição de evento | Organizador |
| `/event/delete/<id>` | Exclusão de evento | Organizador |
| `/event/<id>/schedule` | Gerenciar programação | Organizador |
| `/event/inscribe/<id>` | Inscrição em evento | Participante |
| `/my-inscriptions` | Lista de eventos inscritos | Usuário logado |
| `/event/<id>/submit` | Submeter trabalho | Autor/Palestrante |
| `/my-submissions` | Visualizar submissões | Autor |
| `/submission/evaluate/<id>` | Avaliar submissão | Organizador |

---

## 🧮 Modelos de Banco de Dados

### User
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.SmallInteger, nullable=False, default=3)  # 1=Org, 2=Autor, 3=Partic.
```

### Event
```python
class Event(db.Model):
    title = db.Column(db.String(250), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False, default=1)
```

### Submission
```python
class Submission(db.Model):
    title = db.Column(db.String(250), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    status = db.Column(db.SmallInteger, default=1)
```

### Activity
```python
class Activity(db.Model):
    title = db.Column(db.String(250), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
```

---

## 🧾 Relatório de Progresso do Projeto

### 📍 Status Atual

O **Eventum** já implementa **todos os requisitos funcionais principais (RF01–RF04)** e **regras de negócio da semana 8** descritas no DVP. Os módulos estão funcionalmente integrados e prontos para testes de validação.

### 🧱 Estrutura e Arquitetura
- Arquitetura **MVC** (Model-View-Controller).
- Modularização do código: `models.py`, `forms.py`, `views.py`, `configuration.py`.
- Rotas com decorators e autenticação via `Flask-Login`.
- Templates com **Bootstrap** para responsividade.
- Banco PostgreSQL gerenciado via **Flask-Migrate**.

---

## 🧩 Próximos Passos (Backlog)

### 1. Termo de Consentimento (LGPD – RNF05)
- Adicionar campo de aceite no `RegistrationForm`.
- Criar páginas `/termos-de-uso` e `/politica-de-privacidade`.

### 2. Notificações por E-mail (Flask-Mail)
- Configurar e enviar e-mails em ações como registro, inscrição e avaliação.

### 3. Dashboard Dinâmico
- Mostrar diferentes painéis conforme o papel do usuário:
  - Participante: próximos eventos.
  - Autor: submissões pendentes.
  - Organizador: eventos criados.

### 4. Cancelamento de Inscrição
- Criar rota `/event/unsubscribe/<id>` e botão em `my_inscriptions.html`.

---

## 💡 Futuras Melhorias

- CRUD completo para atividades da programação.
- Suporte a eventos de múltiplos dias.
- Upload de arquivos nas submissões (PDF/DOCX, com verificação de tipo, tamanho e malware).
- Página “Meus Eventos” exclusiva para organizadores.
- Integração de notificações assíncronas (Celery ou APScheduler).

---
## 🧰 Desenvolvimento

### Arquivo `configuration.py`
Define as configurações de ambiente:
```python
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost/postgres"
SECRET_KEY = "password"
CSRF_ENABLED = True
```

### Validações Importantes (em `forms.py`)
- **Datas**: verificação se `end_date > start_date`.
- **Inscrições**: garantem período válido.
- **Atividades**: horários dentro do evento.

### Segurança
- Senhas armazenadas com hash (PBKDF2 via Werkzeug).
- CSRF habilitado globalmente.
- Controle de acesso por papel (role-based access control).

---

## 🧑‍💻 Autor

**André Gasoli Sichelero**  
Universidade de Passo Fundo – Curso de Ciência da Computação  
📅 Outubro de 2025  
📧 contato: 136235@upf.br  

---

## 🪪 Licença

Este projeto é de uso acadêmico e pode ser reutilizado para fins educacionais.  
Todos os direitos reservados © 2025 – Universidade de Passo Fundo.
