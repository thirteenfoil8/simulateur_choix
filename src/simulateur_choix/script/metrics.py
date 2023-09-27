from pydantic import validate_call


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
def time_spent(distance: float, average_speed: float) -> float:
    """
    Calculate total time spent traveling based on the given distance and average speed.

    :param distance: Total distance traveled in km.
    :param average_speed: Average speed of the vehicle in km/h.
    :return: Total time spend in hour
    """
    return distance / average_speed


@validate_call
def fuel_cost(distance: float, fuel_consumption: float, fuel_price: float) -> float:
    """
    Calculate total fuel cost based on distance, fuel consumption, and fuel price.

    :param distance: Total distance traveled in km.
    :param fuel_consumption: Fuel consumption (L/100km).
    :param fuel_price: Price of fuel per liter in CHF/L.
    :return: Total fuel cost in CHF.
    """
    total_fuel = (distance / 100) * fuel_consumption
    return total_fuel * fuel_price

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
def co2_emissions(distance: float, emission_factor: float) -> float:
    """
    Calculate CO2 emissions based on distance and emission factor.
    
    :param distance: Total distance traveled.
    :param emission_factor: CO2 emission factor (kg CO2 per km).
    :return: Total CO2 emissions.
    """
    return distance * emission_factor

if __name__ == "__main__":
    print(f"Distance parcouru pendant une carrière: {distance_total(48, 5)*48} km")

    print(f"Distance parcouru pendant une carrière si on fait 2 jours de covoiturage: {distance_total(48, 5, carpooling_days=2)*48} km")

    print(f"Temps passé à conduire pendant une carrière: {time_spent(distance_total(48, 5)*48, 50)} heures")

    print(f"""Prix de l'essence pendant une carrière: {fuel_cost(
                                                            distance=distance_total(48, 5)*48,
                                                            fuel_consumption=6,
                                                            fuel_price=2)} CHF """)
