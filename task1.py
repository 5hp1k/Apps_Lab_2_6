from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # TODO: Не забыть ключ
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)


engine = create_engine('sqlite:///mars_explorer.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@app.route('/')
def index():
    if 'user_id' in session:
        user_id = session['user_id']
        session.close()
        # Главная страница со всеми работами
        return render_template('task2.html', user_id=user_id)
    return render_template('task1.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    session = Session()
    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match"

        hashed_password = generate_password_hash(password)

        new_user = User(surname=surname, name=name, email=email,
                        hashed_password=hashed_password)
        session.add(new_user)
        session.commit()
        session.close()

        return redirect(url_for('index'))
    # Страница регистрации пользователя из Лаб 5
    return render_template('task14_Lab5.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session = Session()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = session.query(User).filter_by(email=email).first()

        if user and check_password_hash(user.hashed_password, password):
            session['user_id'] = user.id
            session.close()
            return redirect(url_for('index'))

        return "Invalid email or password"

    return render_template('task1.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
