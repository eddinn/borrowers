from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, \
    Length, ValidationError
from app.models import Post


# Forms
class PostForm(FlaskForm):
    clientname = StringField('Name', validators=[DataRequired()],
                             render_kw={'style': 'width: 200px'})
    clientss = StringField('Social security number', validators=[Optional()],
                            render_kw={'style': 'width: 200px'})
    clientemail = StringField('Email', validators=[DataRequired(),
                              EqualTo('clientemail'), Email()],
                              render_kw={'style': 'width: 200px'})
    clientphone = StringField('Phone', validators=[DataRequired()],
                              render_kw={'style': 'width: 200px'})
    clientaddress = StringField('Address', validators=[Optional()],
                                render_kw={'style': 'width: 200px'})
    clientzip = StringField('ZIP', validators=[Optional()],
                            render_kw={'style': 'width: 60px'})
    clientcity = StringField('City', validators=[Optional()],
                             render_kw={'style': 'width: 200px'})
    clientinfo = TextAreaField('Item list', validators=[Optional(),
                               Length(max=2048)],
                               render_kw={'style': 'width: 600px'})
    submit = SubmitField(label='Submit')
    cancel = SubmitField(label='Cancel', render_kw={'formnovalidate': True})

    @staticmethod
    def validate_clientss(form, clientss):
        clientss = Post.query.filter_by(clientss=clientss.data).first()
        if clientss is not None:
            raise ValidationError('Social security number must be unique.')

    @staticmethod
    def validate_clientemail(form, clientemail):
        clientemail = Post.query.filter_by(clientemail=clientemail.data) \
            .first()
        if clientemail is not None:
            raise ValidationError('Email already registered.')


class EditPostForm(FlaskForm):
    clientname = StringField('Name', validators=[DataRequired()],
                             render_kw={'style': 'width: 200px'})
    clientss = StringField('Social security number', validators=[Optional()],
                            render_kw={'style': 'width: 200px'})
    clientemail = StringField('Email', validators=[DataRequired(),
                              EqualTo('clientemail'), Email()],
                              render_kw={'style': 'width: 200px'})
    clientphone = StringField('Phone', validators=[DataRequired()],
                              render_kw={'style': 'width: 200px'})
    clientaddress = StringField('Address', validators=[Optional()],
                                render_kw={'style': 'width: 200px'})
    clientzip = StringField('ZIP', validators=[Optional()],
                            render_kw={'style': 'width: 60px'})
    clientcity = StringField('City', validators=[Optional()],
                             render_kw={'style': 'width: 200px'})
    clientinfo = TextAreaField('Item list', validators=[Optional(),
                               Length(max=2048)],
                               render_kw={'style': 'width: 600px'})
    submit = SubmitField(label='Submit')
    cancel = SubmitField(label='Cancel',
                         render_kw={'formnovalidate': True})


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
