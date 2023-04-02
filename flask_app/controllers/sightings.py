from flask import render_template, redirect, session, request
from flask_app import app 
from flask_app.models.user import User
from flask_app.models.sighting import Sighting

@app.route('/sighting/dashboard')
def dashboard():
    data=User.find_by_id({"id":session["user_id"]})
    retreiving_all_sightings =Sighting.get_all()
    return render_template('dashboard.html',user=data, sightings =retreiving_all_sightings)

@app.route('/sightings/create')
def add_sighting():
    return render_template("add_sighting.html")


@app.route('/sightings/add_sighting',methods=["POST"])
def adding_sighting():
    if not Sighting.validate_sighting(request.form):
        return redirect('/sightings/create')
    Sighting.save(request.form)
    return redirect("/sighting/dashboard")


@app.route('/sightings/view_sighting/<int:id>')
def view_sighting(id):
    sighting_info= Sighting.find_by_id({"id":id})
    you = User.find_by_id({"id":session["user_id"]})
    return render_template("view_sighting.html",sightings=sighting_info, users=you)


@app.route('/sightings/edit_sighting/<int:id>')
def edit_sighting(id):
    sighting_info= Sighting.find_by_id({"id":id})
    you = User.find_by_id({"id":session["user_id"]})
    return render_template("edit_sighting.html",sightings=sighting_info, users=you)


@app.route('/sightings/editing_sighting',methods=["POST"])
def editing_sighting():
    print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",request.form)
    if not Sighting.validate_sighting(request.form):
        return redirect(f'/sightings/edit_sighting/{request.form["id"]}')
    Sighting.update(request.form)

    return redirect("/sighting/dashboard")


@app.route('/sightings/delete/<int:id>')
def delete_sighting(id):
    
    Sighting.delete({"id":id})
    return redirect("/sighting/dashboard")