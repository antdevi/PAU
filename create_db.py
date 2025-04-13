from pau import create_app
from pau.models.models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database created successfully.")