from pydantic import validate_call
from datetime import datetime, timedelta
from simulateur_choix.script.gaz import Gaz


@validate_call
def distance_total(distance_daily: float, frequency: float, carpooling_days: int = 0) -> float:
    """
    Calculate total distance traveled over a career.

    :param distance_daily: Distance traveled daily (round trip).
    :param frequency: Number of days per week the user travels.
    :param years: Number of years of career. Default is 44.
    :return: Total distance traveled over a career.
    """
    distance_per_week = distance_daily*frequency
    if carpooling_days>0:
        distance_per_week = carpooling_reduction(distance_per_week,distance_daily, carpooling_days)

    distance_per_year = distance_per_week * 48
    return distance_per_year

@validate_call
def carpooling_reduction(distance_total: float, distance_daily :float, carpooling_days: int):
    """
    Calculate carpooling reduction per week.

    :param distance_total: Total distance in a week
    :param distance_daily: Distance traveled daily (round trip).
    :param carpooling_days: Number of carpooling days per week if 2 people
    :return: Total distance traveled over a career.
    """
    return distance_total - carpooling_days*distance_daily/2


@validate_call
def compute_total_time(daily_time_seconds: float, years:float):
    DAYS_IN_YEAR = 365
    total_time_seconds = daily_time_seconds * DAYS_IN_YEAR * years
    days, remainder = divmod(total_time_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} jour, {hours} heures, {minutes} minutes, et {seconds} secondes"


@validate_call
def fuel_cost(distance: float, fuel_consumption: float, remaining_working_years: float) -> float:
    """
    Calculate total fuel cost based on distance, predicted fuel consumption, and fuel price.

    :param distance: Total distance traveled in km.
    :param remaining_working_years: Number of years remaining in the user's career.
    :param fuel_price: Price of fuel per liter in CHF/L.
    :return: Total fuel cost in CHF.
    """ 
    gaz = Gaz()
    model = gaz.get_model()

    start_date = datetime.now()
    end_date = datetime.now() + timedelta(days=365*remaining_working_years)
    date_range = [start_date + timedelta(days=x) for x in range(0, (end_date-start_date).days)]
    
    # Assuming gaz.predict returns a list of predicted values
    predicted_fuel_prices = gaz.predict(date_range, model_type="linear")
    average_fuel_price = sum(predicted_fuel_prices) / len(predicted_fuel_prices)

    total_fuel = (distance / 100) * fuel_consumption
    return total_fuel * average_fuel_price[0]


@validate_call
def car_cost_annual(remaining_working_years: float) -> float:
    """
    Calculate total car cost based years. based on 
    https://www.baloise.ch/fr/clients-prives/blog/auto/combien-coute-une-voiture-par-an.html#anchor-id-af15

    :param remaining_working_years: Number of years remaining in the user's career.
    :return: Total fuel cost in CHF.
    """ 
    car_cost_without_fuel = 8000
    return car_cost_without_fuel * remaining_working_years

@validate_call
def compare_with_public_transport(fuel_total_cost: float, public_transport_cost: float):
    """
    Compare the cost of using a personal vehicle with the cost of public transport.
    
    :param fuel_total_cost: Total fuel cost for personal vehicle per year.
    :param public_transport_cost: Annual cost of public transport per year.
    :return: Difference between the two costs.
    """
    #TODO Add average car cost per year with federal taxes, insurance, ...
    return fuel_total_cost - public_transport_cost

@validate_call
def time_spent(distance: float, average_speed: float) -> float:
    """
    Calculate total time spent traveling based on the given distance and average speed.

    :param distance: Total distance traveled in km.
    :param average_speed: Average speed of the vehicle in km/h.
    :return: Total time spend in hour
    """
    return distance / average_speed

@validate_call
def co2_emissions(distance: float, emission_factor: float) -> float:
    """
    Calculate CO2 emissions based on distance and emission factor.
    
    :param distance: Total distance traveled.
    :param emission_factor: CO2 emission factor (kg CO2 per km).
    :return: Total CO2 emissions.
    """
    return distance * emission_factor
