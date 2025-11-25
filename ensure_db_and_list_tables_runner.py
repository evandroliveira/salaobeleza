from run import create_app
from app.models.db import db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    db.create_all()
    insp = inspect(db.engine)
    print('Tabelas no banco:', insp.get_table_names())
