import random

from flask import Flask, render_template, request, redirect, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import abort, Api

from data import db_session, jobs_resources
from data.jobs import Jobs
from data.users import User
from forms.jobs import JobsForm
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'a really really really really long secret key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/page")
@app.route("/")
def index():
    return redirect("/page/1")


@app.route("/page/<int:page>")
def index_page(page):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).order_by(-Jobs.salary)
    len_jobs = len(db_sess.query(Jobs).all())
    if (page - 1) * 10 > len_jobs:
        abort(404)
    return render_template("index.html", jobs=jobs, page=page, len_jobs=len_jobs, title='SoS')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.title = form.title.data
        jobs.salary = form.salary.data
        jobs.contacts = form.contacts.data
        jobs.content = form.content.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление вакансии',
                           form=form)


@app.route("/job/<int:id>")
def detailed(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    return render_template("detailed.html", job=job)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            form.title.data = jobs.title
            form.content.data = jobs.content
            form.contacts.data = jobs.contacts
            form.salary.data = jobs.salary
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            jobs.title = form.title.data
            jobs.content = form.content.data
            jobs.salary = form.salary.data
            jobs.contacts = form.contacts.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование вакансии',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.user == current_user
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


def create_jobs(db_session):
    for i in range(40):
        job = Jobs()
        job.title = f"Вакансия {i}"
        job.salary = random.randint(10, 100) * 1000
        job.content = f"description {i}"
        job.contacts = f'+79{random.randint(100000000, 999999999)}'
        job.user_id = 1
        db_sess = db_session.create_session()
        db_sess.add(job)
        db_sess.commit()


if __name__ == "__main__":
    db_session.global_init("db/jobs.db")

    # create_jobs(db_session)

    api.add_resource(jobs_resources.JobsListResource, '/api/jobs')
    api.add_resource(jobs_resources.JobsResource, '/api/jobs/<int:jobs_id>')

    app.run()
