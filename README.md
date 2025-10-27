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
