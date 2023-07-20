import datetime
import requests
from flask import Flask, request, redirect, abort, jsonify
from flask import render_template, make_response, session
from flask_login import LoginManager, login_user, login_required
from flask_login import logout_user, current_user
from flask_restful import Api
import news_resources
from data import db_session, news_api
from data.news import News
from data.users import User
from forms.add_news import NewsForm
from forms.user import RegisterForm
from loginform import LoginForm
from mail_sender import send_mail