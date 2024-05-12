from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
Base = declarative_base()


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    chief = Column(String)
    members = Column(Integer)
    email = Column(String)


engine = create_engine('sqlite:///mars_explorer.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@app.route('/')
def department_form():
    return render_template('task2.html')


@app.route('/add_department', methods=['POST'])
def add_department():
    session = Session()
    if request.method == 'POST':
        title = request.form['title']
        chief = request.form['chief']
        members = request.form['members']
        email = request.form['email']

        new_department = Department(
            title=title, chief=chief, members=members, email=email)

        session.add(new_department)
        session.commit()
        session.close()

        return redirect(url_for('department_added'))
    else:
        return redirect(url_for('department_form'))


@app.route('/department_added')
def department_added():
    return "Department added successfully!"


if __name__ == '__main__':
    app.run(debug=True)
