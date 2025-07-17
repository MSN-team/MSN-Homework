from flask import Flask, render_template, request, redirect, url_for
from theapp import create_app, db
from flask_migrate import Migrate
from flask_cors import CORS

app=create_app('development')
CORS(app,supports_credentials=True)
Migrate(app, db)

'''
flask db init
flask db migrate 
flask db upgrade
flask db stamp head（将当前版本设置为head）
.\flask_venv\Scripts\Activate
$env:FLASK_APP="myapp"
yarn serve
'''
if __name__ == '__main__':
    app.run()
