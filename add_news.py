from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
 
class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    phonenumber = StringField('Номер телефона', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    place = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Добавить')
