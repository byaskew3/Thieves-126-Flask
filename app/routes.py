from flask import request, render_template
import requests
from app import app
from .forms import LoginForm, SignupForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# fake database
REGISTERED_USERS = {
    'dylank@thieves.com': {
        'name': 'Dylan Katina',
        'password': 'ilovemydog'
    }
}

# HTTP Methods & Rendering Templates
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if email in REGISTERED_USERS and password == REGISTERED_USERS[email]['password']:
            return f'Hello, {REGISTERED_USERS[email]["name"]}'
        else:
            return 'Invalid email or password'
    else:
        print('not validated')
        return render_template('login.html', form=form)
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = f'{form.first_name.data} {form.last_name.data}'
        email = form.email.data
        password = form.password.data
        REGISTERED_USERS[email] = {
            'name': name,
            'password': password
        }
        return f'Thank you for registering {name}!'
    else:
        return render_template('signup.html', form=form)

@app.route('/students')
def students():
    thieves_students = ['Justin', 'Britt', 'Omar']
    return render_template('students.html', students=thieves_students)



@app.route('/f1/driverStandings', methods=['GET', 'POST'])
def get_driver_info_year_rnd():
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