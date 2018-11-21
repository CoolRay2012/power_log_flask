from flask_wtf import Form
from wtforms import StringField, RadioField, validators
from wtforms.validators import DataRequired
import os

# get platform xml list
platxml_list = []
for static_file in os.listdir(os.getcwd() + r"\app_logp\static"):
	if static_file.endswith('xml'):
		platxml_list.append(static_file.split('.')[0])

class LoginForm(Form):
    logpath = StringField('logpath', validators=[DataRequired()])
    platform_radio = RadioField(
        'Platform?',
        [validators.Required()],
        choices=[(e,e) for e in platxml_list]
    )
