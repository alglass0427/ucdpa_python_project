import sys
print(sys.executable)
from functools import wraps
import functions.functions as func    ###Functions file in functions folder to seperate functions from app.py
# import json  #imported in the functions file
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,DateField,RadioField
from wtforms.validators import DataRequired


try:
    import wtforms
    print("WTForms is installed.")
except ImportError:
    print("WTForms is not installed.")


# //////////////////////////////////////////////////////////
class InfoForm(FlaskForm):

    name = StringField("Full Name",validators=[DataRequired()],render_kw={"class": "form-control"})
    dob = DateField("Date of Birth")
    gender = RadioField("Gender",
            choices=[("man","Male"),
                     ("woman","Female"),
                     ("none","Not Disclosed")
                     ])
    print(gender)
    email = StringField("Email Address",validators=[DataRequired()],render_kw={"class": "form-control"})
    password = PasswordField("Password",render_kw={"class": "form-control"})
    # fav_color = ColorField("Fav Color")
    submit = SubmitField("Submit")


@app.route('/forms',methods = ['GET','POST'])
def forms():
    form = InfoForm() #Create instance of class
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['dob'] = form.dob.data
        session['gender'] = form.gender.data
        session['email'] = form.email.data
        session['fav_color'] = form.fav_color.data
        
        return redirect(url_for('thankyou'))
    return render_template('forms.html',form = form)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


# //////////////////////////////////////////////////////////