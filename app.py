from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    surname = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    instituicao = StringField('Informe a sua instituição de ensino:', validators=[DataRequired()])
    disciplina = SelectField('Informe a sua disciplina:',choices=[('DSWA5','DSWA5'),('DSBA4','DSBA4'),('Gestão de projetos','Gestão de projetos')])

    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.remote_addr
    domain = request.url_root
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Você alterou o seu nome!')
        session['name'] = form.name.data
        session['surname'] = form.surname.data
        session['instituicao'] = form.instituicao.data
        session['disciplina'] = form.disciplina.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=f"{session.get('name')} {session.get('surname')}", instituicao=session.get('instituicao'), disciplina=session.get('disciplina'), ip=ip, host=domain)
