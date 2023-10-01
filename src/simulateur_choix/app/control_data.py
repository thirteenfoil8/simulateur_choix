def validate_input_data(data: dict) -> str:
    # Vérification de la présence de toutes les clés nécessaires
    expected_keys = [
        'domicile_lat', 'domicile_lng', 'travail_lat', 'travail_lng','first_name', 'last_name', 'age', 
        'retirement', 'frequency', 'carpooling_days', 'fuel_consumption', 'emission_factor', 'fuel_price'
    ]
    for key in expected_keys:
        if key not in data:
            return f"Le champ {key} est manquant."

    if not data['domicile_lat'] or not data['domicile_lng']:
        return "Veuillez entrer un point de départ."
    
    if not data['travail_lat'] or not data['travail_lng'] :
        return "Veuillez entrer un point d'arrivée."
    

    if not data['first_name']:
        return "Veuillez entrer votre nom."
    if not data['last_name']:
        return "Veuillez entrer votre prénom."

    if not data['age']:
        return "Veuillez entrer votre age."
    if not data['retirement']:
        return "Veuillez entrer votre age à la retraire"

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
