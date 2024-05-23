from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import User, Job, engine

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # TODO: Не забыть ключ

Session = sessionmaker(bind=engine)


@app.route('/')
def index():
    if 'user_id' in session:
        user_id = session['user_id']
        db_session = Session()
        jobs = db_session.query(Job).all()
        db_session.close()
        return render_template('main_page.html', user_id=user_id, jobs=jobs)
    return render_template('register.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        speciality = request.form['speciality']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match"

        # hashed_password = generate_password_hash(password)
        hashed_password = password
        new_user = User(
            surname=surname,
            name=name,
            age=age,
            position=position,
            speciality=speciality,
            address=address,
            email=email,
            hashed_password=hashed_password,
            modified_date=datetime.now()
        )

        db_session = Session()
        db_session.add(new_user)
        db_session.commit()
        db_session.close()

        return redirect(url_for('registration_success'))
    return render_template('register.html')  # Рендерим страницу регистрации


@app.route('/registration_success')
def registration_success():
    return "Registration successful!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db_session = Session()
        user = db_session.query(User).filter_by(email=email).first()

        # if user and check_password_hash(user.hashed_password, password):
        if user and user.hashed_password == password:
            session['user_id'] = user.id
            db_session.close()
            return redirect(url_for('index'))
        db_session.close()
        return "Invalid email or password"

    return render_template('login.html')  # Рендерим страницу логина


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
