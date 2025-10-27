import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import db, app
from app.models import Faculdade, Curso, Turma, User, Event, Activity, Submission

def populate_test_data():
    """Popula o banco com dados de teste."""

    # Verificar se já foi populado
    with db.session.no_autoflush:
        if Event.query.filter_by(title="Semana da Tecnologia 2025").first():
            print("Dados de teste já populados.")
            return

    # Usar faculdades existentes
    faculdade_objects = Faculdade.query.all()
    if not faculdade_objects:
        print("Nenhuma faculdade encontrada. Execute populate_faculdades primeiro.")
        return

    # Usar cursos existentes
    curso_objects = Curso.query.all()
    if not curso_objects:
        print("Nenhum curso encontrado. Execute populate_cursos primeiro.")
        return

    # 3. Adicionar Turmas
    turmas = [
        {"name": "Turma 2025/1 - A", "academic_year": "2025/2026", "semester": 1, "is_public": True, "curso_id": curso_objects[0].id},
        {"name": "Turma 2025/1 - B", "academic_year": "2025/2026", "semester": 1, "is_public": True, "curso_id": curso_objects[1 % len(curso_objects)].id},
        {"name": "Turma 2025/1 - C", "academic_year": "2025/2026", "semester": 1, "is_public": False, "curso_id": curso_objects[2 % len(curso_objects)].id},
        {"name": "Turma 2025/1 - D", "academic_year": "2025/2026", "semester": 1, "is_public": True, "curso_id": curso_objects[3 % len(curso_objects)].id},
        {"name": "Turma 2025/1 - E", "academic_year": "2025/2026", "semester": 1, "is_public": True, "curso_id": curso_objects[4 % len(curso_objects)].id},
        {"name": "Turma 2025/1 - F", "academic_year": "2025/2026", "semester": 1, "is_public": False, "curso_id": curso_objects[5 % len(curso_objects)].id},
        {"name": "Turma 2025/2 - A", "academic_year": "2025/2026", "semester": 2, "is_public": True, "curso_id": curso_objects[0].id},  # Mesmo curso que A
        {"name": "Turma 2025/2 - B", "academic_year": "2025/2026", "semester": 2, "is_public": True, "curso_id": curso_objects[1 % len(curso_objects)].id},  # Mesmo curso que B
        {"name": "Turma 2024/2 - C", "academic_year": "2024/2025", "semester": 2, "is_public": False, "curso_id": curso_objects[6 % len(curso_objects)].id},  # Curso diferente
        {"name": "Turma 2024/1 - D", "academic_year": "2024/2025", "semester": 1, "is_public": True, "curso_id": curso_objects[7 % len(curso_objects)].id},  # Curso diferente
        {"name": "Turma 2025/1 - G", "academic_year": "2025/2026", "semester": 1, "is_public": True, "curso_id": curso_objects[8 % len(curso_objects)].id},  # Novo curso
        {"name": "Turma 2025/1 - H", "academic_year": "2025/2026", "semester": 1, "is_public": False, "curso_id": curso_objects[9 % len(curso_objects)].id},  # Novo curso
    ]

    turma_objects = []
    for turma_data in turmas:
        # Verificar se já existe
        existing = Turma.query.filter_by(name=turma_data["name"], curso_id=turma_data["curso_id"]).first()
        if not existing:
            turma = Turma(**turma_data)
            db.session.add(turma)
            turma_objects.append(turma)
        else:
            turma_objects.append(existing)
    db.session.commit()

    # 4. Adicionar Usuários
    users = [
        {"name": "João Silva", "email": "joao@exemplo.com", "role": 1, "allow_public_profile": True, "curso_id": curso_objects[0].id, "turma_id": turma_objects[0].id},  # Organizer
        {"name": "Maria Santos", "email": "maria@exemplo.com", "role": 2, "allow_public_profile": True, "curso_id": curso_objects[1 % len(curso_objects)].id, "turma_id": turma_objects[1].id},  # Speaker
        {"name": "Pedro Oliveira", "email": "pedro@exemplo.com", "role": 3, "allow_public_profile": False, "curso_id": curso_objects[2 % len(curso_objects)].id, "turma_id": turma_objects[2].id},  # Participant
        {"name": "Ana Costa", "email": "ana@exemplo.com", "role": 4, "allow_public_profile": True, "curso_id": curso_objects[3 % len(curso_objects)].id, "turma_id": turma_objects[3].id},  # Professor
        {"name": "Carlos Lima", "email": "carlos@exemplo.com", "role": 3, "allow_public_profile": True, "curso_id": curso_objects[4 % len(curso_objects)].id, "turma_id": turma_objects[4].id},  # Participant
        {"name": "Beatriz Rocha", "email": "beatriz@exemplo.com", "role": 2, "allow_public_profile": False, "curso_id": curso_objects[5 % len(curso_objects)].id, "turma_id": turma_objects[5].id},  # Speaker
        {"name": "Fernando Alves", "email": "fernando@exemplo.com", "role": 1, "allow_public_profile": True, "curso_id": curso_objects[6 % len(curso_objects)].id},  # Organizer
        {"name": "Gabriela Pereira", "email": "gabriela@exemplo.com", "role": 3, "allow_public_profile": True, "curso_id": curso_objects[0].id, "turma_id": turma_objects[0].id},  # Participant
        # Novos participantes com variações
        {"name": "Lucas Mendes", "email": "lucas@exemplo.com", "role": 3, "allow_public_profile": True, "curso_id": turma_objects[0].curso_id, "turma_id": turma_objects[0].id},  # Mesmo curso e turma que João e Gabriela
        {"name": "Sofia Almeida", "email": "sofia@exemplo.com", "role": 3, "allow_public_profile": False, "curso_id": turma_objects[0].curso_id, "turma_id": turma_objects[0].id},  # Mesmo curso e turma
        {"name": "Rafael Souza", "email": "rafael@exemplo.com", "role": 3, "allow_public_profile": True, "curso_id": turma_objects[0].curso_id, "turma_id": turma_objects[6].id},  # Mesmo curso, turma diferente (2025/2 - A)
        {"name": "Isabela Ferreira", "email": "isabela@exemplo.com", "role": 3, "allow_public_profile": True, "curso_id": turma_objects[1].curso_id, "turma_id": turma_objects[1].id},  # Mesmo curso que Maria, turma B
        {"name": "Mateus Silva", "email": "mateus@exemplo.com", "role": 3, "allow_public_profile": False, "curso_id": turma_objects[1].curso_id, "turma_id": turma_objects[7].id},  # Mesmo curso, turma diferente (2025/2 - B)
        {"name": "Camila Santos", "email": "camila@exemplo.com", "role": 3, "allow_public_profile": True, "curso_id": turma_objects[2].curso_id, "turma_id": turma_objects[2].id},  # Mesmo curso que Pedro, turma C
        {"name": "Gustavo Oliveira", "email": "gustavo@exemplo.com", "role": 3, "allow_public_profile": True, "curso_id": turma_objects[3].curso_id, "turma_id": turma_objects[3].id},  # Mesmo curso que Ana, turma D
        {"name": "Larissa Costa", "email": "larissa@exemplo.com", "role": 3, "allow_public_profile": False, "curso_id": turma_objects[4].curso_id, "turma_id": turma_objects[4].id},  # Mesmo curso que Carlos, turma E
        {"name": "Thiago Lima", "email": "thiago@exemplo.com", "role": 3, "allow_public_profile": True, "curso_id": turma_objects[5].curso_id, "turma_id": turma_objects[5].id},  # Mesmo curso que Beatriz, turma F
        {"name": "Amanda Rocha", "email": "amanda@exemplo.com", "role": 3, "allow_public_profile": True, "curso_id": turma_objects[8].curso_id, "turma_id": turma_objects[8].id},  # Curso diferente (2024/2 - C)
        {"name": "Bruno Pereira", "email": "bruno@exemplo.com", "role": 3, "allow_public_profile": False, "curso_id": turma_objects[9].curso_id, "turma_id": turma_objects[9].id},  # Curso diferente (2024/1 - D)
        {"name": "Fernanda Alves", "email": "fernanda@exemplo.com", "role": 3, "allow_public_profile": True, "curso_id": turma_objects[10].curso_id, "turma_id": turma_objects[10].id},  # Novo curso G
        {"name": "Roberto Nunes", "email": "roberto@exemplo.com", "role": 3, "allow_public_profile": True, "curso_id": turma_objects[11].curso_id, "turma_id": turma_objects[11].id},  # Novo curso H
        {"name": "Juliana Martins", "email": "juliana@exemplo.com", "role": 3, "allow_public_profile": False, "curso_id": turma_objects[6].curso_id, "turma_id": turma_objects[6].id},  # Mesmo curso que Rafael, turma 2025/2 - A
        {"name": "Diego Carvalho", "email": "diego@exemplo.com", "role": 3, "allow_public_profile": True, "curso_id": turma_objects[7].curso_id, "turma_id": turma_objects[7].id},  # Mesmo curso que Mateus, turma 2025/2 - B
        # Mais professores
        {"name": "Prof. Eduardo Lima", "email": "eduardo@exemplo.com", "role": 4, "allow_public_profile": True, "curso_id": turma_objects[0].curso_id, "turma_id": turma_objects[0].id},  # Professor da turma A
        {"name": "Prof. Carla Mendes", "email": "carla@exemplo.com", "role": 4, "allow_public_profile": False, "curso_id": turma_objects[1].curso_id, "turma_id": turma_objects[1].id},  # Professor da turma B
    ]

    user_objects = []
    for user_data in users:
        user = User(**user_data)
        user.set_password("senha123")
        db.session.add(user)
        user_objects.append(user)
    db.session.commit()

    # 5. Adicionar Eventos
    now = datetime.utcnow()
    events = [
        {
            "title": "Semana da Tecnologia 2025",
            "description": "Evento sobre tecnologias emergentes",
            "start_date": now + timedelta(days=10),
            "end_date": now + timedelta(days=12),
            "inscription_start_date": now,
            "inscription_end_date": now + timedelta(days=9),
            "organizer_id": user_objects[0].id,
            "status": 2,  # Publicado
            "workload": 20,
            "curso_id": curso_objects[0].id,
            "faculdade_id": faculdade_objects[0 % len(faculdade_objects)].id,
        },
        {
            "title": "Congresso de Psicologia",
            "description": "Discussões sobre psicologia moderna",
            "start_date": now + timedelta(days=20),
            "end_date": now + timedelta(days=22),
            "inscription_start_date": now + timedelta(days=5),
            "inscription_end_date": now + timedelta(days=19),
            "organizer_id": user_objects[1].id,
            "status": 2,
            "workload": 15,
            "curso_id": curso_objects[1 % len(curso_objects)].id,
            "faculdade_id": faculdade_objects[1 % len(faculdade_objects)].id,
        },
        {
            "title": "Workshop de Engenharia Civil",
            "description": "Técnicas avançadas em construção",
            "start_date": now + timedelta(days=30),
            "end_date": now + timedelta(days=31),
            "inscription_start_date": now + timedelta(days=10),
            "inscription_end_date": now + timedelta(days=29),
            "organizer_id": user_objects[6].id,
            "status": 1,  # Rascunho
            "workload": 10,
            "curso_id": curso_objects[4 % len(curso_objects)].id,
            "faculdade_id": faculdade_objects[4 % len(faculdade_objects)].id,
        },
        {
            "title": "Simpósio de Física",
            "description": "Avanços em física quântica",
            "start_date": now + timedelta(days=40),
            "end_date": now + timedelta(days=42),
            "inscription_start_date": now + timedelta(days=15),
            "inscription_end_date": now + timedelta(days=39),
            "organizer_id": user_objects[3].id,
            "status": 2,
            "workload": 25,
            "curso_id": curso_objects[3 % len(curso_objects)].id,
            "faculdade_id": faculdade_objects[3 % len(faculdade_objects)].id,
        },
        {
            "title": "Encontro de Direito",
            "description": "Debates sobre legislação atual",
            "start_date": now + timedelta(days=50),
            "end_date": now + timedelta(days=51),
            "inscription_start_date": now + timedelta(days=20),
            "inscription_end_date": now + timedelta(days=49),
            "organizer_id": user_objects[5].id,
            "status": 2,
            "workload": 12,
            "curso_id": curso_objects[5 % len(curso_objects)].id,
            "faculdade_id": faculdade_objects[1 % len(faculdade_objects)].id,
        },
        {
            "title": "Evento de Administração",
            "description": "Gestão e liderança empresarial",
            "start_date": now + timedelta(days=60),
            "end_date": now + timedelta(days=62),
            "inscription_start_date": now + timedelta(days=25),
            "inscription_end_date": now + timedelta(days=59),
            "organizer_id": user_objects[0].id,
            "status": 1,
            "workload": 18,
            "curso_id": curso_objects[6 % len(curso_objects)].id,
            "faculdade_id": faculdade_objects[0 % len(faculdade_objects)].id,
        },
    ]

    event_objects = []
    for event_data in events:
        event = Event(**event_data)
        db.session.add(event)
        event_objects.append(event)
    db.session.commit()

    # 6. Adicionar Atividades para eventos
    activities = [
        # Semana da Tecnologia 2025 (event 0)
        {
            "title": "Palestra: IA Generativa",
            "description": "Introdução à IA generativa",
            "start_time": event_objects[0].start_date + timedelta(hours=9),
            "end_time": event_objects[0].start_date + timedelta(hours=11),
            "location": "Auditório A",
            "event_id": event_objects[0].id,
        },
        {
            "title": "Workshop: Machine Learning",
            "description": "Prática com ML",
            "start_time": event_objects[0].start_date + timedelta(hours=14),
            "end_time": event_objects[0].start_date + timedelta(hours=16),
            "location": "Laboratório 1",
            "event_id": event_objects[0].id,
        },
        {
            "title": "Painel: Ética em IA",
            "description": "Discussão sobre ética na IA",
            "start_time": event_objects[0].start_date + timedelta(hours=17),
            "end_time": event_objects[0].start_date + timedelta(hours=18),
            "location": "Sala de Conferências",
            "event_id": event_objects[0].id,
        },
        # Congresso de Psicologia (event 1)
        {
            "title": "Painel: Psicologia Cognitiva",
            "description": "Discussão sobre cognição",
            "start_time": event_objects[1].start_date + timedelta(hours=10),
            "end_time": event_objects[1].start_date + timedelta(hours=12),
            "location": "Sala 101",
            "event_id": event_objects[1].id,
        },
        {
            "title": "Oficina: Terapia de Grupo",
            "description": "Prática de terapia em grupo",
            "start_time": event_objects[1].start_date + timedelta(hours=14),
            "end_time": event_objects[1].start_date + timedelta(hours=16),
            "location": "Laboratório de Psicologia",
            "event_id": event_objects[1].id,
        },
        # Workshop de Engenharia Civil (event 2)
        {
            "title": "Oficina: Construção Sustentável",
            "description": "Técnicas eco-friendly",
            "start_time": event_objects[2].start_date + timedelta(hours=9),
            "end_time": event_objects[2].start_date + timedelta(hours=12),
            "location": "Campo de Testes",
            "event_id": event_objects[2].id,
        },
        {
            "title": "Palestra: Materiais Inovadores",
            "description": "Novos materiais em construção",
            "start_time": event_objects[2].start_date + timedelta(hours=14),
            "end_time": event_objects[2].start_date + timedelta(hours=15),
            "location": "Auditório B",
            "event_id": event_objects[2].id,
        },
        # Simpósio de Física (event 3)
        {
            "title": "Seminário: Física Quântica",
            "description": "Fundamentos da mecânica quântica",
            "start_time": event_objects[3].start_date + timedelta(hours=13),
            "end_time": event_objects[3].start_date + timedelta(hours=15),
            "location": "Auditório Principal",
            "event_id": event_objects[3].id,
        },
        {
            "title": "Workshop: Experimentos Quânticos",
            "description": "Prática com experimentos",
            "start_time": event_objects[3].start_date + timedelta(hours=16),
            "end_time": event_objects[3].start_date + timedelta(hours=18),
            "location": "Laboratório de Física",
            "event_id": event_objects[3].id,
        },
        {
            "title": "Painel: Aplicações da Física",
            "description": "Discussão sobre aplicações",
            "start_time": event_objects[3].end_date + timedelta(hours=9),
            "end_time": event_objects[3].end_date + timedelta(hours=11),
            "location": "Sala de Seminários",
            "event_id": event_objects[3].id,
        },
        # Encontro de Direito (event 4)
        {
            "title": "Debate: Reforma Jurídica",
            "description": "Análise da legislação atual",
            "start_time": event_objects[4].start_date + timedelta(hours=16),
            "end_time": event_objects[4].start_date + timedelta(hours=18),
            "location": "Sala de Debates",
            "event_id": event_objects[4].id,
        },
        {
            "title": "Palestra: Direitos Humanos",
            "description": "Discussão sobre direitos humanos",
            "start_time": event_objects[4].end_date + timedelta(hours=10),
            "end_time": event_objects[4].end_date + timedelta(hours=12),
            "location": "Auditório Jurídico",
            "event_id": event_objects[4].id,
        },
        # Evento de Administração (event 5)
        {
            "title": "Workshop: Liderança Empresarial",
            "description": "Técnicas de liderança",
            "start_time": event_objects[5].start_date + timedelta(hours=9),
            "end_time": event_objects[5].start_date + timedelta(hours=11),
            "location": "Sala de Reuniões",
            "event_id": event_objects[5].id,
        },
        {
            "title": "Painel: Gestão de Recursos",
            "description": "Discussão sobre gestão",
            "start_time": event_objects[5].start_date + timedelta(hours=14),
            "end_time": event_objects[5].start_date + timedelta(hours=16),
            "location": "Auditório Administrativo",
            "event_id": event_objects[5].id,
        },
        {
            "title": "Oficina: Planejamento Estratégico",
            "description": "Prática de planejamento",
            "start_time": event_objects[5].end_date + timedelta(hours=9),
            "end_time": event_objects[5].end_date + timedelta(hours=12),
            "location": "Laboratório de Estratégia",
            "event_id": event_objects[5].id,
        },
    ]

    activity_objects = []
    for activity_data in activities:
        activity = Activity(**activity_data)
        db.session.add(activity)
        activity_objects.append(activity)
    db.session.commit()

    # 7. Adicionar Inscrições (participantes em eventos)
    inscriptions = [
        # Inscrições existentes
        (user_objects[2], event_objects[0]),  # Pedro no Semana Tech
        (user_objects[4], event_objects[0]),  # Carlos no Semana Tech
        (user_objects[7], event_objects[0]),  # Gabriela no Semana Tech
        (user_objects[2], event_objects[1]),  # Pedro no Congresso Psi
        (user_objects[4], event_objects[3]),  # Carlos no Simpósio Física
        (user_objects[7], event_objects[4]),  # Gabriela no Encontro Direito
        # Novas inscrições variadas
        (user_objects[8], event_objects[0]),  # Lucas no Semana Tech (mesmo curso/turma que João)
        (user_objects[9], event_objects[0]),  # Sofia no Semana Tech
        (user_objects[10], event_objects[0]),  # Rafael no Semana Tech (mesmo curso, turma diferente)
        (user_objects[11], event_objects[1]),  # Isabela no Congresso Psi (mesmo curso que Maria)
        (user_objects[12], event_objects[1]),  # Mateus no Congresso Psi
        (user_objects[13], event_objects[2]),  # Camila no Workshop Eng Civil (mesmo curso que Pedro)
        (user_objects[14], event_objects[3]),  # Gustavo no Simpósio Física (mesmo curso que Ana)
        (user_objects[15], event_objects[3]),  # Larissa no Simpósio Física
        (user_objects[16], event_objects[4]),  # Thiago no Encontro Direito (mesmo curso que Beatriz)
        (user_objects[17], event_objects[4]),  # Amanda no Encontro Direito (curso diferente)
        (user_objects[18], event_objects[5]),  # Bruno no Evento Admin (curso diferente)
        (user_objects[19], event_objects[5]),  # Fernanda no Evento Admin
        (user_objects[20], event_objects[0]),  # Roberto no Semana Tech
        (user_objects[21], event_objects[1]),  # Juliana no Congresso Psi
        (user_objects[22], event_objects[2]),  # Diego no Workshop Eng Civil
    ]

    for user, event in inscriptions:
        user.inscribed_events.append(event)
    db.session.commit()

    # 8. Adicionar Submissões (para eventos com submissões)
    # Primeiro, adicionar datas de submissão a todos os eventos publicados
    for event in event_objects:
        if event.status == 2:
            event.submission_start_date = now
            event.submission_end_date = now + timedelta(days=10)

    submissions = [
        # Evento 0: Semana da Tecnologia 2025
        {
            "title": "Aplicações de IA em Educação",
            "file_path": "ia_educacao.pdf",
            "status": 1,
            "author_id": user_objects[1].id,  # Maria
            "event_id": event_objects[0].id,
        },
        {
            "title": "Machine Learning para Previsão",
            "file_path": "ml_previsao.pdf",
            "status": 3,
            "author_id": user_objects[1].id,
            "event_id": event_objects[0].id,
        },
        {
            "title": "Redes Neurais Avançadas",
            "file_path": "redes_neurais.pdf",
            "status": 4,
            "author_id": user_objects[1].id,
            "event_id": event_objects[0].id,
        },
        {
            "title": "Big Data em Tecnologia",
            "file_path": "big_data_tech.pdf",
            "status": 1,
            "author_id": user_objects[3].id,  # Ana
            "event_id": event_objects[0].id,
        },
        # Evento 1: Congresso de Psicologia
        {
            "title": "Terapia Cognitivo-Comportamental",
            "file_path": "tcc_psicologia.pdf",
            "status": 2,
            "author_id": user_objects[5].id,  # Beatriz
            "event_id": event_objects[1].id,
        },
        {
            "title": "Psicologia do Desenvolvimento",
            "file_path": "desenvolvimento_psico.pdf",
            "status": 1,
            "author_id": user_objects[5].id,
            "event_id": event_objects[1].id,
        },
        {
            "title": "Neuropsicologia Aplicada",
            "file_path": "neuropsicologia.pdf",
            "status": 3,
            "author_id": user_objects[5].id,
            "event_id": event_objects[1].id,
        },
        # Evento 2: Workshop de Engenharia Civil
        {
            "title": "Construção Sustentável",
            "file_path": "construcao_sustentavel.pdf",
            "status": 1,
            "author_id": user_objects[2].id,  # Pedro
            "event_id": event_objects[2].id,
        },
        {
            "title": "Materiais Inovadores em Engenharia",
            "file_path": "materiais_engenharia.pdf",
            "status": 2,
            "author_id": user_objects[2].id,
            "event_id": event_objects[2].id,
        },
        # Evento 3: Simpósio de Física
        {
            "title": "Física Quântica Avançada",
            "file_path": "fisica_quantica.pdf",
            "status": 1,
            "author_id": user_objects[4].id,  # Carlos
            "event_id": event_objects[3].id,
        },
        {
            "title": "Experimentos em Física Moderna",
            "file_path": "experimentos_fisica.pdf",
            "status": 3,
            "author_id": user_objects[4].id,
            "event_id": event_objects[3].id,
        },
        # Evento 4: Encontro de Direito
        {
            "title": "Reforma Jurídica Contemporânea",
            "file_path": "reforma_juridica.pdf",
            "status": 1,
            "author_id": user_objects[6].id,  # Daniel
            "event_id": event_objects[4].id,
        },
        {
            "title": "Direitos Humanos no Século XXI",
            "file_path": "direitos_humanos.pdf",
            "status": 2,
            "author_id": user_objects[6].id,
            "event_id": event_objects[4].id,
        },
        # Evento 5: Evento de Administração
        {
            "title": "Liderança Empresarial Moderna",
            "file_path": "lideranca_empresarial.pdf",
            "status": 1,
            "author_id": user_objects[7].id,  # Gabriela
            "event_id": event_objects[5].id,
        },
        {
            "title": "Gestão Estratégica de Recursos",
            "file_path": "gestao_recursos.pdf",
            "status": 3,
            "author_id": user_objects[7].id,
            "event_id": event_objects[5].id,
        },
    ]

    submission_objects = []
    for sub_data in submissions:
        sub = Submission(**sub_data)
        db.session.add(sub)
        submission_objects.append(sub)
    db.session.commit()

    # 9. Adicionar Check-ins (presença em atividades)
    checkins = [
        (user_objects[2], activity_objects[0]),  # Pedro na palestra IA
        (user_objects[4], activity_objects[0]),  # Carlos na palestra IA
        (user_objects[2], activity_objects[2]),  # Pedro no painel psicologia
        (user_objects[4], activity_objects[4]),  # Carlos no seminário física
    ]

    for user, activity in checkins:
        user.attended_activities.append(activity)
    db.session.commit()

    print("Dados de teste populados com sucesso!")

if __name__ == "__main__":
    with app.app_context():
        populate_test_data()