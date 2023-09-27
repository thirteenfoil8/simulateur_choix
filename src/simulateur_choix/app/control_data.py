def validate_input_data(data: dict) -> str:
    # Vérification de la présence de toutes les clés nécessaires
    expected_keys = [
        'start_point', 'end_point', 'frequency', 'carpooling_days',
        'average_speed', 'fuel_consumption', 'emission_factor', 'fuel_price'
    ]
    for key in expected_keys:
        if key not in data:
            return f"Le champ {key} est manquant."

    # Validation de start_point et end_point
    if not data['start_point']:
        return "Veuillez entrer un point de départ."
    if not data['end_point']:
        return "Veuillez entrer un point d'arrivée."

    # Validation de frequency
    try:
        freq_val = int(data['frequency'])
        if freq_val < 1 or freq_val > 7:
            raise ValueError
    except ValueError:
        return "Veuillez entrer un nombre valide pour la fréquence (entre 1 et 7)."

    # Validation de carpooling_days
    try:
        carpooling_days = int(data['carpooling_days'])
        if carpooling_days < 0 or carpooling_days > 7:
            raise ValueError
    except ValueError:
        return "Veuillez entrer un nombre valide pour le nombre de jours en covoiturage (entre 0 et 7)."

    # Validation de average_speed
    try:
        average_speed = float(data['average_speed'])
        if average_speed <= 0:
            raise ValueError
    except ValueError:
        return "Veuillez entrer une vitesse moyenne valide."

    # Validation de fuel_consumption
    try:
        fuel_consumption = float(data['fuel_consumption'])
        if fuel_consumption <= 0:
            raise ValueError
    except ValueError:
        return "Veuillez entrer une consommation de carburant valide."

    # Validation de emission_factor et fuel_price
    for key in ['emission_factor', 'fuel_price']:
        try:
            val = float(data[key])
            if val < 0 or val > 3:
                raise ValueError
        except ValueError:
            return f"Veuillez entrer une valeur valide pour {key}."

    return None  # Tout est valide
