from flask import request
from flask_restful import Resource
from theapp.models import User,Classroom,Comment
from theapp.user import user_bp,user_api
from flask import render_template
from theapp import models
from theapp import db
@user_bp.route('/')
def index():
    return "hello"

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
@user_bp.route('/queryclass/', methods=['POST'])
def queryclass():
    data = request.get_json()
    #print(data)
    name=data.get('name')
    classroom = Classroom.query.filter(Classroom.name == name).first()
    if classroom:
       return {'status': 200, 'classId': classroom.classId}
    else:
       return {'status': 200, 'msg': "您还未设置课堂码，请先设置"}
@user_bp.route('/setclass/', methods=['POST'])
def setclass():
    # name=request.get_json().get('name')
    # classId=request.get_json.get('classId')
    data = request.get_json()
    print(data)
    name=data.get('name')
    classId = data.get('classId')
    if not all([name, classId]):
      return {'status': 400, 'msg': '参数不完整'}
    try:
      classroom= Classroom.query.filter(Classroom.name == name).first()
    except:
      pass
    if classroom:
         #print(classId)
         classroom.classId = classId
         db.session.commit()
         return {'status': 200, 'msg': '课堂码已更改'}
    else:
        classroom=models.Classroom(name=name,classId=classId)
        db.session.add(classroom)  
        db.session.commit()  
        return {'status': 200, 'msg': '注册成功'}
    
@user_bp.route('/joinclass/', methods=['POST'])
def joinclass():
   data = request.get_json()
   name = data.get('name')
   classId = data.get('classId')
   if not all([name, classId]):
      return {'status': 400, 'msg': '参数不完整'}
   try:
      classroom= Classroom.query.filter(Classroom.name == name).first()
   except:
      pass
   if classroom:
      # print(type(classroom.classId), classroom.classId)
      # print(type(classId), classId)
      if classroom.classId == classId:
        # print('111')
        return {'status': 200, 'msg': '课堂加入成功'}
      else:
         return {'status': 400, 'msg': '课堂码错误，请检查输入'}
   else:
      return {'status': 400, 'msg': '课堂不存在，请检查老师名称是否正确'}
@user_bp.route('/getcomment/',methods=['POST'])
def getcomment():
   # 获取数据库中的所有评论
    data = request.get_json()
    name = data.get('name')
    classId = data.get('classId')
    comments = Comment.query.filter(Comment.name==name,Comment.classId==classId).all()
    comments_list = []
    print(classId)
    print(name)

    # 将查询结果转换为字典列表
    for comment in comments:
        comments_list.append({
            'id': comment.id,
            'username': comment.username,
            'text': comment.text,
        })
    print(comments_list)
    return {'status': 200, 'data': comments_list}
@user_bp.route('/addcomment/', methods=['POST'])
def addcomment():
   data = request.get_json()
   username = data.get('username')
   name = data.get('name')
   text = data.get('text')
   classId = data.get('classId')
   comment=models.Comment(username=username,text=text,classId=classId,name=name)
   db.session.add(comment)
   db.session.commit()
   return  {'status': 200, 'msg': '评论成功'}

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