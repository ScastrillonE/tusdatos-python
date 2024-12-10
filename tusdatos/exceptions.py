class WebhookNotAllowedError(Exception):
    """Se genera si intentas usar webhooks en el ambiente de pruebas."""
    pass

class APIConnectionError(Exception):
    """Se genera cuando ocurre un error de conexión con la API."""
    pass
