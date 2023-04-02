def message(sensors: list) -> str:
    """
    This function prepares an email message with the temperature
    measurement devices that could not be connected to.

    :params sensors: a list of devices that could not be connected to

    :return: message for email
    """

    message = """Podczas ostatniego pomiaru temperatury nie udało się odczytać wartości z czyjników zapisanych jako\n\n\n"""
    for sensor in sensors:
        message += str(f"- {sensor}\n")
    message += "\n\nProszę sprawdzić czujniki"
    return message
