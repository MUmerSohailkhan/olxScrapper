from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError




class  loginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    rememberMe=BooleanField('Remember Me')
    submit=SubmitField('Login')


class scrapperToolForm(FlaskForm):
    platForm=StringField('Platform',validators=[DataRequired(),Email()])
    category=StringField('Category',validators=[DataRequired(),Email()])
    scrap = SubmitField('Scrap')

