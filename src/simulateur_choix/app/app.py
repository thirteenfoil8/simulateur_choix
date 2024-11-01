from flask import Flask, render_template, request, redirect, flash, url_for
from simulateur_choix.script.metrics import compute_all_metrics
from simulateur_choix.app.control_data import validate_input_data
from simulateur_choix.script.route import get_route
from math import floor
from dotenv import dotenv_values
import os

dotenv_path = os.getenv("DOTENV_PATH", ".env")
config = dotenv_values(dotenv_path)


app = Flask(__name__)
app.secret_key = config["SECRET_KEY"]


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # check data
        data = request.form.to_dict()
        error = validate_input_data(data)
        if error:
            flash(error, 'danger')
            return redirect(url_for('index'))
        age = float(data.get('age'))
        retirement = float(data.get('retirement'))
        frequency = float(data.get('frequency'))
        home_office_days = int(data.get('home_office_days'))
        fuel_consumption = float(data.get('fuel_consumption'))
        emission_factor = float(data.get('emission_factor'))
        time_spent = float(data.get('time_spent'))

        domicile_lat = float(data.get('domicile_lat'))
        domicile_lng = float(data.get('domicile_lng'))
        travail_lat = float(data.get('travail_lat'))
        travail_lng = float(data.get('travail_lng'))
        distance_daily, time_daily = get_route(domicile_lat,domicile_lng, travail_lat, travail_lng, time_spent)
        # compute metrics:
        remaning_working_years = (retirement-age) if (retirement-age) else 44
        full_time_without_home_office = compute_all_metrics(distance_daily, frequency, 0, remaning_working_years, fuel_consumption, emission_factor, time_daily)
        full_time_with_home_office = compute_all_metrics(distance_daily, frequency, home_office_days, remaning_working_years, fuel_consumption, emission_factor, time_daily)
        total_distance = full_time_without_home_office['total_distance'] - full_time_with_home_office['total_distance']
        time_per_life = full_time_without_home_office['time_per_life'] - full_time_with_home_office['time_per_life']
        total_cost = full_time_without_home_office['total_cost'] - full_time_with_home_office['total_cost']
        total_emissions = full_time_without_home_office['total_emissions'] - full_time_with_home_office['total_emissions']
        days, remainder = divmod(time_per_life, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        total_time = f"{days} jours, {hours} heures, {minutes} minutes et {seconds} secondes"
        return render_template('results.html', total_distance=total_distance,
                               total_time=total_time, total_cost=floor(total_cost),
                               total_emissions=total_emissions)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
