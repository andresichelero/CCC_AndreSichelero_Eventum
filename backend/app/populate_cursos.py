import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import db, app
from app.models import Faculdade, Curso
import csv

def populate_faculdades():
    """Popula faculdades do CSV se não existirem."""
    if Faculdade.query.count() > 0:
        print("Faculdades já populadas.")
        return

    try:
        with open("app/faculdades.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=1):
                name = row.get("name", "")
                sigla = row.get("sigla", "")
                state = row.get("state", "")
                full_name = f"{name} ({sigla})" if sigla else name
                faculdade = Faculdade(
                    id=i,
                    name=full_name,
                    description="",
                    address=state
                )
                db.session.add(faculdade)
            db.session.commit()
            print("Faculdades populadas.")
    except FileNotFoundError:
        print("Arquivo faculdades.csv não encontrado.")

def populate_cursos():
    """Popula cursos comuns."""
    if Curso.query.count() > 0:
        print("Cursos já populados.")
        return

    # Lista de cursos comuns baseada na Wikipedia
    cursos_comuns = [
        # Ciências Exatas e da Terra
        "Matemática",
        "Álgebra",
        "Lógica Matemática",
        "Teoria dos Números",
        "Geometria",
        "Geometria Algébrica",
        "Topologia",
        "Análise",
        "Equações Diferenciais",
        "Probabilidade",
        "Estatística",
        "Inferência Estatística",
        "Análise de Dados",
        "Ciência da Computação",
        "Teoria da Computação",
        "Linguagens de Programação",
        "Engenharia de Software",
        "Banco de Dados",
        "Sistemas de Informação",
        "Inteligência Artificial",
        "Engenharia de Computação",
        "Engenharia de Telecomunicações",
        "Engenharia de Controle e Automação",
        "Engenharia de Sistemas",
        "Ciência de Dados",
        "Astronomia",
        "Astrofísica",
        "Física",
        "Física Quântica",
        "Relatividade",
        "Física Nuclear",
        "Química",
        "Química Orgânica",
        "Química Inorgânica",
        "Físico-Química",
        "Geoquímica",
        "Geociências",
        "Geologia",
        "Geofísica",
        "Meteorologia",
        "Oceanografia Física",
        "Cartografia",
        # Ciências Biológicas
        "Biologia",
        "Genética",
        "Genética Molecular",
        "Citologia",
        "Embriologia",
        "Histologia",
        "Anatomia",
        "Fisiologia",
        "Neurofisiologia",
        "Bioquímica",
        "Biofísica",
        "Farmacologia",
        "Imunologia",
        "Microbiologia",
        "Virologia",
        "Bacteriologia",
        "Parasitologia",
        "Ecologia",
        "Botânica",
        "Zoologia",
        "Paleontologia",
        # Engenharias
        "Engenharia Civil",
        "Engenharia Sanitária",
        "Engenharia de Transportes",
        "Engenharia de Minas",
        "Engenharia de Materiais",
        "Engenharia Química",
        "Engenharia Nuclear",
        "Engenharia Mecânica",
        "Engenharia de Produção",
        "Engenharia Naval e Oceânica",
        "Engenharia Aeroespacial",
        "Engenharia Elétrica",
        "Engenharia Biomédica",
        "Engenharia de Energia",
        "Engenharia Ambiental",
        # Ciências da Saúde
        "Medicina",
        "Cirurgia",
        "Psiquiatria",
        "Odontologia",
        "Ortodontia",
        "Endodontia",
        "Farmácia",
        "Farmacognosia",
        "Enfermagem",
        "Nutrição",
        "Epidemiologia",
        "Fonoaudiologia",
        "Fisioterapia",
        "Terapia Ocupacional",
        "Educação Física",
        "Biomedicina",
        "Ciências Biológicas Aplicadas",
        # Ciências Agrárias
        "Agronomia",
        "Engenharia Florestal",
        "Engenharia Agrícola",
        "Zootecnia",
        "Medicina Veterinária",
        "Engenharia de Pesca",
        "Engenharia de Alimentos",
        # Ciências Sociais Aplicadas
        "Direito",
        "Teoria do Direito",
        "Direito Penal",
        "Direito Civil",
        "Direito Tributário",
        "Administração",
        "Ciências Contábeis",
        "Economia",
        "Teoria Econômica",
        "Arquitetura e Urbanismo",
        "Biblioteconomia",
        "Arquivologia",
        "Museologia",
        "Comunicação",
        "Jornalismo",
        "Publicidade e Propaganda",
        "Rádio e Televisão",
        "Relações Públicas",
        "Serviço Social",
        "Desenho Industrial",
        "Turismo",
        "Marketing",
        "Gestão de Recursos Humanos",
        # Ciências Humanas
        "Filosofia",
        "História",
        "História Antiga",
        "História Medieval",
        "História Moderna",
        "História Contemporânea",
        "Geografia",
        "Geografia Humana",
        "Geografia Física",
        "Psicologia",
        "Psicologia Experimental",
        "Psicologia Social",
        "Educação",
        "Pedagogia",
        "Ciência Política",
        "Sociologia",
        "Antropologia",
        "Arqueologia",
        "Teologia",
        # Linguística, Letras e Artes
        "Linguística",
        "Letras",
        "Língua Portuguesa",
        "Línguas Estrangeiras",
        "Literatura",
        "Literatura Brasileira",
        "Teoria Literária",
        "Artes",
        "Artes Visuais",
        "Pintura",
        "Escultura",
        "Música",
        "Composição Musical",
        "Dança",
        "Teatro",
        "Dramaturgia",
        "Fotografia",
        "Cinema",
        "Educação Artística",
        "Outros",
    ]

    # Associa a uma faculdade genérica ou primeira faculdade
    faculdade = Faculdade.query.first()
    if not faculdade:
        faculdade = Faculdade(name="Faculdade Genérica", description="Faculdade para cursos gerais")
        db.session.add(faculdade)
        db.session.commit()

    for curso_name in cursos_comuns:
        curso = Curso(
            name=curso_name,
            faculdade_id=faculdade.id,
            description=f"Curso de {curso_name}",
            duration_years=4  # Assumindo 4 anos padrão
        )
        db.session.add(curso)
    db.session.commit()
    print("Cursos populados.")

if __name__ == "__main__":
    with app.app_context():
        populate_faculdades()
        populate_cursos()