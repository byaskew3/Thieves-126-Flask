from flask import request, render_template, flash, redirect, url_for
import requests
from app import app
from .forms import LoginForm, SignupForm
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, db
from werkzeug.security import check_password_hash

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# HTTP Methods & Rendering Templates
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        # query the user object from database
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Hello, {queried_user.first_name}!', 'primary')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():

        # Grabbing our sign up form data
        first_name = form.first_name.data 
        last_name = form.last_name.data
        email = form.email.data.lower()
        password = form.password.data
        
        # Creating an instance of the User Model
        new_user = User(first_name, last_name, email, password)

        # Adding new user to our database
        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you for signing up {new_user.first_name}!', 'primary')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/students')
def students():
    thieves_students = ['Justin', 'Britt', 'Omar']
    return render_template('students.html', students=thieves_students)



@app.route('/f1/driverStandings', methods=['GET', 'POST'])
@login_required
def driver_standings():
    if request.method == 'POST':
        year = request.form.get('year')
        rnd = request.form.get('rnd')

        url = f'https://ergast.com/api/f1/{year}/{rnd}/driverStandings.json'
        response = requests.get(url)
        if response.ok:
            data = response.json()
            driver_standings_data = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
            drivers = get_driver_info(driver_standings_data)
            return render_template('driverStandings.html', drivers=drivers)
    else:
        return render_template('driverStandings.html')

# Helper Function
def get_driver_info(data):
    new_driver_data = []
    for driver in data:
        driver_dict = {
            'first_name': driver['Driver']['givenName'],
            'last_name': driver['Driver']['familyName'],
            'DOB': driver['Driver']['dateOfBirth'],
            'wins': driver['wins'],
            'team': driver['Constructors'][0]['name']
        }
        new_driver_data.append(driver_dict)
    return new_driver_data