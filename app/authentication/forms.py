from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError

from app.authentication.user import User


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=1, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=1, max=20)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Log In")


def validate_username(username):
    existing_user_username = User.query.filter_by(
        username=username.data
    ).first()

    if existing_user_username:
        raise ValidationError(" USERNAME ALREADY EXISTS , PLZ CHOOSE OTHER")


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=1, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=1, max=20)],
        render_kw={"placeholder": "Password"},
    )
    address = StringField(
        validators=[InputRequired(), Length(min=4, max=80)],
        render_kw={"placeholder": "address"},
    )
    key = StringField(
        validators=[InputRequired(), Length(min=4, max=80)],
        render_kw={"placeholder": "key"},
    )

    submit = SubmitField("Register")
