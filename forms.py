from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from sqlalchemy import func
from models import User

class RegistrationForm(FlaskForm):
    name = StringField('Ad Soyad', validators=[
        DataRequired(message='Lütfen adınızı ve soyadınızı girin.'),
        Length(min=2, max=100, message='Ad Soyad en az 2 karakter olmalıdır.')
    ])
    email = StringField('E-posta', validators=[
        DataRequired(message='Lütfen e-posta adresinizi girin.'),
        Email(message='Lütfen geçerli bir e-posta adresi girin.')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Lütfen bir şifre belirleyin.'),
        Length(min=6, message='Şifreniz en az 6 karakter olmalıdır.')
    ])
    confirm_password = PasswordField('Şifreyi Onayla', validators=[
        DataRequired(message='Lütfen şifrenizi tekrar girin.'),
        EqualTo('password', message='Girilen şifreler birbiriyle eşleşmiyor.')
    ])
    submit = SubmitField('Kayıt Ol')

    def validate_email(self, email):
        clean_email = (email.data or '').strip().lower()
        user = User.query.filter(func.lower(User.email) == clean_email).first()
        if user:
            raise ValidationError('Bu e-posta adresi zaten kayıtlı. Lütfen giriş yapın veya şifremi unuttum seçeneğini kullanın.')

class LoginForm(FlaskForm):
    email = StringField('E-posta', validators=[
        DataRequired(message='Lütfen e-posta adresinizi girin.'),
        Email(message='Lütfen geçerli bir e-posta adresi girin.')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Lütfen şifrenizi girin.')
    ])
    submit = SubmitField('Giriş Yap')

