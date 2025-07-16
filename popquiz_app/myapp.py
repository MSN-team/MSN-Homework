from flask import Flask, render_template, request, redirect, url_for
from theapp import create_app, db
from flask_migrate import Migrate

app=create_app('development')

Migrate(app, db)

'''
flask db init
flask db migrate 
flask db upgrade
'''
if __name__ == '__main__':
    app.run()
