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

---

## 🚀 Funcionalidades Implementadas

| Módulo | Funcionalidades |
|---------|----------------|
| **Autenticação** | Registro, login e logout de usuários com papéis distintos (Organizador, Autor/Palestrante, Participante). Senhas armazenadas com hash seguro (`werkzeug.security`). Vínculos acadêmicos opcionais (faculdade, curso, turma) com pesquisa e adição dinâmica. |
| **Eventos (RF01)** | CRUD completo: criação, edição, visualização e exclusão de eventos. Apenas organizadores têm permissão para gerenciar eventos. |
| **Inscrições (RF02)** | Participantes podem se inscrever em eventos publicados e dentro do período de inscrição. O sistema evita inscrições duplicadas. Organizadores visualizam a lista de participantes. |
| **Submissões de Trabalhos (RF04)** | Autores podem submeter trabalhos com título e resumo; organizadores podem aprovar ou rejeitar submissões. |
| **Programação (RF03)** | Organizadores podem adicionar, editar e gerenciar atividades com calendário interativo (FullCalendar). Participantes visualizam a programação em grade. Suporte a drag-and-drop para reorganizar horários. |
| **Validação de Regras de Negócio** | Período de inscrição, status de evento (Rascunho/Publicado), validações de data e horário. Calendário impede movimentação para datas passadas ou fora do evento. |
| **Vínculos Acadêmicos** | Sistema de faculdades, cursos e turmas com lista extensa populada automaticamente. Pesquisa em tempo real, adição de cursos/turmas personalizados. Botão de contato para faculdades não listadas. |

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
|------------|-------------|
| **Backend** | Python 3.10, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF, Flask-Mail, Flask-CORS, python-dotenv |
| **Frontend** | Vue 3, Vuetify 3, Vue Router, Axios, FullCalendar, Vite |
| **Banco de Dados** | PostgreSQL |
| **Containerização** | Docker, Docker Compose |
| **Ferramentas** | Vite (build frontend), Alembic (migrações), WeasyPrint (geração de PDFs), Magic (detecção de tipos de arquivo) |

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
│   │   ├── faculdades.csv
│   │   ├── uploads/
│   │   ├── __pycache__/
│   │   └── templates/ (não utilizado, SPA)
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
│   ├── package-lock.json
│   ├── vite.config.js
│   └── .eslintrc.cjs
├── .env.example
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

### 2. Configurar Variáveis de Ambiente
Copie o arquivo `.env.example` para `.env` e configure as variáveis necessárias:
```bash
cp .env.example .env
# Edite .env com suas configurações
```

### 3. Executar com Docker (Recomendado)
```bash
docker-compose up --build
```
- Backend: [http://localhost:5000](http://localhost:5000)
- Frontend: [http://localhost:3000](http://localhost:3000)
- Banco: PostgreSQL em container (porta 5432)

### 4. Popular Dados Iniciais (Opcional)
```bash
docker-compose exec web python backend/populate_cursos.py
```

### 5. Instalação Manual (Alternativa)
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
| GET | `/api/faculdades` | Lista de faculdades | Público |
| GET | `/api/cursos?faculdade_id=<id>` | Lista de cursos por faculdade | Público |
| GET | `/api/turmas?curso_id=<id>` | Lista de turmas por curso | Público |
| POST | `/api/cursos` | Adicionar curso personalizado | Público |
| POST | `/api/turmas` | Adicionar turma personalizada | Público |

### Páginas do Frontend (Vue Router)
- `/` - Home/Dashboard
- `/login` - Login
- `/register` - Registro (com vínculos acadêmicos)
- `/events` - Lista de eventos
- `/events/:id` - Detalhes do evento (com calendário)
- `/events/new` - Criar evento
- `/events/:id/edit` - Editar evento
- `/events/:id/manage-schedule` - Gerenciar programação (calendário editável)
- `/my-inscriptions` - Minhas inscrições
- `/my-submissions` - Minhas submissões
- `/submit/:eventId` - Submeter trabalho
- `/profile` - Perfil do usuário
- `/forgot-password` - Recuperação de senha
- `/reset-password` - Redefinição de senha
- `/terms-of-use` - Termos de uso
- `/privacy-policy` - Política de privacidade

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
    allow_public_profile = db.Column(db.Boolean, nullable=False, default=False)
    reset_token = db.Column(db.String(256), nullable=True)
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"), nullable=True)
    turma_id = db.Column(db.Integer, db.ForeignKey("turma.id"), nullable=True)
```

### Faculdade
```python
class Faculdade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(300), nullable=True)
```

### Curso
```python
class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration_years = db.Column(db.Integer, nullable=True)
    faculdade_id = db.Column(db.Integer, db.ForeignKey("faculdade.id"), nullable=False)
```

### Turma
```python
class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    academic_year = db.Column(db.String(10), nullable=True)
    semester = db.Column(db.SmallInteger, nullable=True)
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"), nullable=False)
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
    faculdade_id = db.Column(db.Integer, db.ForeignKey("faculdade.id"), nullable=True)
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"), nullable=True)
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
O **Eventum** implementa **todos os requisitos funcionais principais (RF01–RF04)** e **regras de negócio** descritas no DVP, além de funcionalidades extras como vínculos acadêmicos e validações aprimoradas. Os módulos estão funcionalmente integrados, com frontend responsivo e calendário interativo.

### 🧱 Estrutura e Arquitetura
- **Backend**: API REST com Flask, arquitetura MVC, autenticação via sessions, suporte a CORS para frontend.
- **Frontend**: SPA com Vue 3, Vuetify 3 para UI moderna, Vue Router para navegação, Axios para API calls.
- **Banco**: PostgreSQL com migrações via Alembic, suporte a relacionamentos complexos.
- **Containerização**: Docker Compose para desenvolvimento e produção, com volumes para persistência.
- **Segurança**: Senhas hasheadas, validações de entrada, controle de acesso por papéis.

---

## 🧩 Próximos Passos (Backlog)

### 1. Melhorias no Calendário
- Adicionar popups com detalhes das atividades ao clicar.
- Suporte a eventos recorrentes ou atividades repetidas.
- Visualização de conflitos de horário.
- Exportar calendário para iCal/Google Calendar.

### 2. Notificações por E-mail Automáticas
- Garantir envio em todas as ações relevantes (registro, inscrição, avaliação de submissões).
- Templates de email customizáveis.
- Sistema de lembretes automáticos (ex: 24h antes do evento).

### 3. Melhorias nos Vínculos Acadêmicos
- Integração com APIs externas para validação de faculdades/cursos (ex: MEC, CNPq).
- Relatórios por faculdade/curso (estatísticas de participação).
- Sistema de recomendações de eventos baseado no perfil acadêmico.
- Importação em lote de alunos/turmas via CSV.

### 4. Notificações em Tempo Real
- Implementar WebSockets (ex: Socket.IO) para atualizações live no calendário e inscrições.
- Notificações push no navegador para mudanças em eventos inscritos.
- Chat integrado para participantes e organizadores.

### 5. Internacionalização (i18n)
- Suporte a múltiplos idiomas (Português, Inglês, Espanhol).
- Interface para tradução dinâmica.
- Formatação de datas e moedas por locale.

### 6. Acessibilidade e UX
- Conformidade completa com WCAG 2.1 (níveis A, AA, AAA).
- Suporte a leitores de tela e navegação por teclado.
- Testes de usabilidade com usuários reais.
- Modo escuro/claro.

### 7. Relatórios e Analytics
- Dashboards para organizadores com métricas (taxa de inscrição, demografia, feedback).
- Exportação de relatórios em PDF/Excel.
- Análise de tendências e previsões.

### 8. Integração com Pagamentos
- Suporte a inscrições pagas via gateways (Stripe, PagSeguro).
- Controle de preços por categoria (estudante, profissional).
- Reembolsos automáticos para cancelamentos.

### 9. API Pública e Integrações
- Documentação OpenAPI/Swagger para API.
- Webhooks para integrações externas (ex: sistemas universitários).
- OAuth 2.0 para autenticação de terceiros.

### 10. Mobile e PWA
- Progressive Web App (PWA) para instalação como app.
- Otimização para dispositivos móveis.
- Notificações push nativas.

### 11. Gamificação e Engajamento
- Sistema de pontos/badges para participação ativa.
- Rankings de eventos mais populares.
- Certificados digitais automáticos via QR code.

### 12. Segurança e Conformidade
- Auditoria de logs para compliance LGPD.
- Two-factor authentication (2FA).
- Encriptação end-to-end para dados sensíveis.

---

## 🔧 Refactors e Otimizações Técnicas

### Backend
- **Separação de Concerns**: Extrair lógica de negócio para services/layers (ex: `EventService`, `UserService`).
- **Async/Await**: Migrar operações I/O para assíncronas (ex: envio de emails).
- **Cache**: Implementar Redis para cache de queries frequentes (ex: lista de eventos).
- **Testes**: Cobertura de testes unitários e integração com pytest.
- **API Versioning**: Versionar endpoints (ex: `/api/v1/events`).
- **Rate Limiting**: Proteger contra abuso com Flask-Limiter.

### Frontend
- **Componentização**: Quebrar componentes grandes em menores e reutilizáveis.
- **State Management**: Introduzir Pinia/Vuex para estado global complexo.
- **Lazy Loading**: Carregar rotas e componentes sob demanda.
- **Performance**: Otimizar bundles com code splitting e tree shaking.
- **Testes**: Adicionar testes E2E com Cypress ou Playwright.

### Banco de Dados
- **Índices**: Otimizar queries com índices apropriados.
- **Particionamento**: Para tabelas grandes (ex: logs de auditoria).
- **Backup Automático**: Estratégias de backup e recuperação.

### DevOps
- **CI/CD**: Pipelines com GitHub Actions para testes e deploy.
- **Monitoramento**: Logs centralizados e métricas (ex: Prometheus).
- **Containerização**: Otimizar Dockerfiles para produção (multi-stage builds).

---

## 💡 Futuras Melhorias Avançadas
- **IA/ML**: Recomendações personalizadas de eventos usando machine learning.
- **Blockchain**: Certificados imutáveis para submissões aprovadas.
- **VR/AR**: Experiências imersivas para eventos virtuais.
- **Integração com IoT**: Controle de acesso físico via RFID/NFC.
- **Sustentabilidade**: Métricas de carbono para eventos híbridos.
