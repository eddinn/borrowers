from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length


# Forms
class BorrowForm(FlaskForm):
    clientname = StringField('Name', validators=[DataRequired()])
    clientemail = StringField('Email', validators=[DataRequired()])
    clientphone = StringField('Phone', validators=[DataRequired()])
    clientaddress = StringField('Address', validators=[Optional()])
    clientzip = StringField('ZIP', validators=[Optional()])
    clientcity = StringField('City', validators=[Optional()])
    clientinfo = TextAreaField('Info',
                               validators=[Optional(), Length(max=2048)])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
