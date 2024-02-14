from flask import render_template, redirect, url_for, flash, request, current_app

from flask_login import login_required

from datetime import datetime

from sqlalchemy.exc import IntegrityError

from . import member

from .forms import AddMemberForm

from app import db

from app.models import Member


@member.route('/add_member', methods=["GET", "POST"])
def add_member():

    form = AddMemberForm()

    if form.validate_on_submit():

        Member.create(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data.lower(),
        )

        return redirect(url_for('member.view_members'))
    
    submit_button_text = "Add Member"
    
    return render_template("members/add_member.html", form=form, submit_button_text=submit_button_text)


@member.route("/view_members")
def view_members():

    page = request.args.get('page', 1, type=int)

    search_term = request.args.get("search_term", "")

    if search_term:
        # Perform search query based on the search term
        pagination = Member.query.filter(
            Member.first_name.ilike(f"%{search_term}%") | 
            Member.email.ilike(f"%{search_term}%") | 
            Member.last_name.ilike(f"%{search_term}%"))\
            .paginate(
                page=page,
                per_page=current_app.config["RECORDS_PER_PAGE"],
                error_out=False
            )
        
        members = pagination.items

    else:

        pagination = Member.query.paginate(
                page=page,
                per_page=current_app.config["RECORDS_PER_PAGE"],
                error_out=False
            )
        
        members = pagination.items

    return render_template("members/view_members.html", members=members, pagination=pagination, page=page)


@member.route("/view_member/<int:member_id>")
def view_member(member_id):

    try:

        member = Member.get(member_id)

        if member is None:
            
            raise Exception("Member not found")

        return render_template("members/view_member.html", member=member)
    
    except Exception as e:

        flash(f"Error: {str(e)}", category="error")

        return render_template("error.html")
    

@member.route('/update_member/<int:member_id>', methods=["GET", "POST", "PUT"])
def update_member(member_id):

    form = AddMemberForm()

    member = Member.get(member_id)

    if member is None:

        flash("Member not found", category="error")

    if form.validate_on_submit():
        # Update the member attributes based on the data received in the request

        member.update(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            email = form.email.data,
        
            # Update the 'updated_at' attribute
            updated_at = datetime.utcnow()
        )

        return redirect(url_for('member.view_member', member_id=member.id))
    
    form.first_name.data = member.first_name
    form.last_name.data = member.last_name
    form.email.data = member.email

    form_heading = "Update Member"
    submit_button_text = "Update Member"

    return render_template("members/add_member.html", form=form, submit_button_text=submit_button_text, form_heading=form_heading)

@member.route('/delete_member/<int:member_id>', methods=["GET", "DELETE"])
def delete_member(member_id):
    
    member = Member.get(member_id)

    if member is None:

        flash("Member not found", category="error")

    try:
        
        member.delete()

        flash(f"Member deleted successfully", category="success")

    except IntegrityError as e:

        db.session.rollback()

        flash(f"Failed to delete member. Please try again.", category="error")


    return redirect(url_for("member.view_members"))