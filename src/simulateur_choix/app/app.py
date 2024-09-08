from flask import Flask, render_template, request, redirect, flash, url_for
from simulateur_choix.script.metrics import distance_total, compute_total_time, fuel_cost, co2_emissions, car_cost_annual
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
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        age = float(data.get('age'))
        retirement = float(data.get('retirement'))
        frequency = float(data.get('frequency'))
        carpooling_days = int(data.get('carpooling_days'))
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
        total_distance = distance_total(distance_daily, frequency, carpooling_days)*remaning_working_years
        total_fuel_cost = fuel_cost(total_distance, fuel_consumption, remaning_working_years)
        car_cost = car_cost_annual(remaning_working_years)
        total_emissions = co2_emissions(total_distance, emission_factor)
        total_time = compute_total_time(time_daily, remaning_working_years)

        return render_template('results.html', total_distance=total_distance,
                               total_time=total_time, total_cost=floor(total_fuel_cost+ car_cost),
                               total_emissions=floor(total_emissions), first_name=first_name, last_name=last_name)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
