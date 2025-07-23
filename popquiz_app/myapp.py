from flask import Flask, render_template, request, redirect, url_for
from theapp import create_app, db
from flask_migrate import Migrate
from flask_cors import CORS

app=create_app('development')
CORS(app,supports_credentials=True)
Migrate(app, db)


if __name__ == '__main__':
    app.run()
