# add update delete view tasks route

from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task
from flask_login import login_required, current_user

task_bp = Blueprint("tasks",__name__)

@task_bp.route('/',methods=['GET'])
@login_required
def view_tasks():
  
  
  tasks = Task.query.all()
  return render_template('tasks.html',tasks=tasks)


@task_bp.route("/add",methods=['POST'])
@login_required
def add_task():
  if request.method == 'POST':
    title = request.form.get("title")
    if title:
      new_task = Task(title=title,status='Pending')
      db.session.add(new_task)
      db.session.commit()
      flash("Task added successfully","success")
      return redirect(url_for('tasks.view_tasks'))
    else:
      flash("Task added failed","danger")
      return redirect(url_for('tasks.view_tasks'))
  
  
  return redirect(url_for('tasks.view_tasks'))


@task_bp.route('/toggle/<int:task_id>',methods=['POST'])
@login_required
def toggle_status(task_id):
  

  task = Task.query.get(task_id)
  if not task:
    flash("Task not found", "danger")
    return redirect(url_for('tasks.view_tasks'))
  if task:
    if task.status == 'Pending':
      task.status = 'Working'
    elif task.status == 'Working':
      task.status = 'Done'
    else:
      task.status = 'Pending'
    db.session.commit()
    return redirect(url_for('tasks.view_tasks'))



@task_bp.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
  
  task = Task.query.get(task_id)
  if task:
    db.session.delete(task)
    db.session.commit()
  flash("One task deleted!","info")
  return redirect(url_for("tasks.view_tasks"))

@task_bp.route('/clear',methods=['POST'])
@login_required
def clear_tasks():
  
  Task.query.delete()
  db.session.commit()
  flash("All tasks cleared!","info")
  return redirect(url_for("tasks.view_tasks"))