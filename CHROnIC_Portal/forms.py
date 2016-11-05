#!/usr/bin/env/ python
__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'

from flask_wtf import Form
from wtforms import StringField, PasswordField

class hcHealthAuthForm(Form):
    ucs_hostname = StringField('Hostname')
    ucs_username = StringField('Username')
    ucs_password = PasswordField('Password')
    vc_hostname = StringField('Hostname')
    vc_username = StringField('Username')
    vc_password = PasswordField('Password')