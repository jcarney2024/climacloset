from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User
from . import db

profile_blueprint = Blueprint('profile', __name__)

# Route to display the profile page
@profile_blueprint.route('/')
@login_required
def profile():
    user = current_user  # Get the current logged-in user
    return render_template('profile.html', name=user.name, current_user=user)

# Route to edit the user's name
@profile_blueprint.route('/profile/edit_name', methods=['GET', 'POST'])
@login_required
def edit_name():
    if request.method == 'POST':
        new_name = request.form['new_name']
        if new_name:
            current_user.name = new_name  
            db.session.commit()  
            flash("Name updated successfully!", "success")
        else:
            flash("Name cannot be empty!", "error")
        return redirect(url_for('profile.profile'))  

    return redirect(url_for('profile.profile')) 

