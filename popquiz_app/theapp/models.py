from theapp import  db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(object): 
  create_time = db.Column(db.DateTime, default=db.func.now())
  update_time = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class User(db.Model, BaseModel):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(32), unique=True,nullable=False)
  pwd = db.Column(db.String(255))
  identity = db.Column(db.String(16))
  nickname = db.Column(db.String(32))
  
  
  @property
  def password(self):
    return self.pwd

  @password.setter
  #加密
  def password(self,pwd):
    self.pwd = generate_password_hash(pwd)
  def check_password(self, pwd): 
    #检查密码
    return check_password_hash(self.pwd, pwd)
