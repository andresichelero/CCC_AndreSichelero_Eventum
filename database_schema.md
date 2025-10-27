# 🗂️ Esquema Relacional do Banco de Dados - Eventum

Este documento descreve o esquema relacional do banco de dados PostgreSQL utilizado pela plataforma Eventum, incluindo todas as tabelas, colunas, tipos de dados, restrições e relacionamentos.

## 📊 Diagrama Entidade-Relacionamento (ERD)

```
+----------------+       +-----------------+       +-----------------+
|   Faculdade    |       |      Curso      |       |      Turma      |
+----------------+       +-----------------+       +-----------------+
| id (PK)        |<------| id (PK)         |<------| id (PK)         |
| name           |       | name            |       | name            |
| description    |       | description     |       | academic_year   |
| address        |       | duration_years  |       | semester        |
+----------------+       | faculdade_id (FK)|       | is_public       |
                         +-----------------+       | curso_id (FK)   |
                                                   +-----------------+
                                                          ^
                                                          |
                                                          |
+----------------+       +-----------------+       +-----------------+
|     User       |       |      Event      |       |    Activity     |
+----------------+       +-----------------+       +-----------------+
| id (PK)        |       | id (PK)         |       | id (PK)         |
| name           |       | title           |       | title           |
| email          |       | description     |       | description     |
| password_hash  |       | start_date      |       | start_time      |
| role           |       | end_date        |       | end_time        |
| allow_public   |       | inscription_sd  |       | location        |
| reset_token    |       | inscription_ed  |       | event_id (FK)   |
| curso_id (FK)  |       | organizer_id(FK)|       | check_in_open   |
| turma_id (FK)  |       | status          |       | check_in_code   |
+----------------+       | submission_sd   |       +-----------------+
                         | submission_ed   |               ^
                         | workload        |               |
                         | faculdade_id(FK)|               |
                         | curso_id (FK)   |               |
                         | turma_id (FK)   |               |
                         +-----------------+               |
                                ^                         |
                                |                         |
                                |                         |
+----------------+       +-----------------+       +-----------------+
|  Inscriptions  |       |   Submission    |       |ActivityAttendance|
+----------------+       +-----------------+       +-----------------+
| user_id (PK,FK)|       | id (PK)         |       | user_id (PK,FK) |
| event_id (PK,FK)|       | title           |       | activity_id(PK,FK)
+----------------+       | file_path       |       | check_in_time   |
                         | status          |       +-----------------+
                         | author_id (FK)  |
                         | event_id (FK)   |
                         +-----------------+
```

## 📋 Descrição das Tabelas

### 1. Faculdade

Armazena informações sobre instituições de ensino superior.

| Coluna      | Tipo         | Restrições                  | Descrição              |
| ----------- | ------------ | --------------------------- | ---------------------- |
| id          | INTEGER      | PRIMARY KEY, AUTO_INCREMENT | Identificador único    |
| name        | VARCHAR(200) | UNIQUE, NOT NULL            | Nome da faculdade      |
| description | TEXT         | NULL                        | Descrição da faculdade |
| address     | VARCHAR(300) | NULL                        | Endereço da faculdade  |

**Relacionamentos:**

- 1:N com Curso (uma faculdade tem muitos cursos)
- 1:N com Event (uma faculdade pode organizar muitos eventos)

### 2. Curso

Representa cursos acadêmicos oferecidos pelas faculdades.

| Coluna         | Tipo         | Restrições                  | Descrição              |
| -------------- | ------------ | --------------------------- | ---------------------- |
| id             | INTEGER      | PRIMARY KEY, AUTO_INCREMENT | Identificador único    |
| name           | VARCHAR(200) | NOT NULL                    | Nome do curso          |
| description    | TEXT         | NULL                        | Descrição do curso     |
| duration_years | INTEGER      | NULL                        | Duração em anos        |
| faculdade_id   | INTEGER      | FOREIGN KEY, NOT NULL       | Referência à faculdade |

**Relacionamentos:**

- N:1 com Faculdade
- 1:N com Turma (um curso tem muitas turmas)
- 1:N com User (um curso tem muitos usuários)
- 1:N com Event (um curso pode organizar muitos eventos)

### 3. Turma

Agrupa alunos em classes específicas.

| Coluna        | Tipo         | Restrições                  | Descrição                             |
| ------------- | ------------ | --------------------------- | ------------------------------------- |
| id            | INTEGER      | PRIMARY KEY, AUTO_INCREMENT | Identificador único                   |
| name          | VARCHAR(100) | NOT NULL                    | Nome da turma (ex: "Comp2025/1 - IA") |
| academic_year | VARCHAR(10)  | NULL                        | Ano acadêmico (ex: "2024/2025")       |
| semester      | SMALLINT     | NULL                        | Semestre (1 ou 2)                     |
| is_public     | BOOLEAN      | NOT NULL, DEFAULT FALSE     | Se aparece na lista pública           |
| curso_id      | INTEGER      | FOREIGN KEY, NOT NULL       | Referência ao curso                   |

**Relacionamentos:**

- N:1 com Curso
- 1:N com User (uma turma tem muitos usuários)
- 1:N com Event (uma turma pode organizar muitos eventos)

### 4. User

Usuários do sistema com diferentes papéis.

| Coluna               | Tipo         | Restrições                  | Descrição                                                  |
| -------------------- | ------------ | --------------------------- | ---------------------------------------------------------- |
| id                   | INTEGER      | PRIMARY KEY, AUTO_INCREMENT | Identificador único                                        |
| name                 | VARCHAR(150) | NOT NULL                    | Nome completo                                              |
| email                | VARCHAR(150) | UNIQUE, NOT NULL            | Email do usuário                                           |
| password_hash        | VARCHAR(256) | NULL                        | Hash da senha                                              |
| role                 | SMALLINT     | NOT NULL, DEFAULT 3         | Papel: 1=Organizador, 2=Autor, 3=Participante, 4=Professor |
| allow_public_profile | BOOLEAN      | NOT NULL, DEFAULT FALSE     | Permite perfil público                                     |
| reset_token          | VARCHAR(256) | NULL                        | Token para reset de senha                                  |
| curso_id             | INTEGER      | FOREIGN KEY, NULL           | Referência ao curso                                        |
| turma_id             | INTEGER      | FOREIGN KEY, NULL           | Referência à turma                                         |

**Relacionamentos:**

- N:1 com Curso
- N:1 com Turma
- 1:N com Event (usuário organiza eventos)
- N:N com Event (inscrições via tabela inscriptions)
- 1:N com Submission (usuário submete trabalhos)
- N:N com Activity (presença via tabela activity_attendance)

### 5. Event

Eventos acadêmicos organizados no sistema.

| Coluna                 | Tipo         | Restrições                  | Descrição                       |
| ---------------------- | ------------ | --------------------------- | ------------------------------- |
| id                     | INTEGER      | PRIMARY KEY, AUTO_INCREMENT | Identificador único             |
| title                  | VARCHAR(250) | NOT NULL                    | Título do evento                |
| description            | TEXT         | NULL                        | Descrição do evento             |
| start_date             | DATETIME     | NOT NULL                    | Data/hora de início             |
| end_date               | DATETIME     | NOT NULL                    | Data/hora de fim                |
| inscription_start_date | DATETIME     | NOT NULL                    | Início das inscrições           |
| inscription_end_date   | DATETIME     | NOT NULL                    | Fim das inscrições              |
| organizer_id           | INTEGER      | FOREIGN KEY, NOT NULL       | Organizador do evento           |
| status                 | SMALLINT     | NOT NULL, DEFAULT 1         | Status: 1=Rascunho, 2=Publicado |
| submission_start_date  | DATETIME     | NULL                        | Início das submissões           |
| submission_end_date    | DATETIME     | NULL                        | Fim das submissões              |
| workload               | INTEGER      | NULL, DEFAULT 0             | Carga horária em horas          |
| faculdade_id           | INTEGER      | FOREIGN KEY, NULL           | Faculdade organizadora          |
| curso_id               | INTEGER      | FOREIGN KEY, NULL           | Curso organizador               |
| turma_id               | INTEGER      | FOREIGN KEY, NULL           | Turma organizadora              |

**Relacionamentos:**

- N:1 com User (organizer)
- N:1 com Faculdade
- N:1 com Curso
- N:1 com Turma
- 1:N com Activity (atividades do evento)
- 1:N com Submission (submissões para o evento)
- N:N com User (participantes via tabela inscriptions)

### 6. Activity

Atividades individuais dentro de eventos (palestras, workshops, etc.).

| Coluna        | Tipo         | Restrições                  | Descrição               |
| ------------- | ------------ | --------------------------- | ----------------------- |
| id            | INTEGER      | PRIMARY KEY, AUTO_INCREMENT | Identificador único     |
| title         | VARCHAR(250) | NOT NULL                    | Título da atividade     |
| description   | TEXT         | NULL                        | Descrição da atividade  |
| start_time    | DATETIME     | NOT NULL                    | Data/hora de início     |
| end_time      | DATETIME     | NOT NULL                    | Data/hora de fim        |
| location      | VARCHAR(250) | NULL                        | Local da atividade      |
| event_id      | INTEGER      | FOREIGN KEY, NOT NULL       | Evento ao qual pertence |
| check_in_open | BOOLEAN      | NOT NULL, DEFAULT FALSE     | Se check-in está aberto |
| check_in_code | VARCHAR(10)  | NULL                        | Código para check-in    |

**Relacionamentos:**

- N:1 com Event
- N:N com User (presença via tabela activity_attendance)

### 7. Submission

Submissões de trabalhos acadêmicos para eventos.

| Coluna    | Tipo         | Restrições                  | Descrição                                                    |
| --------- | ------------ | --------------------------- | ------------------------------------------------------------ |
| id        | INTEGER      | PRIMARY KEY, AUTO_INCREMENT | Identificador único                                          |
| title     | VARCHAR(250) | NOT NULL                    | Título do trabalho                                           |
| file_path | VARCHAR(255) | NOT NULL                    | Caminho do arquivo submetido                                 |
| status    | SMALLINT     | NOT NULL, DEFAULT 1         | Status: 1=Submetido, 2=Em avaliação, 3=Aprovado, 4=Rejeitado |
| author_id | INTEGER      | FOREIGN KEY, NOT NULL       | Autor da submissão                                           |
| event_id  | INTEGER      | FOREIGN KEY, NOT NULL       | Evento para o qual foi submetido                             |

**Relacionamentos:**

- N:1 com User (author)
- N:1 com Event

### 8. Inscriptions (Tabela Associativa)

Relacionamento muitos-para-muitos entre usuários e eventos (inscrições).

| Coluna   | Tipo    | Restrições               | Descrição                    |
| -------- | ------- | ------------------------ | ---------------------------- |
| user_id  | INTEGER | PRIMARY KEY, FOREIGN KEY | Usuário inscrito             |
| event_id | INTEGER | PRIMARY KEY, FOREIGN KEY | Evento no qual está inscrito |

**Relacionamentos:**

- N:1 com User
- N:1 com Event

### 9. Activity_Attendance (Tabela Associativa)

Relacionamento muitos-para-muitos entre usuários e atividades (presença/check-in).

| Coluna        | Tipo     | Restrições                | Descrição                      |
| ------------- | -------- | ------------------------- | ------------------------------ |
| user_id       | INTEGER  | PRIMARY KEY, FOREIGN KEY  | Usuário presente               |
| activity_id   | INTEGER  | PRIMARY KEY, FOREIGN KEY  | Atividade na qual fez check-in |
| check_in_time | DATETIME | DEFAULT CURRENT_TIMESTAMP | Momento do check-in            |

**Relacionamentos:**

- N:1 com User
- N:1 com Activity

## 🔗 Chaves Estrangeiras e Restrições

### Índices Recomendados

Para otimizar performance em casos de uso em larga escala, considere criar os seguintes índices:

```sql
-- Índices para buscas frequentes
CREATE INDEX idx_event_status ON event(status);
CREATE INDEX idx_event_start_date ON event(start_date);
CREATE INDEX idx_event_organizer ON event(organizer_id);
CREATE INDEX idx_activity_event ON activity(event_id);
CREATE INDEX idx_submission_event ON submission(event_id);
CREATE INDEX idx_submission_author ON submission(author_id);
CREATE INDEX idx_user_email ON "user"(email);
CREATE INDEX idx_user_role ON "user"(role);

-- Índices compostos para tabelas associativas
CREATE INDEX idx_inscriptions_user_event ON inscriptions(user_id, event_id);
CREATE INDEX idx_activity_attendance_user_activity ON activity_attendance(user_id, activity_id);
```

### Restrições de Integridade Referencial

Todas as chaves estrangeiras têm comportamento padrão:

- ON DELETE: RESTRICT (impede exclusão se houver dependentes)
- ON UPDATE: CASCADE (atualiza referências automaticamente)

## 📈 Estatísticas e Considerações

- **Total de Tabelas**: 9 (8 entidades + 1 tabela associativa adicional)
- **Relacionamentos**: 15 relacionamentos diretos
- **Tabelas Associativas**: 2 (inscriptions, activity_attendance)
- **Hierarquia Acadêmica**: Faculdade → Curso → Turma → User
- **Entidades Principais**: User, Event, Activity, Submission

Este esquema suporta completamente os requisitos funcionais do sistema Eventum, incluindo gestão de usuários com papéis distintos, eventos com programação detalhada, submissões de trabalhos e controle de presença.
