def validate_response(response):
    """Valida si la respuesta HTTP fue exitosa."""
    if not isinstance(response, dict):
        raise ValueError("La respuesta no tiene un formato válido.")
    if "status" in response and response["status"] != "success":
        raise ValueError(f"Error en la API: {response.get('message', 'Error desconocido.')}")
