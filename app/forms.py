from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, SelectField, TextAreaField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo, NumberRange, email_validator
from app.models import User
import config as  cnfg

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    #Поля с валидаторами
    username = StringField('Имя пользователя', validators=[DataRequired()])
    #Стоит валидатор на проверку того, что это email
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    #Проверка на совпадение с первым паролем
    password2 = PasswordField('Подтверждение пароля',
                              validators=[DataRequired(),
                                          EqualTo('password')])
    favbet_login = StringField('Логин FavBet', validators=[DataRequired()])
    favbet_password = PasswordField('Пароль FavBet', validators=[DataRequired()])
    verify_field = IntegerField('Код верификации', validators=[DataRequired()])
    submit = SubmitField('Зареєструватися')

    def validate_verify_field(self, verify_field):
        if verify_field.data != cnfg.verification_code:
            raise ValidationError("Неверный код верификации")

class FavBetDataForm(FlaskForm):
    username = StringField('Иия пользователя в FavBet', validators=[DataRequired()])
    password = PasswordField('Пароль в FavBet', validators=[DataRequired()])
    submit = SubmitField('Изменить данные')

class UserDataForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Обновить данные')

    def __init__(self, original_username):
        super(UserDataForm,self).__init__()
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Введите другое имя пользователя')

class ImitateCasinoGame(FlaskForm):
    mode = SelectField('Режим', choices=[('retro','Ретроперспектива'),
                                         ('forecasting', 'Прогнозирование')])
    play_schema = SelectField('Схема игры', choices=[('1', '#1. 2 раза на цвет'),
                                                     ('5', '#2. Антимартингейл-цвет'),
                                                     ('2', '#3. Линии'),
                                                     ('3', '#4. Линии на 3 шага назад'),
                                                     ('4', '#5. Линии на 2 шага назад'),
                                                     ('6', '#6. Средняя линия почти 0'),
                                                     ('7', '#7. Средний блок почти 0'),
                                                     ('8', '#8. Средняя линия и блок 0')])
    min_bet = SelectField('Минимальная ставка', choices=[('4', '4'),
                                                         ('10', '10'),
                                                         ('20', '20'),
                                                         ('100', '100'),
                                                         ('500', '500'),
                                                         ('2000', '2000')
                                                         ])
    game_count = IntegerField('Количество игр', validators=[DataRequired(),NumberRange(min=1,max=500)])
    middle0_line = SelectField('Средняя линия/блок', choices=[('middle', 'Средняя линия / Вторые 12'),
                                                              ('min', 'Нижняя линия / Первые 12'),
                                                              ('max', 'Верхняя линия / Третьи 12')])

class BotSettingForm(FlaskForm):
    play_schema = SelectField('Схема игры',choices=[('1', '#1. 2 раза на цвет'),
                                                    ('5', '#2. Антимартингейл-цвет'),
                                                    ('2', '#3. Линии'),
                                                    ('3', '#4. Линии на 3 шага назад'),
                                                    ('4', '#5. Линии на 2 шага назад'),
                                                    ('6', '#6. Средняя линия почти 0'),
                                                    ('7', '#7. Средний блок почти 0'),
                                                    ('8', '#8. Средняя линия и блок 0')])
    play_time = TimeField('Время игры', validators=[DataRequired()])
    min_bet = SelectField('Минимальная ставка', choices=[('4','4'),
                                                         ('10','10'),
                                                         ('20','20'),
                                                         ('100','100'),
                                                         ('500','500'),
                                                         ('2000','2000')
                                                         ])
    bet_info = SelectField('Информирование', choices=[('one_bet', 'По каждой ставке'),
                                                      ('summary_bet', 'Общее по сессии')])
    middle0_line = SelectField('Средняя линия', choices=[('middle', 'Средняя линия'),
                                                         ('min', 'Нижняя линия'),
                                                         ('max', 'Верхняя линия')])
    middle0_block = SelectField('Средний блок', choices=[('middle', 'Вторые 12'),
                                                         ('min', 'Первые 12'),
                                                         ('max', 'Третьи 12')])
    submit = SubmitField('Подтвердить')

    def validate_play_time(self, play_time):
        if play_time.data.hour > 11:
            raise ValidationError("Максимальное значение времени игры - 12 часов.")

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Отправить ссылку на email')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Подтвердите пароль', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Сбросить пароль')

class ChangePassword(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')

class AdminPanelAllUsers(FlaskForm):
    is_admin = SelectField(' ', choices=[('0','Пользователь'),
                                         ('1', 'Администратор')])
    is_active = SelectField(' ', choices=[('0', 'Заблокирован'),
                                          ('1', 'Разблокирован')])
    submit = SubmitField('Подтвердить')