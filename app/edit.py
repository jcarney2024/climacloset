from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User
from . import db

profile = Blueprint('profile', __name__)

# Route to display the profile page
@profile.route('/')
@login_required
def show_profile():  # Renamed from 'profile'
    user = current_user  # Get the current logged-in user
    return render_template('profile.html', name=user.name, current_user=user)

# Route to edit the user's name
@profile.route('/edit_name', methods=['POST'])
@login_required
def edit_name():
    new_name = request.form['new_name']
    if new_name:
        current_user.name = new_name  
        db.session.commit()  
        flash("Name updated successfully!", "success")
        return render_template('profile.html', name=new_name, current_user=current_user)
    else:
        flash("Name cannot be empty!", "error")
        return redirect(url_for('profile.show_profile'))

@profile.route('/upload_picture', methods=['POST'])
@login_required
def upload_picture():
    image = request.form['profile_picture']
    if image:
        user = current_user
        current_user.image_file = image
        db.session.commit()
        flash("Image uploaded successfully!", "success")
        return render_template('profile.html', name=user.name, current_user=current_user)
    else:
        flash("No image selected!", "error")
        return redirect(url_for('profile.show_profile'))