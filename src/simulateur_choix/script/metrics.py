from pydantic import validate_call
from math import floor
from datetime import datetime, timedelta
from simulateur_choix.script.gaz import Gaz


def compute_all_metrics(distance_daily: float,
                        frequency: float,
                        home_office_days: int,
                        remaining_working_years: int,
                        fuel_consumption: float,
                        emission_factor: float,
                        time_daily: float) -> dict:
    """
    Calculate all the metrics related to commuting, including total distance, fuel cost,
    car cost, CO2 emissions, and total time spent commuting over the remaining working years.

    Parameters
    ----------
    distance_daily : float
        The distance traveled in a single day (round trip).
    frequency : float
        The number of times per week commuting to the office is required.
    home_office_days : int
        The number of days working from home per week.
    remaining_working_years : int
        The number of remaining working years.
    fuel_consumption : float
        Fuel consumption in liters per kilometer.
    emission_factor : float
        CO2 emission factor in grams per kilometer.
    time_daily : float
        Time spent commuting in a single day (in hours).

    Returns
    -------
    dict
        A dictionary containing all the calculated metrics:
        - total_distance: The total distance traveled over the remaining working years.
        - total_fuel_cost: The total fuel cost over the remaining working years.
        - car_cost: The total car cost over the remaining working years.
        - total_emissions: The total CO2 emissions over the remaining working years.
        - total_time: The total time spent commuting over the remaining working years.
    """
    # Calculate total distance for the remaining working years
    total_distance = distance_total(distance_daily, frequency, home_office_days) * remaining_working_years

    # Calculate total fuel cost for the remaining working years
    total_fuel_cost = fuel_cost(total_distance, fuel_consumption, remaining_working_years)

    # Calculate car cost over the remaining working years
    car_cost = car_cost_annual(remaining_working_years)

    # Calculate total CO2 emissions for the remaining working years
    total_emissions = co2_emissions(total_distance, emission_factor)

    # Calculate total time spent commuting over the remaining working years
    time_per_life = compute_total_time(time_daily, frequency, home_office_days, remaining_working_years)

    # Return all the metrics in a dictionary
    return {
        "total_distance": total_distance,
        "total_fuel_cost": total_fuel_cost,
        "total_cost": floor(car_cost+total_fuel_cost),
        "total_emissions": floor(total_emissions),
        "time_per_life": time_per_life
    }


@validate_call
def distance_total(distance_daily: float, frequency: float, home_office_days: int) -> float:
    """
    Calculate the total distance traveled in a year, accounting for home office days.

    Parameters
    ----------
    distance_daily : float
        The distance traveled in a single day (round trip).
    frequency : float
        The number of times per week commuting to the office is required.
    home_office_days : int
        The number of days working from home per week.

    Returns
    -------
    float
        The total distance traveled over the year, assuming 48 working weeks 
        (4 weeks of vacation).

    Notes
    -----
    - Assumes a work schedule of 52 weeks with 4 weeks of vacation (hence 48 working weeks).
    - The number of office commuting days per week is reduced by the number of home office days.

    """
    times_per_week = home_office_days_reduction(frequency, home_office_days)
    distance_per_week = distance_daily * times_per_week
    return distance_per_week * 48  # assuming 4 weeks of vacation per year

@validate_call
def home_office_days_reduction(frequency: int, home_office_days:int) -> int:

    return frequency - home_office_days


@validate_call
def compute_total_time(daily_time_seconds: float, frequency: int, home_office_days: int, years: int) -> str:
    time_per_week = daily_time_seconds * home_office_days_reduction(frequency, home_office_days)
    time_per_life = time_per_week * 48 * years
    return time_per_life


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
    gaz.get_model()

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
