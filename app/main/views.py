from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, RegisterBikeForm
from .. import db
from ..models import Permission, Role, User, BikeUsage
from ..decorators import admin_required, permission_required

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['DRAPPOINTMENT_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/register-bike', methods=['GET', 'POST'])
@login_required
def register_bike():
    ridertype = BikeUsage.query.filter_by(user_id=current_user.id).first()
    if ridertype is None:
        ridertype =  BikeUsage()
    form = RegisterBikeForm(current_user.id)
    if form.validate_on_submit():
        ridertype.weight = form.weight.data
        ridertype.style = form.style.data
        ridertype.terrain = form.terrain.data
        ridertype.duration = form.duration.data
        ridertype.cleaning = form.cleaning.data
        ridertype.conditions = form.conditions.data
        ridertype.gears = form.gears.data
        ridertype.user_id = current_user.id
        db.session.add(ridertype)
        flash('Your bike usage data has been added.')
        return redirect(url_for('.user', username=current_user.username))
    form.weight.data = ridertype.weight
    form.style.data = ridertype.style 
    form.terrain.data = ridertype.terrain 
    form.duration.data = ridertype.duration 
    form.cleaning.data = ridertype.cleaning 
    form.conditions.data = ridertype.conditions 
    form.gears.data = ridertype.gears 
    return render_template('register_bike.html', form=form, user_id=current_user.id)
        
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)



