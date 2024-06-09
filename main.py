from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import User, Job, engine


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # TODO: Не забыть ключ

Session = sessionmaker(bind=engine)


@app.route('/')
def index():
    db_session = Session()
    jobs = db_session.query(Job).all()
    db_session.close()

    if 'user_id' in session:
        user_id = session['user_id']
        db_session = Session()
        user = db_session.query(User).filter_by(id=user_id).first()
        db_session.close()
        return render_template('main_page.html', user=user, jobs=jobs)
    else:
        return render_template('main_page.html', user=None, jobs=jobs)


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
            return "Пароли не совпадают"

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
    return "Вы успешно зарегистрировались!"


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
        return "Неверный email или пароль"

    return render_template('login.html')  # Рендерим страницу логина


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        job_title = request.form['job']
        team_leader = request.form['team_leader']
        work_size = request.form['work_size']
        collaborators = request.form['collaborators']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        is_finished = request.form.get('is_finished') == 'on'
        user_id = session['user_id']

        new_job = Job(
            job=job_title,
            team_leader=team_leader,
            work_size=work_size,
            collaborators=collaborators,
            start_date=datetime.strptime(start_date, '%Y-%m-%d'),
            end_date=datetime.strptime(end_date, '%Y-%m-%d'),
            is_finished=is_finished
        )

        db_session = Session()
        db_session.add(new_job)
        db_session.commit()
        db_session.close()

        return redirect(url_for('index'))

    return render_template('add_job.html')


@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db_session = Session()
    job = db_session.query(Job).filter_by(id=job_id).first()

    if request.method == 'POST':
        job.job = request.form['job']
        job.team_leader = request.form['team_leader']
        job.work_size = request.form['work_size']
        job.collaborators = request.form['collaborators']
        job.start_date = datetime.strptime(
            request.form['start_date'], '%Y-%m-%d')
        job.end_date = datetime.strptime(
            request.form['end_date'], '%Y-%m-%d')
        job.is_finished = request.form.get('is_finished') == 'on'
        db_session.commit()
        db_session.close()
        return redirect(url_for('index'))

    db_session.close()
    return render_template('edit_job.html', job=job)


@app.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db_session = Session()
    job = db_session.query(Job).filter_by(id=job_id).first()
    db_session.delete(job)
    db_session.commit()
    db_session.close()
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
