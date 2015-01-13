from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField, FloatField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class RegisterBikeForm(Form):
    weight = IntegerField('What is your weight in lbs?', validators=[Required()])
    style = SelectField('What is your riding style?', coerce=int)
    terrain = SelectField('What type of terrain do you mostly ride on?', coerce=int)
    duration = FloatField('How many hours per week do you ride?')
    cleaning = SelectField('How often do you clean and lube your chain?', coerce=int)
    conditions = SelectField('What are the conditions like for most of your rides?', coerce=int)
    gears = SelectField('How many speeds are on your rear derailer?', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
      super(RegisterBikeForm, self).__init__(*args, **kwargs)
      self.style.choices = [(1, 'Very Aggressive'), (2, 'Aggressive'), (3, 'Moderate'),
                            (4, 'Casual'),(5, 'Light')]
      self.terrain.choices = [(1, 'Cyclocross'), (2, 'Mountain'), (3, 'Road'),
                              (4, 'Touring'), (5, 'Commuter'), (6, 'Casual')]
      self.cleaning.choices = [(1, 'Never'), (2, 'Once a Year'), (3, 'Once a Month'),
                               (4, 'Once a Week'), (5, 'Every Ride')]
      self.conditions.choices = [(1, 'Muddy'), (2, 'Sandy'), (3, 'Wet'),
                               (4, 'Dusty'), (5, 'Dry')]
      self.gears.choices = [(1, '11'), (2, '10'), (3, '9'),
                              (4, '8'), (5, '5,6, or 7'), (6, '1')]

class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

