from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, History
from . import db

profile = Blueprint('profile', __name__)

# Route to edit the user's name
@profile.route('/edit_name', methods=['POST'])
@login_required
def edit_name():
    new_name = request.form['new_name']
    if new_name:
        current_user.name = new_name  
        db.session.commit()  
        flash("Name updated successfully!", "success")
        return redirect(url_for('main.profile'))
    else:
        flash("Name cannot be empty!", "error")
        return redirect(url_for('main.profile'))

@profile.route('/upload_picture', methods=['POST'])
@login_required
def upload_picture():
    image = request.form['profile_picture']
    if image:
        current_user.image_file = image
        db.session.commit()
        flash("Image uploaded successfully!", "success")
        return redirect(url_for('main.profile'))
    else:
        flash("No image selected!", "error")
        return redirect(url_for('main.profile'))

@profile.route('/delete_entry/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = History.query.get(entry_id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        flash("Entry deleted successfully!", "success")
        return redirect(url_for('main.profile'))
    flash("Failed to delete entry!", "error")
    return redirect(url_for('main.profile'))