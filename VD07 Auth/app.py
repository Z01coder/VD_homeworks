from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# База данных пользователей прямо здесь будет храниться
users_db = {}

# Класс - пользователь
class User(UserMixin):
    def __init__(self, id, email, password, name=None):
        self.id = id
        self.email = email
        self.password = password
        self.name = name or "User"  # default name if none provided

# Декоратор загрузки пользователя по ID
@login_manager.user_loader
def load_user(user_id):
    return users_db.get(user_id)

# Форма регистрации
class RegisterForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Форма входа
class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Login')

# Форма редактирования профиля
class EditProfileForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    new_password = PasswordField('Новый пароль')
    confirm_new_password = PasswordField('Подтвердите пароль', validators=[EqualTo('new_password')])
    submit = SubmitField('Сохранить изменения')

# Руты
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        if email in [user.email for user in users_db.values()]:
            flash('Такой пользователь уже зарегистрирован.')
            return redirect(url_for('register'))
        user = User(id=str(len(users_db) + 1), email=email, password=form.password.data)
        users_db[user.id] = user
        flash('Успешная регистрация! Теперь вы можете войти.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = next((u for u in users_db.values() if u.email == email), None)
        if user and user.password == form.password.data:
            login_user(user)
            flash('Вход успешно выполнен!')
            return redirect(url_for('protected'))
        flash('Неверная почта или пароль.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.')
    return redirect(url_for('home'))

@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html', user=current_user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        if form.new_password.data:
            current_user.password = form.new_password.data
        flash('Профиль успешно обновлен!')
        return redirect(url_for('protected'))

    form.name.data = current_user.name
    form.email.data = current_user.email
    return render_template('edit_profile.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
