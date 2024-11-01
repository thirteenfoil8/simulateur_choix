def validate_input_data(data: dict) -> str:
    # Vérification de la présence de toutes les clés nécessaires
    expected_keys = [
        'domicile_lat', 'domicile_lng', 'travail_lat', 'travail_lng', 'age',
        'retirement', 'frequency', 'home_office_days', 'fuel_consumption', 'emission_factor', 
    ]
    for key in expected_keys:
        if key not in data:
            return f"Le champ {key} est manquant."

    if not data['domicile_lat'] or not data['domicile_lng']:
        return "Veuillez entrer un point de départ."
    
    if not data['travail_lat'] or not data['travail_lng'] :
        return "Veuillez entrer un point d'arrivée."

    if not data['age']:
        return "Veuillez entrer votre age."
    if not data['retirement']:
        return "Veuillez entrer votre age à la retraire"

    # Validation de frequency
    try:
        freq_val = int(data['frequency'])
        if freq_val < 1 or freq_val > 5:
            raise ValueError
    except ValueError:
        return "Veuillez entrer un nombre valide pour la fréquence (entre 1 et 5)."

    # Validation de home_office_days
    try:
        home_office_days = int(data['home_office_days'])
        if home_office_days < 2 or home_office_days > 5:
            raise ValueError
    except ValueError:
        return "Veuillez entrer un nombre valide pour le nombre de jours en covoiturage (entre 2 et 5)."


    # Validation de fuel_consumption
    try:
        fuel_consumption = float(data['fuel_consumption'])
        if fuel_consumption <= 0:
            raise ValueError
    except ValueError:
        return "Veuillez entrer une consommation de carburant valide."


    return None  # Tout est valide
