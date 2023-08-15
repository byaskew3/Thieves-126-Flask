from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return 'This is the thieves home page'

@app.route('/user/<string:name>')
def users(name):
    return f'This is {name} page'

@app.route('/post/<int:post_id>')
def post(post_id):
    return f'This is post number {post_id}'

# HTTP Methods & Rendering Templates
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return f'{email} {password}'
    else:
        return render_template('login.html')


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