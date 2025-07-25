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
#change

class Classroom(db.Model, BaseModel):
  __tablename__ = 'classroom'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(32),nullable=False)
  classId = db.Column(db.String(32), unique=True, nullable=False)
  studentNum = db.Column(db.Integer)
  chooseNum = db.Column(db.Integer)
  correntNum = db.Column(db.Integer)

class Comment(db.Model,BaseModel):
  __tablename__ = 'comment'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String(32))
  name =db.Column(db.String(32))
  text = db.Column(db.String(32))
  classId = db.Column(db.String(32))

  # class Comment(db.Model, BaseModel):
  #   __tablename__ = 'comment'
  #   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  #   username = db.Column(db.String(32), db.ForeignKey('user.name'))  # 外键约束，关联到 User 表的 name 字段
  #   teachername = db.Column(db.String(32), db.ForeignKey('user.name'))  # 外键约束，关联到 User 表的 name 字段
  #   text = db.Column(db.String(255))  # 评论内容
  #   classId = db.Column(db.String(32), db.ForeignKey('classroom.classId'))  # 外键约束，关联到 Classroom 表的 classId 字段

  #   # 设置关系
  #   user = db.relationship('User', foreign_keys=[username])
  #   teacher = db.relationship('User', foreign_keys=[teachername])
  #   classroom = db.relationship('Classroom', foreign_keys=[classId])