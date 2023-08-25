from . import main
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import requests
from app.models import User, db

@main.route('/')
@main.route('/home')
@login_required
def home():
    users = User.query.all()
    for user in users:
        if user in current_user.followed:
            user.isFollowed = True
    return render_template('home.html', users=users)

# follow functionality
@main.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)

    # add user to followed list
    current_user.followed.append(user)

    # commit changes to database
    db.session.commit()

    flash(f'Successfully followed {user.first_name}!', 'success')
    return redirect(url_for('main.home'))

# unfollow functionality
@main.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    user = User.query.get(user_id)

    # remove user from followed list
    current_user.followed.remove(user)

    # commit changes to db
    db.session.commit()

    flash(f'You unfollowed {user.first_name}!', 'info')
    return redirect(url_for('main.home'))

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