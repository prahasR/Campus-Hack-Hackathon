from flask import Flask, render_template,url_for,flash, redirect
app = Flask(__name__)
from forms import RegistrationForm,LoginForm

app.config['SECRET_KEY']='f154e1e86eb3f11bba3ade756bf8d0'
posts=[
    {"author":"Prahas",
     "title":'Blog1',
     "content":'pehla blog',
     "date_posted":"jan22"

    },
    {"author":"Pratyush",
     "title":'Blog1',
     "content":'second blog',
     "date_posted":"jan42"

    }
]

@app.route("/", methods=['GET','POST'])    
def registeration():
    form= RegistrationForm()
    if form.validate_on_submit():
        flash(f"""We found these results!
                PYL100
                300
                670""",'success')  
        return redirect(url_for('registeration'))
    return render_template('register.html', title="SIGN UP", form=form)
@app.route("/login", methods=['GET','POST'])    
def login():
    form= LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('hello'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title="SIGN In", form=form)

if __name__=="__main__":
    app.run(debug=True)
