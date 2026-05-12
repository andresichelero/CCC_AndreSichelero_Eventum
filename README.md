# 🗓️ Eventum

> Plataforma web para gestão de eventos acadêmicos, construída com **Flask** (backend) e **Vue.js** (frontend), utilizando **PostgreSQL** como banco de dados.
> Este documento reúne tanto a **documentação técnica e operacional** quanto o **relatório de progresso e análise do projeto**.

<p align="center">
    <a href="#english-version"><strong>English version</strong></a>
</p>

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
- Integrar vínculos acadêmicos para melhor organização e personalização.

## 🚀 Funcionalidades Implementadas

| Módulo                             | Funcionalidades                                                                                                                                                                                                                                                                                        |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Autenticação**                   | Registro, login e logout de usuários com papéis distintos (Organizador, Autor/Palestrante, Participante, Professor). Senhas armazenadas com hash seguro (`werkzeug.security`). Vínculos acadêmicos opcionais (faculdade, curso, turma) com pesquisa e adição dinâmica. Recuperação de senha via email. |
| **Eventos (RF01)**                 | CRUD completo: criação, edição, visualização e exclusão de eventos. Apenas organizadores têm permissão para gerenciar eventos. Suporte a eventos vinculados a faculdades, cursos ou turmas.                                                                                                            |
| **Inscrições (RF02)**              | Participantes podem se inscrever em eventos publicados e dentro do período de inscrição. O sistema evita inscrições duplicadas. Organizadores visualizam a lista de participantes (públicos e privados). Cancelamento de inscrições.                                                                   |
| **Submissões de Trabalhos (RF04)** | Autores podem submeter trabalhos com arquivos (PDF, DOC, DOCX, ODT, RTF) e títulos. Organizadores podem aprovar ou rejeitar submissões. Download seguro de arquivos.                                                                                                                                   |
| **Programação (RF03)**             | Organizadores podem adicionar, editar e gerenciar atividades com calendário interativo (FullCalendar). Participantes visualizam a programação em grade. Suporte a drag-and-drop para reorganizar horários. Controle de presença com check-in via código.                                               |
| **Validação de Regras de Negócio** | Período de inscrição, status de evento (Rascunho/Publicado), validações de data e horário. Calendário impede movimentação para datas passadas ou fora do evento. Validações de MIME type para uploads.                                                                                                 |
| **Vínculos Acadêmicos**            | Sistema hierárquico de faculdades, cursos e turmas com lista extensa populada automaticamente via CSV. Pesquisa em tempo real, adição de cursos/turmas personalizados. Gerenciamento de turmas por professores.                                                                                        |
| **Certificados**                   | Geração automática de certificados em PDF para participantes de eventos concluídos, incluindo carga horária.                                                                                                                                                                                           |
| **LGPD Compliance**                | Política de privacidade, termos de uso, controle de perfis públicos, minimização de dados coletados.                                                                                                                                                                                                   |

## 🛠️ Tecnologias Utilizadas

| Categoria           | Tecnologia       | Versão | Propósito                    |
| ------------------- | ---------------- | ------ | ---------------------------- |
| **Backend**         | Python           | 3.10+  | Linguagem principal          |
|                     | Flask            | 2.3+   | Framework web                |
|                     | Flask-SQLAlchemy | 3.0+   | ORM para banco de dados      |
|                     | Flask-Migrate    | 4.0+   | Migrações de banco           |
|                     | Flask-Login      | 0.6+   | Gerenciamento de sessões     |
|                     | Flask-WTF        | 1.1+   | Formulários e validações     |
|                     | Flask-Mail       | 0.9+   | Envio de emails              |
|                     | Flask-CORS       | 4.0+   | Suporte a CORS               |
|                     | python-dotenv    | 1.0+   | Variáveis de ambiente        |
|                     | Werkzeug         | 2.3+   | Utilitários (hash de senhas) |
|                     | WeasyPrint       | 60+    | Geração de PDFs              |
|                     | python-magic     | 0.4+   | Detecção de tipos de arquivo |
| **Frontend**        | Vue.js           | 3.5+   | Framework JavaScript         |
|                     | Vuetify          | 3.0+   | Biblioteca de componentes UI |
|                     | Vue Router       | 4.6+   | Roteamento SPA               |
|                     | Axios            | 1.12+  | Cliente HTTP                 |
|                     | FullCalendar     | 6.1+   | Calendário interativo        |
|                     | Vite             | 5.4+   | Build tool e dev server      |
| **Banco de Dados**  | PostgreSQL       | 13+    | Banco relacional             |
|                     | Alembic          | 1.12+  | Sistema de migrações         |
| **Containerização** | Docker           | 20+    | Containerização              |
|                     | Docker Compose   | 2.0+   | Orquestração de containers   |
| **Ferramentas**     | Git              | 2.0+   | Controle de versão           |
|                     | ESLint           | 8.57+  | Linting JavaScript           |
|                     | Prettier         | 3.6+   | Formatação de código         |

## 📁 Estrutura de Diretórios

```
eventum/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Inicialização da aplicação Flask
│   │   ├── configuration.py     # Configurações por ambiente
│   │   ├── models.py            # Modelos SQLAlchemy
│   │   ├── forms.py             # Formulários WTForms
│   │   ├── views.py             # Rotas e lógica da API
│   │   ├── faculdades.csv       # Dados de faculdades brasileiras
│   │   ├── populate_cursos.py   # Script de população inicial
│   │   ├── populate_test_data.py # Dados de teste
│   │   └── uploads/             # Arquivos submetidos (criado runtime)
│   ├── migrations/              # Migrações Alembic
│   ├── requirements.txt         # Dependências Python
│   ├── Pipfile                  # Ambiente Pipenv (alternativo)
│   ├── Pipfile.lock
│   └── run.py                   # Ponto de entrada da aplicação
├── frontend/
│   ├── src/
│   │   ├── App.vue              # Componente raiz Vue
│   │   ├── main.js              # Inicialização Vue
│   │   ├── router/
│   │   │   └── index.js         # Definição de rotas
│   │   └── views/               # Páginas Vue
│   │
│   ├── public/                  # Assets estáticos
│   ├── package.json             # Dependências Node.js
│   ├── package-lock.json
│   ├── vite.config.js           # Configuração Vite
│   ├── .eslintrc.cjs            # Configuração ESLint
│   └── .prettierrc              # Configuração Prettier
├── .env.example                 # Exemplo de variáveis de ambiente
├── docker-compose.yml           # Orquestração Docker
├── Dockerfile                   # Container backend
├── frontend/Dockerfile          # Container frontend
├── .gitignore                   # Arquivos ignorados pelo Git
├── database_schema.md           # Documentação do schema BD
└── README.md
```

## ⚙️ Instalação e Configuração

### Pré-requisitos do Sistema

- **Sistema Operacional**: Linux, macOS ou Windows (via WSL)
- **Docker**: Versão 20.10+ com Docker Compose 2.0+
- **Git**: Versão 2.0+
- **Navegador Web**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### 1. Clonagem do Repositório

```bash
git clone https://github.com/andresichelero/CCC_AndreSichelero_Eventum.git
cd CCC_AndreSichelero_Eventum
```

### 2. Configuração das Variáveis de Ambiente

Copie o arquivo de exemplo e configure as variáveis necessárias:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Flask Configuration
SECRET_KEY=sua-chave-secreta-muito-forte-aqui
FLASK_APP=run.py
FLASK_ENV=development

# Database Configuration
SQLALCHEMY_DATABASE_URI=postgresql://postgres:password@db:5432/eventumdb

# Email Configuration (opcional, para funcionalidades de email)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=sua-senha-de-app
MAIL_DEFAULT_SENDER=seu-email@gmail.com

# Server Configuration
PORT=5000
```

**Nota**: Para Gmail, use uma "senha de app" em vez da senha normal da conta.

### 3. Execução com Docker (Recomendado)

```bash
# Construir e iniciar todos os serviços
docker-compose up --build

# Ou executar em background
docker-compose up -d --build
```

**Serviços disponíveis:**

- **Backend API**: http://localhost:5000
- **Frontend SPA**: http://localhost:3000
- **Banco PostgreSQL**: localhost:5432 (apenas interno)

### 4. Verificação da Instalação

Após iniciar os containers, verifique se tudo está funcionando:

```bash
# Verificar status dos containers
docker-compose ps

# Ver logs em caso de problemas
docker-compose logs web
docker-compose logs frontend
```

### 5. Instalação Manual (Alternativa)

#### Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar banco de dados
export FLASK_APP=run.py
export FLASK_ENV=development
flask db upgrade

# Executar aplicação
python run.py
```

#### Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run dev

# Ou build para produção
npm run build
npm run preview
```

### 6. População de Dados Iniciais

```bash
# Acessar container do backend
docker-compose exec web bash

# Executar scripts de população
cd /app/backend
python -c "from app.populate_cursos import populate_faculdades, populate_cursos; populate_faculdades(); populate_cursos()"
python populate_test_data.py
```

## 🧠 Uso da Aplicação

### Papéis de Usuário

1. **Participante** (padrão): Pode visualizar eventos, se inscrever, fazer check-in em atividades
2. **Autor/Palestrante**: Pode submeter trabalhos para eventos
3. **Organizador**: Pode criar e gerenciar eventos, avaliar submissões, gerenciar programação
4. **Professor**: Pode gerenciar turmas e alunos

### Fluxo Básico de Uso

#### Para Participantes

1. **Registro**: Criar conta com vínculos acadêmicos opcionais
2. **Exploração**: Visualizar eventos publicados no calendário
3. **Inscrição**: Inscrever-se em eventos de interesse
4. **Participação**: Fazer check-in em atividades usando códigos
5. **Certificação**: Baixar certificados após conclusão do evento

#### Para Organizadores

1. **Criação**: Criar eventos com datas, descrições e configurações
2. **Programação**: Adicionar atividades via calendário interativo
3. **Publicação**: Tornar evento visível para participantes
4. **Gestão**: Avaliar submissões, monitorar inscrições
5. **Relatórios**: Exportar listas de participantes

### API REST Documentation

#### Autenticação

| Método | Endpoint               | Descrição                | Autenticação |
| ------ | ---------------------- | ------------------------ | ------------ |
| POST   | `/api/register`        | Registrar novo usuário   | Público      |
| POST   | `/api/login`           | Fazer login              | Público      |
| POST   | `/api/logout`          | Fazer logout             | Autenticado  |
| POST   | `/api/forgot-password` | Solicitar reset de senha | Público      |
| POST   | `/api/reset-password`  | Redefinir senha          | Público      |

#### Dashboard

| Método | Endpoint | Descrição                     | Autenticação |
| ------ | -------- | ----------------------------- | ------------ |
| GET    | `/api/`  | Dados do dashboard do usuário | Autenticado  |

#### Eventos

| Método | Endpoint                    | Descrição                 | Autenticação | Permissão    |
| ------ | --------------------------- | ------------------------- | ------------ | ------------ |
| GET    | `/api/events`               | Listar eventos publicados | Público      | -            |
| GET    | `/api/events/<id>`          | Detalhes do evento        | Público      | -            |
| POST   | `/api/events`               | Criar evento              | Autenticado  | Organizador  |
| PUT    | `/api/events/<id>`          | Editar evento             | Autenticado  | Organizador  |
| DELETE | `/api/events/<id>`          | Excluir evento            | Autenticado  | Organizador  |
| POST   | `/api/events/<id>/inscribe` | Inscrever-se              | Autenticado  | Participante |
| DELETE | `/api/events/<id>/inscribe` | Cancelar inscrição        | Autenticado  | Participante |
| GET    | `/api/my-organized-events`  | Eventos organizados       | Autenticado  | Organizador  |
| GET    | `/api/my-inscriptions`      | Minhas inscrições         | Autenticado  | -            |

#### Atividades

| Método | Endpoint                             | Descrição         | Autenticação | Permissão    |
| ------ | ------------------------------------ | ----------------- | ------------ | ------------ |
| POST   | `/api/events/<id>/activities`        | Criar atividade   | Autenticado  | Organizador  |
| PUT    | `/api/activities/<id>`               | Editar atividade  | Autenticado  | Organizador  |
| DELETE | `/api/activities/<id>`               | Excluir atividade | Autenticado  | Organizador  |
| POST   | `/api/activities/<id>/open-checkin`  | Abrir check-in    | Autenticado  | Organizador  |
| POST   | `/api/activities/<id>/close-checkin` | Fechar check-in   | Autenticado  | Organizador  |
| POST   | `/api/checkin`                       | Fazer check-in    | Autenticado  | Participante |

#### Submissões

| Método | Endpoint                         | Descrição         | Autenticação | Permissão         |
| ------ | -------------------------------- | ----------------- | ------------ | ----------------- |
| GET    | `/api/my-submissions`            | Minhas submissões | Autenticado  | -                 |
| POST   | `/api/events/<id>/submit`        | Submeter trabalho | Autenticado  | Autor             |
| POST   | `/api/submissions/<id>/evaluate` | Avaliar submissão | Autenticado  | Organizador       |
| GET    | `/api/submissions/<id>/download` | Download arquivo  | Autenticado  | Autor/Organizador |

#### Acadêmicos

| Método | Endpoint                          | Descrição                 | Autenticação            |
| ------ | --------------------------------- | ------------------------- | ----------------------- |
| GET    | `/api/faculdades`                 | Listar faculdades         | Público                 |
| GET    | `/api/cursos`                     | Listar cursos             | Público                 |
| POST   | `/api/cursos`                     | Criar curso personalizado | Público                 |
| GET    | `/api/turmas`                     | Listar turmas             | Público                 |
| POST   | `/api/turmas`                     | Criar turma               | Autenticado (Org/Prof)  |
| PUT    | `/api/turmas/<id>`                | Editar turma              | Autenticado (Professor) |
| POST   | `/api/turmas/<id>/add_student`    | Adicionar aluno           | Autenticado (Professor) |
| POST   | `/api/turmas/<id>/remove_student` | Remover aluno             | Autenticado (Professor) |

#### Utilitários

| Método | Endpoint                               | Descrição                    | Autenticação      |
| ------ | -------------------------------------- | ---------------------------- | ----------------- |
| GET    | `/api/calendar`                        | Dados do calendário          | Público           |
| PUT    | `/api/me/settings`                     | Atualizar perfil             | Autenticado       |
| GET    | `/api/events/<id>/export_participants` | Exportar participantes (CSV) | Autenticado (Org) |
| GET    | `/api/event/<id>/certificate`          | Gerar certificado (PDF)      | Autenticado       |

### Interface Web (Frontend)

#### Páginas Principais

- **/** - Página inicial com informações gerais
- **/login** - Autenticação de usuários
- **/register** - Registro de novos usuários
- **/dashboard** - Painel personalizado do usuário logado
- **/events** - Lista de eventos publicados
- **/events/:id** - Detalhes do evento e programação
- **/calendar** - Visualização em calendário de todos os eventos/atividades
- **/profile** - Gerenciamento do perfil do usuário

#### Páginas de Gestão (Organizadores)

- **/events/new** - Criar novo evento
- **/events/:id/edit** - Editar evento existente
- **/events/:id/manage-schedule** - Gerenciar programação (calendário editável)
- **/my-organized-events** - Lista de eventos organizados
- **/manage-turmas** - Gerenciar turmas (professores/organizadores)

#### Páginas de Participação

- **/my-inscriptions** - Eventos nos quais estou inscrito
- **/my-submissions** - Trabalhos que submeti
- **/submit/:eventId** - Formulário de submissão de trabalho

#### Páginas Legais

- **/terms-of-use** - Termos de uso da plataforma
- **/privacy-policy** - Política de privacidade (LGPD)

## 🧮 Modelos de Banco de Dados

### Resumo dos Modelos

Para detalhes completos sobre o schema relacional, incluindo relacionamentos, restrições e tipos de dados, consulte o arquivo [`database_schema.md`](./database_schema.md).

#### User

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.SmallInteger, nullable=False, default=3)  # 1=Org, 2=Autor, 3=Part, 4=Prof
    allow_public_profile = db.Column(db.Boolean, nullable=False, default=False)
    reset_token = db.Column(db.String(256), nullable=True)
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"), nullable=True)
    turma_id = db.Column(db.Integer, db.ForeignKey("turma.id"), nullable=True)
```

#### Event

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
    submission_start_date = db.Column(db.DateTime, nullable=True)
    submission_end_date = db.Column(db.DateTime, nullable=True)
    workload = db.Column(db.Integer, nullable=True, default=0)
    faculdade_id = db.Column(db.Integer, db.ForeignKey("faculdade.id"), nullable=True)
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"), nullable=True)
    turma_id = db.Column(db.Integer, db.ForeignKey("turma.id"), nullable=True)
```

#### Hierarquia Acadêmica

- **Faculdade** → **Curso** → **Turma** → **User**
- Sistema populado automaticamente via CSV de faculdades brasileiras
- Suporte a criação dinâmica de cursos e turmas personalizados

## 🔧 Configuração Avançada

### Variáveis de Ambiente Detalhadas

```env
# Flask Core
SECRET_KEY=chave-secreta-min-32-caracteres
FLASK_APP=run.py
FLASK_ENV=development  # development, production, testing

# Database
SQLALCHEMY_DATABASE_URI=postgresql://user:password@host:port/database
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_ECHO=False  # Set True para debug SQL

# Email (SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=seu-email@dominio.com
MAIL_PASSWORD=senha-app-especifica
MAIL_DEFAULT_SENDER=noreply@eventum.com

# File Uploads
UPLOADED_FILES_DEST=/app/backend/app/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB

# Security
SESSION_COOKIE_SECURE=False  # True em produção com HTTPS
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Configuração do PostgreSQL

```sql
-- Criar banco de dados
CREATE DATABASE eventumdb;

-- Criar usuário
CREATE USER postgres WITH PASSWORD 'password';

-- Conceder permissões
GRANT ALL PRIVILEGES ON DATABASE eventumdb TO postgres;
```

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão com Banco de Dados

```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```

**Soluções:**

- Verificar se o container PostgreSQL está rodando: `docker-compose ps`
- Verificar logs: `docker-compose logs db`
- Resetar banco: `docker-compose down -v && docker-compose up --build`

#### 2. Erro de Migrações

```
alembic.util.exc.CommandError: Can't locate revision identified by 'head'
```

**Soluções:**

- Resetar migrações: `rm -rf backend/migrations/versions/*`
- Recriar: `flask db migrate && flask db upgrade`

#### 3. Frontend não carrega

```
Failed to load resource: net::ERR_CONNECTION_REFUSED
```

**Soluções:**

- Verificar se o container frontend está rodando
- Verificar CORS no backend
- Verificar VITE_API_BASE_URL no frontend

#### 4. Upload de arquivos falha

```
The file is too large
```

**Soluções:**

- Aumentar MAX_CONTENT_LENGTH no Flask
- Verificar permissões da pasta uploads
- Verificar espaço em disco no container

#### 5. Emails não são enviados

```
smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted')
```

**Soluções:**

- Usar senha de app do Gmail
- Verificar configurações SMTP
- Verificar firewall/antivírus

### Logs e Debug

#### Ver logs dos containers

```bash
# Todos os serviços
docker-compose logs

# Serviço específico
docker-compose logs web

# Seguir logs em tempo real
docker-compose logs -f web
```

#### Debug do Flask

```bash
# Ativar debug mode
export FLASK_ENV=development
export FLASK_DEBUG=1

# Ver SQL queries
export SQLALCHEMY_ECHO=True
```

#### Debug do Vue.js

```bash
cd frontend
npm run dev -- --debug
```

### Comandos Úteis de Desenvolvimento

```bash
# Reset completo do ambiente
docker-compose down -v
docker system prune -f
docker-compose up --build

# Acessar container
docker-compose exec web bash

# Executar testes (se implementados)
docker-compose exec web python -m pytest

# Backup do banco
docker-compose exec db pg_dump -U postgres eventumdb > backup.sql

# Restore do banco
docker-compose exec -T db psql -U postgres eventumdb < backup.sql
```

## 🧾 Relatório de Progresso do Projeto

### 📍 Status Atual

O **Eventum** implementa **todos os requisitos funcionais principais (RF01–RF04)** e **regras de negócio** descritas no DVP, além de funcionalidades extras como vínculos acadêmicos, controle de presença, certificados digitais e compliance LGPD.

### 🧱 Arquitetura e Design

- **Backend**: API REST com Flask, arquitetura MVC, autenticação via Flask-Login, suporte a CORS para SPA.
- **Frontend**: Single Page Application com Vue 3, Vuetify 3 para UI moderna, Vue Router para navegação, Axios para comunicação com API.
- **Banco**: PostgreSQL com migrações via Alembic, suporte a relacionamentos complexos e hierarquia acadêmica.
- **Containerização**: Docker Compose para desenvolvimento e produção, com volumes para persistência de dados.
- **Segurança**: Hash de senhas com Werkzeug, validações de entrada, controle de acesso baseado em papéis, sanitização de uploads.

### 📊 Métricas do Projeto

- **Linhas de Código**: ~5000+ (Backend: ~3000, Frontend: ~2000)
- **Cobertura de Funcionalidades**: 100% dos RFs principais + extras
- **Tabelas do Banco**: 9 (8 entidades + 1 associativa)
- **Endpoints API**: 25+ rotas REST
- **Páginas Frontend**: 15+ views Vue
- **Tecnologias**: 15+ bibliotecas/frameworks

## 🧩 Próximos Passos (Backlog)

### 1. Melhorias no Calendário

- Adicionar popups com detalhes das atividades ao clicar
- Suporte a eventos recorrentes ou atividades repetidas
- Visualização de conflitos de horário
- Exportar calendário para iCal/Google Calendar
- Sincronização bidirecional com Google Calendar

### 2. Notificações por E-mail Automáticas

- Sistema de templates de email customizáveis
- Notificações push no navegador para mudanças em eventos
- Lembretes automáticos (24h antes do evento)
- Relatórios semanais para organizadores

### 3. Melhorias nos Vínculos Acadêmicos

- Integração com APIs externas (MEC, CNPq) para validação
- Relatórios por faculdade/curso (estatísticas de participação)
- Sistema de recomendações baseado no perfil acadêmico
- Importação em lote de alunos/turmas via CSV/Excel

### 4. Notificações em Tempo Real

- WebSockets com Socket.IO para atualizações live
- Notificações push nativas no navegador móvel
- Chat integrado entre participantes e organizadores
- Status online de usuários

### 5. Internacionalização (i18n)

- Suporte a múltiplos idiomas (PT, EN, ES)
- Interface para tradução dinâmica
- Formatação de datas/moedas por locale
- RTL support para árabe/hebraico

### 6. Acessibilidade e UX

- Conformidade WCAG 2.1 (níveis A, AA, AAA)
- Suporte a leitores de tela e navegação por teclado
- Testes de usabilidade com usuários reais
- Modo escuro/claro automático

### 7. Relatórios e Analytics

- Dashboards com métricas em tempo real
- Exportação de relatórios em PDF/Excel/CSV
- Análise de tendências e previsões com ML
- Integração com Google Analytics

### 8. Integração com Pagamentos

- Suporte a inscrições pagas (Stripe, PagSeguro, Mercado Pago)
- Sistema de preços dinâmicos
- Reembolsos automáticos para cancelamentos
- Integração com sistemas de gestão financeira

### 9. API Pública e Integrações

- Documentação OpenAPI/Swagger completa
- Webhooks para integrações externas
- OAuth 2.0 para autenticação de terceiros
- SDKs para integração com outros sistemas

### 10. Mobile e PWA

- Progressive Web App (PWA) para instalação nativa
- Otimização completa para dispositivos móveis
- Notificações push nativas
- Suporte offline para visualização de eventos

### 11. Gamificação e Engajamento

- Sistema de pontos/badges para participação ativa
- Rankings de eventos mais populares
- Certificados digitais com QR codes
- Sistema de referências e indicações

### 12. Segurança e Conformidade

- Auditoria completa de logs para LGPD
- Two-factor authentication (2FA/TOTP)
- Encriptação end-to-end para dados sensíveis
- Penetration testing e security audits

## 🔧 Refactors e Otimizações Técnicas

### Backend

- **Separação de Concerns**: Extrair lógica de negócio para services/layers
- **Async/Await**: Migrar operações I/O para assíncronas
- **Cache**: Redis para cache de queries frequentes
- **Testes**: Cobertura completa com pytest
- **API Versioning**: Versionar endpoints (/api/v1/)
- **Rate Limiting**: Flask-Limiter para proteção contra abuso

### Frontend

- **Componentização**: Quebrar componentes grandes em menores
- **State Management**: Pinia/Vuex para estado complexo
- **Lazy Loading**: Carregar rotas/componentes sob demanda
- **Performance**: Code splitting e tree shaking
- **Testes**: E2E com Playwright

### Banco de Dados

- **Índices**: Otimizar queries com índices apropriados
- **Particionamento**: Para tabelas grandes (logs, auditoria)
- **Backup Automático**: Estratégias robustas de backup

### DevOps

- **CI/CD**: GitHub Actions para testes e deploy
- **Monitoramento**: Prometheus + Grafana
- **Containerização**: Multi-stage builds para produção
- **Orquestração**: Kubernetes para escalabilidade

## 💡 Futuras Melhorias Avançadas

- **IA/ML**: Recomendações personalizadas usando machine learning
- **Blockchain**: Certificados imutáveis para submissões
- **VR/AR**: Experiências imersivas para eventos virtuais
- **IoT**: Controle de acesso físico via RFID/NFC

## 📄 Licença

Este projeto está licenciado sob a MIT License.

## 👥 Autores

- **André Sichelero** - Desenvolvimento principal

_Última atualização: Outubro 2025_

---

## English Version

# 🗓️ Eventum

> Academic event management web platform, built with **Flask** (backend) and **Vue.js** (frontend), using **PostgreSQL** as the database.
> This document combines the **technical and operational documentation** with the **project progress report and analysis**.

## 📘 About the Project

**Eventum** is a web application that centralizes academic event management, allowing **organizers**, **speakers/authors**, and **participants** to interact within a single system.

The platform was developed through an iterative and incremental process, evolving from a basic Flask template into a complete and functional application, in line with the requirements established in the Product Vision Document (DVP) that was prepared.

**Main objectives:**

- Automate event registration, publication, and management.
- Facilitate the participant registration process.
- Offer academic paper submission and review.
- Provide schedule control with an interactive calendar (activities, lectures, workshops).
- Ensure compliance with the **LGPD** (Brazilian General Data Protection Law).
- Integrate academic affiliations for better organization and personalization.

## 🚀 Implemented Features

| Module                             | Features                                                                                                                                                                                                                                                                                        |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Authentication**                | User registration, login, and logout with distinct roles (Organizer, Author/Speaker, Participant, Professor). Passwords stored with secure hashing (`werkzeug.security`). Optional academic affiliations (faculty, course, class) with search and dynamic addition. Password recovery by email. |
| **Events (RF01)**                  | Full CRUD: create, edit, view, and delete events. Only organizers can manage events. Support for events linked to faculties, courses, or classes.                                                                                                                                                |
| **Registrations (RF02)**           | Participants can register for published events within the registration period. The system prevents duplicate registrations. Organizers can view the participant list (public and private). Registration cancellation.                                                                           |
| **Paper Submissions (RF04)**       | Authors can submit papers with files (PDF, DOC, DOCX, ODT, RTF) and titles. Organizers can approve or reject submissions. Secure file downloads.                                                                                                                                               |
| **Scheduling (RF03)**              | Organizers can add, edit, and manage activities with an interactive calendar (FullCalendar). Participants can view the schedule in a grid layout. Drag-and-drop support for reorganizing times. Attendance control with code-based check-in.                                                   |
| **Business Rule Validation**        | Registration period, event status (Draft/Published), date and time validation. The calendar prevents movement to past dates or outside the event window. MIME type validation for uploads.                                                                                                     |
| **Academic Affiliations**           | Hierarchical system of faculties, courses, and classes with an extensive list populated automatically via CSV. Real-time search, addition of custom courses/classes. Class management by professors.                                                                                           |
| **Certificates**                    | Automatic generation of PDF certificates for participants in completed events, including workload.                                                                                                                                                                                               |
| **LGPD Compliance**                 | Privacy policy, terms of use, public profile control, data minimization.                                                                                                                                                                                                                        |

## 🛠️ Technologies Used

| Category            | Technology        | Version | Purpose                      |
| ------------------- | ----------------- | ------- | ---------------------------- |
| **Backend**         | Python            | 3.10+   | Main language                |
|                     | Flask             | 2.3+    | Web framework                |
|                     | Flask-SQLAlchemy  | 3.0+    | Database ORM                 |
|                     | Flask-Migrate     | 4.0+    | Database migrations          |
|                     | Flask-Login       | 0.6+    | Session management           |
|                     | Flask-WTF         | 1.1+    | Forms and validation         |
|                     | Flask-Mail        | 0.9+    | Email sending                |
|                     | Flask-CORS        | 4.0+    | CORS support                 |
|                     | python-dotenv     | 1.0+    | Environment variables        |
|                     | Werkzeug          | 2.3+    | Utilities (password hashing) |
|                     | WeasyPrint        | 60+     | PDF generation               |
|                     | python-magic      | 0.4+    | File type detection          |
| **Frontend**        | Vue.js            | 3.5+    | JavaScript framework         |
|                     | Vuetify           | 3.0+    | UI component library         |
|                     | Vue Router        | 4.6+    | SPA routing                  |
|                     | Axios             | 1.12+   | HTTP client                  |
|                     | FullCalendar      | 6.1+    | Interactive calendar         |
|                     | Vite              | 5.4+    | Build tool and dev server    |
| **Database**        | PostgreSQL        | 13+     | Relational database          |
|                     | Alembic           | 1.12+   | Migration system             |
| **Containerization**| Docker            | 20+     | Containerization             |
|                     | Docker Compose    | 2.0+    | Container orchestration      |
| **Tools**           | Git               | 2.0+    | Version control              |
|                     | ESLint            | 8.57+   | JavaScript linting           |
|                     | Prettier          | 3.6+    | Code formatting              |

## 📁 Directory Structure

```
eventum/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask application initialization
│   │   ├── configuration.py     # Environment-specific settings
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── forms.py             # WTForms forms
│   │   ├── views.py             # API routes and logic
│   │   ├── faculdades.csv       # Brazilian faculty data
│   │   ├── populate_cursos.py   # Initial population script
│   │   ├── populate_test_data.py # Test data
│   │   └── uploads/             # Submitted files (created at runtime)
│   ├── migrations/              # Alembic migrations
│   ├── requirements.txt         # Python dependencies
│   ├── Pipfile                  # Pipenv environment (alternative)
│   ├── Pipfile.lock
│   └── run.py                   # Application entry point
├── frontend/
│   ├── src/
│   │   ├── App.vue              # Root Vue component
│   │   ├── main.js              # Vue initialization
│   │   ├── router/
│   │   │   └── index.js         # Route definitions
│   │   └── views/               # Vue pages
│   │
│   ├── public/                  # Static assets
│   ├── package.json             # Node.js dependencies
│   ├── package-lock.json
│   ├── vite.config.js           # Vite configuration
│   ├── .eslintrc.cjs            # ESLint configuration
│   └── .prettierrc              # Prettier configuration
├── .env.example                 # Example environment variables
├── docker-compose.yml           # Docker orchestration
├── Dockerfile                   # Backend container
├── frontend/Dockerfile          # Frontend container
├── .gitignore                   # Git-ignored files
├── database_schema.md           # Database schema documentation
└── README.md
```

## ⚙️ Installation and Setup

### System Requirements

- **Operating System**: Linux, macOS, or Windows (via WSL)
- **Docker**: Version 20.10+ with Docker Compose 2.0+
- **Git**: Version 2.0+
- **Web Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### 1. Clone the Repository

```bash
git clone https://github.com/andresichelero/CCC_AndreSichelero_Eventum.git
cd CCC_AndreSichelero_Eventum
```

### 2. Configure Environment Variables

Copy the example file and set the required variables:

```bash
cp .env.example .env
```

Edit the `.env` file with your settings:

```env
# Flask Configuration
SECRET_KEY=your-very-strong-secret-key-here
FLASK_APP=run.py
FLASK_ENV=development

# Database Configuration
SQLALCHEMY_DATABASE_URI=postgresql://postgres:password@db:5432/eventumdb

# Email Configuration (optional, for email features)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Server Configuration
PORT=5000
```

**Note**: For Gmail, use an "app password" instead of your regular account password.

### 3. Run with Docker (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Or run in the background
docker-compose up -d --build
```

**Available services:**

- **Backend API**: http://localhost:5000
- **Frontend SPA**: http://localhost:3000
- **PostgreSQL Database**: localhost:5432 (internal only)

### 4. Verify the Installation

After starting the containers, check that everything is working:

```bash
# Check container status
docker-compose ps

# View logs if something goes wrong
docker-compose logs web
docker-compose logs frontend
```

### 5. Manual Installation (Alternative)

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure the database
export FLASK_APP=run.py
export FLASK_ENV=development
flask db upgrade

# Run the application
python run.py
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run in development mode
npm run dev

# Or build for production
npm run build
npm run preview
```

### 6. Populate Initial Data

```bash
# Access the backend container
docker-compose exec web bash

# Run population scripts
cd /app/backend
python -c "from app.populate_cursos import populate_faculdades, populate_cursos; populate_faculdades(); populate_cursos()"
python populate_test_data.py
```

## 🧠 Using the Application

### User Roles

1. **Participant** (default): Can view events, register, and check in to activities
2. **Author/Speaker**: Can submit papers for events
3. **Organizer**: Can create and manage events, evaluate submissions, and manage scheduling
4. **Professor**: Can manage classes and students

### Basic Usage Flow

#### For Participants

1. **Registration**: Create an account with optional academic affiliations
2. **Exploration**: View published events in the calendar
3. **Registration**: Register for events of interest
4. **Participation**: Check in to activities using codes
5. **Certification**: Download certificates after the event is completed

#### For Organizers

1. **Creation**: Create events with dates, descriptions, and settings
2. **Scheduling**: Add activities through the interactive calendar
3. **Publication**: Make the event visible to participants
4. **Management**: Evaluate submissions and monitor registrations
5. **Reports**: Export participant lists

### REST API Documentation

#### Authentication

| Method | Endpoint               | Description              | Authentication |
| ------ | ---------------------- | ------------------------ | -------------- |
| POST   | `/api/register`        | Register a new user      | Public         |
| POST   | `/api/login`           | Log in                   | Public         |
| POST   | `/api/logout`          | Log out                  | Authenticated  |
| POST   | `/api/forgot-password` | Request password reset   | Public         |
| POST   | `/api/reset-password`  | Reset password           | Public         |

#### Dashboard

| Method | Endpoint | Description                 | Authentication |
| ------ | -------- | --------------------------- | -------------- |
| GET    | `/api/`  | User dashboard data         | Authenticated  |

#### Events

| Method | Endpoint                    | Description               | Authentication | Permission  |
| ------ | --------------------------- | ------------------------- | -------------- | ----------- |
| GET    | `/api/events`               | List published events     | Public         | -           |
| GET    | `/api/events/<id>`          | Event details             | Public         | -           |
| POST   | `/api/events`               | Create event              | Authenticated  | Organizer   |
| PUT    | `/api/events/<id>`          | Edit event                | Authenticated  | Organizer   |
| DELETE | `/api/events/<id>`          | Delete event              | Authenticated  | Organizer   |
| POST   | `/api/events/<id>/inscribe` | Register for event        | Authenticated  | Participant |
| DELETE | `/api/events/<id>/inscribe` | Cancel registration       | Authenticated  | Participant |
| GET    | `/api/my-organized-events`  | Organized events          | Authenticated  | Organizer   |
| GET    | `/api/my-inscriptions`      | My registrations          | Authenticated  | -           |

#### Activities

| Method | Endpoint                             | Description        | Authentication | Permission  |
| ------ | ------------------------------------ | ------------------ | -------------- | ----------- |
| POST   | `/api/events/<id>/activities`        | Create activity    | Authenticated  | Organizer   |
| PUT    | `/api/activities/<id>`               | Edit activity      | Authenticated  | Organizer   |
| DELETE | `/api/activities/<id>`               | Delete activity    | Authenticated  | Organizer   |
| POST   | `/api/activities/<id>/open-checkin`  | Open check-in      | Authenticated  | Organizer   |
| POST   | `/api/activities/<id>/close-checkin` | Close check-in     | Authenticated  | Organizer   |
| POST   | `/api/checkin`                       | Perform check-in   | Authenticated  | Participant |

#### Submissions

| Method | Endpoint                         | Description         | Authentication | Permission      |
| ------ | -------------------------------- | ------------------- | -------------- | --------------- |
| GET    | `/api/my-submissions`            | My submissions      | Authenticated  | -               |
| POST   | `/api/events/<id>/submit`        | Submit paper        | Authenticated  | Author          |
| POST   | `/api/submissions/<id>/evaluate` | Evaluate submission | Authenticated  | Organizer       |
| GET    | `/api/submissions/<id>/download` | Download file       | Authenticated  | Author/Organizer |

#### Academic Data

| Method | Endpoint                          | Description                    | Authentication           |
| ------ | --------------------------------- | ------------------------------ | ------------------------ |
| GET    | `/api/faculdades`                 | List faculties                 | Public                   |
| GET    | `/api/cursos`                     | List courses                   | Public                   |
| POST   | `/api/cursos`                     | Create custom course           | Public                   |
| GET    | `/api/turmas`                     | List classes                   | Public                   |
| POST   | `/api/turmas`                     | Create class                   | Authenticated (Org/Prof) |
| PUT    | `/api/turmas/<id>`                | Edit class                     | Authenticated (Professor) |
| POST   | `/api/turmas/<id>/add_student`    | Add student                    | Authenticated (Professor) |
| POST   | `/api/turmas/<id>/remove_student` | Remove student                 | Authenticated (Professor) |

#### Utilities

| Method | Endpoint                               | Description                      | Authentication      |
| ------ | -------------------------------------- | -------------------------------- | ------------------- |
| GET    | `/api/calendar`                        | Calendar data                    | Public              |
| PUT    | `/api/me/settings`                     | Update profile                   | Authenticated       |
| GET    | `/api/events/<id>/export_participants` | Export participants (CSV)        | Authenticated (Org) |
| GET    | `/api/event/<id>/certificate`          | Generate certificate (PDF)       | Authenticated       |

### Web Interface (Frontend)

#### Main Pages

- **/** - Home page with general information
- **/login** - User authentication
- **/register** - New user registration
- **/dashboard** - Personalized dashboard for the logged-in user
- **/events** - List of published events
- **/events/:id** - Event details and schedule
- **/calendar** - Calendar view of all events/activities
- **/profile** - User profile management

#### Management Pages (Organizers)

- **/events/new** - Create new event
- **/events/:id/edit** - Edit existing event
- **/events/:id/manage-schedule** - Manage schedule (editable calendar)
- **/my-organized-events** - List of organized events
- **/manage-turmas** - Manage classes (professors/organizers)

#### Participation Pages

- **/my-inscriptions** - Events I am registered for
- **/my-submissions** - Papers I submitted
- **/submit/:eventId** - Paper submission form

#### Legal Pages

- **/terms-of-use** - Platform terms of use
- **/privacy-policy** - Privacy policy (LGPD)

## 🧮 Database Models

### Model Summary

For full details on the relational schema, including relationships, constraints, and data types, refer to [`database_schema.md`](./database_schema.md).

#### User

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.SmallInteger, nullable=False, default=3)  # 1=Org, 2=Author, 3=Part, 4=Prof
    allow_public_profile = db.Column(db.Boolean, nullable=False, default=False)
    reset_token = db.Column(db.String(256), nullable=True)
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"), nullable=True)
    turma_id = db.Column(db.Integer, db.ForeignKey("turma.id"), nullable=True)
```

#### Event

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
    status = db.Column(db.SmallInteger, nullable=False, default=1)  # 1=Draft, 2=Published
    submission_start_date = db.Column(db.DateTime, nullable=True)
    submission_end_date = db.Column(db.DateTime, nullable=True)
    workload = db.Column(db.Integer, nullable=True, default=0)
    faculdade_id = db.Column(db.Integer, db.ForeignKey("faculdade.id"), nullable=True)
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"), nullable=True)
    turma_id = db.Column(db.Integer, db.ForeignKey("turma.id"), nullable=True)
```

#### Academic Hierarchy

- **Faculty** → **Course** → **Class** → **User**
- System populated automatically via a CSV file of Brazilian faculties
- Support for creating custom courses and classes dynamically

## 🔧 Advanced Configuration

### Detailed Environment Variables

```env
# Flask Core
SECRET_KEY=minimum-32-character-secret-key
FLASK_APP=run.py
FLASK_ENV=development  # development, production, testing

# Database
SQLALCHEMY_DATABASE_URI=postgresql://user:password@host:port/database
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_ECHO=False  # Set True to debug SQL

# Email (SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your-email@domain.com
MAIL_PASSWORD=app-specific-password
MAIL_DEFAULT_SENDER=noreply@eventum.com

# File Uploads
UPLOADED_FILES_DEST=/app/backend/app/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB

# Security
SESSION_COOKIE_SECURE=False  # True in production with HTTPS
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### PostgreSQL Setup

```sql
-- Create the database
CREATE DATABASE eventumdb;

-- Create the user
CREATE USER postgres WITH PASSWORD 'password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE eventumdb TO postgres;
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Database Connection Error

```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```

**Solutions:**

- Check whether the PostgreSQL container is running: `docker-compose ps`
- Check logs: `docker-compose logs db`
- Reset the database: `docker-compose down -v && docker-compose up --build`

#### 2. Migration Error

```
alembic.util.exc.CommandError: Can't locate revision identified by 'head'
```

**Solutions:**

- Reset migrations: `rm -rf backend/migrations/versions/*`
- Recreate them: `flask db migrate && flask db upgrade`

#### 3. Frontend Does Not Load

```
Failed to load resource: net::ERR_CONNECTION_REFUSED
```

**Solutions:**

- Check whether the frontend container is running
- Check CORS in the backend
- Check `VITE_API_BASE_URL` in the frontend

#### 4. File Upload Fails

```
The file is too large
```

**Solutions:**

- Increase `MAX_CONTENT_LENGTH` in Flask
- Check permissions on the uploads folder
- Check available disk space in the container

#### 5. Emails Are Not Sent

```
smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted')
```

**Solutions:**

- Use a Gmail app password
- Check SMTP settings
- Check firewall/antivirus settings

### Logs and Debugging

#### View Container Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs web

# Follow logs in real time
docker-compose logs -f web
```

#### Flask Debug

```bash
# Enable debug mode
export FLASK_ENV=development
export FLASK_DEBUG=1

# View SQL queries
export SQLALCHEMY_ECHO=True
```

#### Vue.js Debug

```bash
cd frontend
npm run dev -- --debug
```

### Useful Development Commands

```bash
# Full environment reset
docker-compose down -v
docker system prune -f
docker-compose up --build

# Access container
docker-compose exec web bash

# Run tests (if implemented)
docker-compose exec web python -m pytest

# Backup the database
docker-compose exec db pg_dump -U postgres eventumdb > backup.sql

# Restore the database
docker-compose exec -T db psql -U postgres eventumdb < backup.sql
```

## 🧾 Project Progress Report

### 📍 Current Status

**Eventum** implements **all main functional requirements (RF01–RF04)** and the **business rules** described in the DVP, as well as extra features such as academic affiliations, attendance tracking, digital certificates, and LGPD compliance.

### 🧱 Architecture and Design

- **Backend**: REST API with Flask, MVC architecture, authentication via Flask-Login, CORS support for SPA.
- **Frontend**: Single Page Application with Vue 3, Vuetify 3 for modern UI, Vue Router for navigation, Axios for API communication.
- **Database**: PostgreSQL with migrations via Alembic, support for complex relationships and academic hierarchy.
- **Containerization**: Docker Compose for development and production, with volumes for data persistence.
- **Security**: Password hashing with Werkzeug, input validation, role-based access control, upload sanitization.

### 📊 Project Metrics

- **Lines of Code**: ~5000+ (Backend: ~3000, Frontend: ~2000)
- **Feature Coverage**: 100% of the main RFs + extras
- **Database Tables**: 9 (8 entities + 1 associative table)
- **API Endpoints**: 25+ REST routes
- **Frontend Pages**: 15+ Vue views
- **Technologies**: 15+ libraries/frameworks

## 🧩 Next Steps (Backlog)

### 1. Calendar Improvements

- Add popups with activity details when clicked
- Support for recurring events or repeated activities
- Visualization of time conflicts
- Export calendar to iCal/Google Calendar
- Bidirectional synchronization with Google Calendar

### 2. Automated Email Notifications

- Customizable email template system
- Browser push notifications for event changes
- Automatic reminders (24 hours before the event)
- Weekly reports for organizers

### 3. Academic Affiliation Improvements

- Integration with external APIs (MEC, CNPq) for validation
- Reports by faculty/course (participation statistics)
- Recommendation system based on academic profile
- Bulk import of students/classes via CSV/Excel

### 4. Real-Time Notifications

- WebSockets with Socket.IO for live updates
- Native push notifications for mobile browsers
- Integrated chat between participants and organizers
- User online status

### 5. Internationalization (i18n)

- Support for multiple languages (PT, EN, ES)
- Dynamic translation interface
- Date/currency formatting by locale
- RTL support for Arabic/Hebrew

### 6. Accessibility and UX

- WCAG 2.1 compliance (A, AA, AAA levels)
- Support for screen readers and keyboard navigation
- Usability testing with real users
- Automatic dark/light mode

### 7. Reporting and Analytics

- Dashboards with real-time metrics
- Export reports in PDF/Excel/CSV
- Trend and forecast analysis with ML
- Google Analytics integration

### 8. Payment Integration

- Support for paid registrations (Stripe, PagSeguro, Mercado Pago)
- Dynamic pricing system
- Automatic refunds for cancellations
- Integration with financial management systems

### 9. Public API and Integrations

- Complete OpenAPI/Swagger documentation
- Webhooks for external integrations
- OAuth 2.0 for third-party authentication
- SDKs for integration with other systems

### 10. Mobile and PWA

- Progressive Web App (PWA) for native installation
- Full optimization for mobile devices
- Native push notifications
- Offline support for event viewing

### 11. Gamification and Engagement

- Point/badge system for active participation
- Rankings for most popular events
- Digital certificates with QR codes
- Referral and recommendation system

### 12. Security and Compliance

- Full audit logging for LGPD
- Two-factor authentication (2FA/TOTP)
- End-to-end encryption for sensitive data
- Penetration testing and security audits

## 🔧 Refactors and Technical Optimizations

### Backend

- **Separation of Concerns**: Extract business logic into services/layers
- **Async/Await**: Migrate I/O operations to asynchronous workflows
- **Cache**: Redis for frequent query caching
- **Tests**: Full coverage with pytest
- **API Versioning**: Version endpoints (/api/v1/)
- **Rate Limiting**: Flask-Limiter to protect against abuse

### Frontend

- **Componentization**: Break large components into smaller ones
- **State Management**: Pinia/Vuex for complex state
- **Lazy Loading**: Load routes/components on demand
- **Performance**: Code splitting and tree shaking
- **Tests**: E2E with Playwright

### Database

- **Indexes**: Optimize queries with appropriate indexes
- **Partitioning**: For large tables (logs, audit)
- **Automated Backups**: Robust backup strategies

### DevOps

- **CI/CD**: GitHub Actions for testing and deployment
- **Monitoring**: Prometheus + Grafana
- **Containerization**: Multi-stage builds for production
- **Orchestration**: Kubernetes for scalability

## 💡 Future Advanced Improvements

- **AI/ML**: Personalized recommendations using machine learning
- **Blockchain**: Immutable certificates for submissions
- **VR/AR**: Immersive experiences for virtual events
- **IoT**: Physical access control via RFID/NFC

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **André Sichelero** - Main development

_Last updated: October 2025_
