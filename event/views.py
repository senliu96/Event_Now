from flask import Blueprint, render_template, request, session, redirect, url_for, abort
import bson


from event.forms import BasicEventForm,EditEventForm,CancelEventForm
from user.decorators import login_required
from event.models import Event
from user.models import User
from utilities.storage import upload_image_file

event_page = Blueprint('event_page', __name__)

@event_page.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = BasicEventForm()
    error = None
    if request.method == 'POST' and form.validate():
        if form.end_datetime.data < form.start_datetime.data:
            error = "A event must end after it starts!"
        if not error:
            user = User.objects.filter(email=session.get('email')).first()
            
            event = Event(
                name=form.name.data,
                place=form.place.data,
                location=[form.lng.data, form.lat.data],
                start_datetime=form.start_datetime.data,
                end_datetime=form.end_datetime.data,
                description=form.description.data,
                host=user.id,
                attendees=[user]
            )
            event.save()
            return redirect(url_for('event_page.edit', id=event.id))
    return render_template('event/create.html', form=form)
@event_page.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    try:
        event = Event.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)
        
    user = User.objects.filter(email=session.get('email')).first()
    
    if event and event.host == user.id:
        error = None
        message = None
        form = EditEventForm(obj=event)
        if request.method == 'POST' and form.validate():
            if form.end_datetime.data < form.start_datetime.data:
                error = 'A event must end after it starts!'
            if not error:
                form.populate_obj(event)
                if form.lng.data and form.lat.data:
                    event.location = [form.lng.data, form.lat.data]
                image_url = upload_image_file(request.files.get('photo'), 'event_photo', str(event.id))
                if image_url:
                    event.event_photo = image_url
                event.save()
                message = 'Event updated'
        return render_template('event/edit.html', form=form, error=error,
                              message=message, event=event)
    else:
        abort(404)
@event_page.route('/<id>/cancel', methods=['GET', 'POST'])
@login_required
def cancel(id):
    try:
        event = Event.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)
    user = User.objects.filter(email=session.get('email')).first()
    
    if event and event.host == user.id and event.cancel == False:
        error = None
        form = CancelEventForm()
        if request.method == 'POST' and form.validate():
            if form.confirm.data == 'yes':
                event.cancel = True
                event.save()
                return redirect(url_for('event_page.edit', id=event.id))
            else:
                error = 'Say yes if you want to cancel'
        return render_template('event/cancel.html', form=form, error=error, event=event)
    else:
        abort(404)
@event_page.route('/<id>', methods=['GET'])
def public(id):
    try:
        event = Event.objects.filter(id=bson.ObjectId(id)).first()
    except bson.errors.InvalidId:
        abort(404)
        
    if event:
        host = User.objects.filter(id=event.host).first()
        user = User.objects.filter(email=session.get('email')).first()
        return render_template('event/public.html', event=event, host=host, user=user)
    else:
        abort(404)