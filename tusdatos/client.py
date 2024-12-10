import requests
from typing import Any, Dict, Optional
from .config import PRODUCTION_URL, TESTING_URL
from .exceptions import APIConnectionError

class DataService:
    def __init__(self, environment: str = "production", username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the client to interact with the TusDatos.co API.

        :param environment: Environment to use ('production' or 'testing').
        :param username: Username for authentication.
        :param password: Password for authentication.
        """
        self._validate_environment(environment)
        self.base_url = PRODUCTION_URL if environment == "production" else TESTING_URL
        self.client = self._initialize_client(username, password)

    @staticmethod
    def _validate_environment(environment: str):
        """Validate that the specified environment is valid."""
        if environment not in ["production", "testing"]:
            raise ValueError("Environment must be 'production' or 'testing'.")

    @staticmethod
    def _initialize_client(username: Optional[str], password: Optional[str]) -> requests.Session:
        """Initialize the HTTP client configuration."""
        session = requests.Session()
        session.auth = (username or "pruebas", password or "password")
        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        return session

    def _send_request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Send an HTTP request to the TusDatos.co server.

        :param method: HTTP method (GET or POST).
        :param endpoint: Relative endpoint for the request.
        :param kwargs: Additional parameters for the request.
        :return: JSON response from the server.
        """
        url = f"{self.base_url}{endpoint}"
        timeout = kwargs.pop("timeout", 10)
        try:
            response = self.client.request(method, url, timeout=timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise APIConnectionError(f"HTTP Error: {http_err.response.status_code}") from http_err
        except requests.RequestException as ex:
            raise APIConnectionError(f"Connection error with the API: {ex}")

    def start_query(self, document: str, doc_type: str, issue_date: Optional[str] = None) -> Any:
        """
        Start a background check query for a document.

        :param document: Document number.
        :param doc_type: Document type (CC, CE, etc.).
        :param issue_date: Issue date (optional).
        :return: Query result.
        """
        payload = {"doc": document, "typedoc": doc_type}
        if issue_date:
            payload["fechaE"] = issue_date
        return self._send_request("POST", "/api/launch", json=payload)

    def results(self, idarg: str) -> Any:
        """
        Get the status and result of a previous query.

        :param idarg: Result ID.
        :return: Query details.
        """
        return self._send_request("GET", f"/api/results/{idarg}")

    def retry(self, payload: Dict[str, Any]) -> Any:
        """
        Retry loading sources with errors in a previous query.

        :param payload: Dictionary with 'id' and 'typedoc'.
        :return: Retry result.
        """
        return self._send_request("GET", f"/api/retry/{payload['id']}", params={"typedoc": payload["typedoc"]})

    def vehicle_query(self, owner_doc: str, doc_type: str, license_plate: str) -> Any:
        """
        Perform a query to validate a vehicle.

        :param owner_doc: Owner's document.
        :param doc_type: Owner's document type.
        :param license_plate: Vehicle license plate.
        :return: Query result.
        """
        payload = {"doc": owner_doc, "typedoc": doc_type, "placa": license_plate}
        return self._send_request("POST", "/api/launch/car", json=payload)

    def report(self, idarg: str) -> Any:
        """
        Generate an HTML report.

        :param idarg: Report ID.
        :return: Report content in HTML.
        """
        return self._send_request("GET", f"/api/report/{idarg}")

    def report_pdf(self, idarg: str) -> Any:
        """
        Generate a report in PDF format.

        :param idarg: Report ID.
        :return: Report content in PDF.
        """
        return self._send_request("GET", f"/api/report_pdf/{idarg}")

    def report_json(self, idarg: str) -> Any:
        """
        Generate a report in JSON format.

        :param idarg: Report ID.
        :return: Report content in JSON.
        """
        return self._send_request("GET", f"/api/report_json/{idarg}")

    def plan_status(self) -> Any:
        """
        Check the user's plan status.

        :return: Plan status details.
        """
        return self._send_request("GET", "/api/plans")

    def query_history(self) -> Any:
        """
        Retrieve the history of performed queries.

        :return: Query history details.
        """
        return self._send_request("GET", "/api/querys")

    def launch_verify(self, payload: Dict[str, Any]) -> Any:
        """
        Verify a person's identity through the /api/launch/verify endpoint.

        :param payload: Dictionary with required verification data.
                        Must include:
                        - "doc": Identity document number.
                        - "typedoc": Document type (CC, CE, etc.).
                        - "fechaE": Document issue date.
        :return: Server JSON response.
        """
        return self._send_request("POST", "/api/launch/verify", json=payload)

    def launch_verify_nit(self, payload: Dict[str, Any]) -> Any:
        """
        Verify company information by its NIT using the /api/launch/verify/nit endpoint.

        :param payload: Dictionary with required verification data.
                        Must include:
                        - "nit": Tax Identification Number (NIT).
        :return: Server JSON response.
        """
        return self._send_request("POST", "/api/launch/verify/nit", json=payload)
