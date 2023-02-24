def message(sensors: list):
    message = """Podczas ostatniego pomiaru temperatury nie udało się odczytać wartości z czyjników zapisanych jako\n\n\n"""
    for sensor in sensors:
        message += str(f"- {sensor}\n")
    message += "\n\nProszę sprawdzić czujniki"
    return message
