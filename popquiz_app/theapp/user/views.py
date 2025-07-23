from flask import request
from flask_restful import Resource
from theapp.models import User
from theapp.user import user_bp,user_api
from flask import render_template
from theapp import models
from theapp import db
@user_bp.route('/')
def index():
    return "hello"

# @user_bp.route('/register')
# def register():
#     return render_template('register.html')
# 登录功能
# @user_bp.route('/quiz',methods=['POST'])
# def quiz():
#     sort_field="_id"

#     try:
#         # 按指定字段降序排列并取第一条
#         latest_doc = collection.find().sort(sort_field, -1).limit(1).next()
#         print(f"🔍 最新文档 (按 {sort_field}):")
#         return latest_doc
#     except StopIteration:
#         print("❌ 集合为空")
#         return None
@user_bp.route('/login/', methods=['POST'])
def login():
  # 获取用户名
  # name = request.form.get('name')  
  name = request.get_json().get('name') 
  # 获取密码
  pwd = request.get_json().get('pwd')
  identity = request.get_json().get('identity')
  # nick_name = request.get_json().get('nick_name')
  # 判断是否传递数据完整
  if not all([name, pwd,identity]):
    return {'status': 400, 'msg': '参数不完整'}
  else:
    # 通过用户名获取用户对象
    user = User.query.filter(User.name == name).first()
    # 判断用户是否存在
    if user:
      # 判断密码是否正确
      print(user.name)
      # print(user.pwd)
      # print(pwd)
      # print(user.check_password(pwd))
      if user.check_password(pwd) and user.identity == identity:
        return {'status': 200, 'msg': '登录成功'}
      else:
        return {'status': 400, 'msg': '用户名或密码错误（请注意身份是否正确）'}
    else:
      return {'status': 400, 'msg': '用户名不存在'}
class Users(Resource):
   def get(self):
      pass
   def post(self):
      # name = request.form.get('name')
      # pwd = request.form.get('pwd')
      # real_pwd = request.form.get('real_pwd')
      name = request.get_json().get('name')
      pwd = request.get_json().get('pwd')
      
      real_pwd = request.get_json().get('real_pwd')
      identity = request.get_json().get('identity')
      # nick_name = request.get_json().get('nick_name')
      #验证数据完整性
      if not all([name, pwd,real_pwd]):
        return {'status': 400, 'msg': '参数不完整'}
      if pwd != real_pwd:
        return {'status': 400, 'msg': '两次密码不一致'}
      if len(pwd)<6:
        return {'status': 400, 'msg': '密码长度过小'}
      if len(pwd)>18:
        return {'status': 400, 'msg': '密码长度过长'}
      try:
        #判断用户名是否存在
        user = User.query.filter(User.name==name).first()
      except:
        pass

      if user:
        return {'status': 400, 'msg': '用户名已存在'}
      #创建用户对象
      user = models.User(name=name, password=pwd, identity=identity)
      #保存到数据库
      db.session.add(user)
      db.session.commit()
      return {'status': 200, 'msg': '注册成功'}
user_api.add_resource(Users, '/users/')