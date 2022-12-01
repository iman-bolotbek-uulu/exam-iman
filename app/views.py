from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db
from . import models
from . import forms


def index():
    employees = models.Employee.query.all()
    return render_template('index.html',employees=employees)


@login_required
def employee_create():
    form = forms.EmployeeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            employee = models.Employee()
            form.populate_obj(employee)
            db.session.add(employee)
            db.session.commit()
            flash('Работник успешно добавлен!','success')
            return redirect(url_for('index'))
    return render_template('employee_create.html',form=form)


@login_required
def employee_detail(id):
    employee = models.Employee.query.get(id)
    return render_template('employee_detail.html',employee=employee)


@login_required
def employee_delete(id):
    employee = models.Employee.query.get(id)
    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()
        flash('Работник успешно удален!', 'success')
        return redirect(url_for('index'))
    return render_template('employee_delete.html',employee=employee)


@login_required
def employee_update(id):
    employee = models.Employee.query.get(id)
    form = forms.EmployeeForm(request.form,obj=employee)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(employee)
            db.session.add(employee)
            db.session.commit()
            flash('Работник успешно изменен!','success')
            return redirect(url_for('index'))
    return render_template('employee_update.html', form=form)


# user functions

def register():
    form = forms.UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = models.User()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            flash(f'Пользователь {user.username} успешно зарегистрирован!','success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


def login():
    form = forms.UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = models.User.query.filter_by(username=request.form.get('username')).first()
            if user and user.check_password(request.form.get('password')):
                login_user(user)
                flash('Успешно авторизован!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Неправильно введенные логин или пароль!', 'danger')
    return render_template('login.html', form=form)


def logout():
    logout_user()
    return redirect(url_for('index'))
