import os
from app import app

# Popula o banco de dados se estiver vazio
try:
    with app.app_context():
        from app.populate_cursos import populate_faculdades, populate_cursos
        populate_faculdades()
        populate_cursos()
except Exception as e:
    print(f"Erro ao popular banco: {e}")

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
