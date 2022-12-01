from flask_wtf import FlaskForm
import wtforms as ws
from app import app
from . import models


class EmployeeForm(FlaskForm):
    fullname = ws.StringField('ФИО работника',validators=[ws.validators.DataRequired(),])
    phone = ws.StringField('Номер телефона',validators=[ws.validators.DataRequired(),])
    short_info = ws.TextAreaField('Короткое информация о работнике',validators=[ws.validators.DataRequired(),])
    experience = ws.IntegerField('Опыт работы',validators=[ws.validators.DataRequired(),])
    preferred_position = ws.StringField('Предпочитаемый должность')
    user_id = ws.SelectField('Имя пользователя',choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_choices = []
        with app.app_context():
            for user in models.User.query.all():
                self.user_choices.append((user.id, user.username))
            self._fields['user_id'].choices = self.user_choices

    def validate(self):
        if not super().validate() == True:
            return False

        error_counter = 0

        name_split = self.fullname.data.split(' ')
        if len(name_split) == 1:
            self.fullname.errors.append('В ФИО не может состоять из одного слова')
            error_counter += 1

        for name in self.fullname.data:
            if not name.isalpha() and not ' ' in name:
                self.fullname.errors.append('В ФИО не должно быть спец символы и чисел')
                error_counter += 1

        if error_counter > 0:
            return False
        else:
            return True


class UserForm(FlaskForm):
    username = ws.StringField('Имя пользователя', validators=[ws.validators.DataRequired(), ws.validators.length(min=4, max=20)])
    password = ws.PasswordField('Пароль', validators=[ws.validators.DataRequired(), ws.validators.length(min=8, max=24)])
    submit = ws.SubmitField('Сохранить')

