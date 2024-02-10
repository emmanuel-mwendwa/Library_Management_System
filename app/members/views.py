from flask import render_template, redirect, url_for, flash, request

from flask_login import login_required

from datetime import datetime

from . import member

from .forms import AddMemberForm

from .. import db

from ..models import Member


@member.route('/add_member', methods=["GET", "POST"])
def add_member():

    form = AddMemberForm()

    if form.validate_on_submit():

        new_member = Member(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data.lower(),
        )

        db.session.add(new_member)

        db.session.commit()

        return redirect(url_for('member.view_members'))
    
    submit_button_text = "Add Member"
    
    return render_template("members/add_member.html", form=form, submit_button_text=submit_button_text)


@member.route("/view_members")
def view_members():

    search_term = request.args.get("search_term", "")

    if search_term:
        # Perform search query based on the search term
        members = Member.query.filter(Member.first_name.ilike(f"%{search_term}%") | Member.email.ilike(f"%{search_term}%") | Member.last_name.ilike(f"%{search_term}%")).all()

    else:

        members = Member.query.all()

    return render_template("members/view_members.html", members=members)


@member.route("/view_member/<int:member_id>")
def view_member(member_id):

    try:

        member = Member.query.filter_by(id=member_id).first()

        if member is None:
            
            raise Exception("Member not found")

        return render_template("members/view_member.html", member=member)
    
    except Exception as e:

        flash(f"Error: {str(e)}", category="error")

        return render_template("error.html")
    

@member.route('/update_member/<int:member_id>', methods=["GET", "POST", "PUT"])
def update_member(member_id):

    form = AddMemberForm()

    member = Member.query.get(member_id)

    if member is None:

        flash("Member not found", category="error")

    if form.validate_on_submit():
        # Update the member attributes based on the data received in the request
        member.first_name = form.first_name.data
        member.last_name = form.last_name.data
        member.email = form.email.data

        # Update the 'updated_at' attribute
        member.updated_at = datetime.utcnow()

        db.session.commit()

        return redirect(url_for('member.view_member', member_id=member.id))
    
    form.first_name.data = member.first_name
    form.last_name.data = member.last_name
    form.email.data = member.email

    form_heading = "Update Member"
    submit_button_text = "Update Member"

    return render_template("members/add_member.html", form=form, submit_button_text=submit_button_text, form_heading=form_heading)

@member.route('/delete_member/<int:member_id>', methods=["GET", "DELETE"])
def delete_member(member_id):
    
    member = Member.query.get(member_id)

    if member is None:

        flash("Member not found", category="error")

    db.session.delete(member)

    db.session.commit()

    return redirect(url_for("member.view_members"))