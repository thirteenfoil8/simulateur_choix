from flask import Flask, render_template, request, redirect, flash, url_for
from simulateur_choix.script.metrics import distance_total, time_spent, fuel_cost, co2_emissions
from simulateur_choix.app.control_data import validate_input_data


app = Flask(__name__)
app.secret_key = 'une_cle_secrete_tres_difficile_a_deviner'


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
        distance_daily = 2*(float(data.get('end_point')) - float(data.get('start_point')))
        frequency = float(data.get('frequency'))
        carpooling_days = int(data.get('carpooling_days'))
        average_speed = float(data.get('average_speed'))
        fuel_consumption = float(data.get('fuel_consumption'))
        emission_factor = float(data.get('emission_factor'))
        fuel_price = float(data.get('fuel_price'))



        # compute metrics:
        total_distance = distance_total(distance_daily, frequency, carpooling_days)*48
        total_time = time_spent(total_distance, average_speed)
        total_fuel_cost = fuel_cost(total_distance, fuel_consumption, fuel_price)
        total_emissions = co2_emissions(total_distance, emission_factor)

        return render_template('results.html', total_distance=total_distance,
                               total_time=total_time, total_fuel_cost=total_fuel_cost,
                               total_emissions=total_emissions, first_name=first_name, last_name=last_name)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
