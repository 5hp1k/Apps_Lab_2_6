from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from task11 import Base, Jobs


app = Flask(__name__, template_folder='.')

engine = create_engine('sqlite:///mars_explorer.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def show_jobs():
    all_jobs = session.query(Jobs).all()

    return render_template('templates/task13.html', jobs=all_jobs)


if __name__ == '__main__':
    app.run(debug=True)
