from . import main
from flask import render_template, request
from flask_login import login_required
import requests

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/f1/driverStandings', methods=['GET', 'POST'])
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