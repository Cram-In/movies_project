from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from con_fig import Config


app = Flask(__name__)

app.config.from_object(Config)


db = SQLAlchemy(app)