```bash
# 1. 克隆仓库
$ git clone https://github.com/MSN-team/MSN-Homework.git && cd popquiz_app
# 2. 激活虚拟环境
$ .\flask_venv\Scripts\Activate
（或者根据".\MSN-Homework\popquiz_app\test\install_model.txt"中安装相应的包）
# 3. 数据库初始化
$ flask db init && flask db migrate && flask db upgrade
$ Make sure MongoDB is running locally on `mongodb://localhost:27017/`.
# 4. 启动后端（FastAPI + Flask + MongoDB）
$ $env:FLASK_APP="myapp" && python myapp.py 
$ uvicorn main:app --reload
# 5. 启动前端
$ cd popquize_vue
$ yarn serve


---
