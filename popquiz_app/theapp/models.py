from theapp import  db


class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(32), unique=True,nullable=False)
  password = db.Column(db.String(128))
  identity = db.Column(db.String(16))
