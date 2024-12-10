import pytest
import requests
from unittest.mock import patch, Mock
from tusdatos.client import DataService
from tusdatos.exceptions import APIConnectionError


@pytest.fixture
def data_service():
    """Fixture para inicializar el servicio en ambiente de pruebas."""
    return DataService(environment="testing")


@patch("tusdatos.client.requests.Session.request")
def test_start_query(mock_request, data_service):
    """Prueba el método start_query."""
    # Configuración del mock para el endpoint
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "email": "usuario@pruebas.com",
        "doc": 111,
        "jobid": "6460fc34-4154-43db-9438-8c5a059304c0",
        "nombre": "MIGUEL FERNANDO PEREZ GOMEZ",
        "typedoc": "CC",
        "validado": True,
    }
    mock_request.return_value = mock_response

    # Ejecución
    response = data_service.start_query(
        document=111, doc_type="CC", issue_date="01/12/2014"
    )

    # Validaciones
    assert response["doc"] == 111
    assert response["typedoc"] == "CC"
    assert response["validado"] is True
    assert "jobid" in response


@patch("tusdatos.client.requests.Session.request")
def test_results(mock_request, data_service):
    """Prueba el método results."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "details": "Consulta exitosa",
    }
    mock_request.return_value = mock_response

    jobid = "6460fc34-4154-43db-9438-8c5a059304c0"
    response = data_service.results(jobid)

    assert response["status"] == "success"
    assert response["details"] == "Consulta exitosa"


@patch("tusdatos.client.requests.Session.request")
def test_retry(mock_request, data_service):
    """Prueba el método retry."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "details": "Reintento exitoso",
    }
    mock_request.return_value = mock_response

    payload = {"id": "6460fc34-4154-43db-9438-8c5a059304c0", "typedoc": "CC"}
    response = data_service.retry(payload)

    assert response["status"] == "success"
    assert response["details"] == "Reintento exitoso"


@patch("tusdatos.client.requests.Session.request")
def test_start_query_connection_error(mock_request, data_service):
    """Prueba que se maneje correctamente un error de conexión."""
    mock_request.side_effect = requests.RequestException("Error de conexión")

    with pytest.raises(APIConnectionError) as excinfo:
        data_service.start_query(
            document=111, doc_type="CC", issue_date="01/12/2014"
        )

    assert "Connection error with the API" in str(excinfo.value)

@patch("tusdatos.client.requests.Session.request")
def test_results_invalid_status(mock_request, data_service):
    """Test that the results method handles an invalid HTTP status code."""
    # Mock a response with an invalid HTTP status code
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.reason = "Internal Server Error"
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        response=mock_response
    )
    mock_request.return_value = mock_response

    jobid = "6460fc34-4154-43db-9438-8c5a059304c0"

    # Execute and verify the expected exception
    with pytest.raises(APIConnectionError) as excinfo:
        data_service.results(jobid)

    # Adjust the assertion to match the actual exception message
    assert "HTTP Error: 500" in str(excinfo.value)


@patch("tusdatos.client.requests.Session.request")
def test_results_valid_response(mock_request, data_service):
    """Prueba que el método results maneje correctamente una respuesta válida."""
    # Simula la respuesta del endpoint
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "cedula": 111,
        "error": False,
        "errores": [],
        "estado": "finalizado",
        "hallazgo": True,
        "hallazgos": "Alto",
        "id": "651c2ede72476080772781f5",
        "nombre": "MIGUEL FERNANDO PEREZ GOMEZ",
        "results": {
            "Analisis Reputacional": True,
            "Asociaciones Profesionales": True,
            "CIDOB Peps nivel mundial": True,
            "Concordato de Supersociedades": True,
            "Consejo de Seguridad de la Naciones Unidas (ONU)": True,
            "Contadores Sancionados": True,
            "Contraloría General de la Republica (Consulta en Linea)": True,
            "Contratación Pública en SECOP1 ": True,
            "Contratación Pública en SECOP2 ": True,
            "DIAN (Proveedores Ficticios)": True,
            "Delitos sexuales contra menores de edad": True,
            "Empresas y Personas Sancionadas Banco Interamericano de Desarrollo (IADB)": True,
            "European Union Most Wanted List (EUROPOL)": True,
            "Fondo de Pensiones Publicas (FOPEP)": True,
            "Histórico de multas en Bogotá (SIMUR)": True,
            "Instituto Nacional Penitenciario y Carcelario (INPEC)": True,
            "Juzgados Tyba - Justicia XXI": True,
            "Libreta Militar": True,
            "Lista Clinton (OFAC), Busqueda por Documento (Consulta en Línea)": True,
            "Lista Clinton (OFAC), Busqueda por Nombre (Consulta en Línea)": True,
            "Listado del Banco Mundial de empresas e individuos no elegibles": True,
            "Listas y PEPs (Personas Expuestas Políticamente), Busqueda por Documento": True,
            "Listas y PEPs (Personas Expuestas Políticamente), Busqueda por Nombre": True,
            "Offshore Leaks Database (ICJI)": True,
            "Organización Internacional de Policía Criminal (INTERPOL)": True,
            "Personeria de Bogota": True,
            "Policia Nacional de Colombia": True,
            "Procuraduría General de la Nación (Consulta en Linea)": True,
            "RGM Registro de Garantías Mobiliarias": True,
            "Rama Judicial Unificada, Busqueda por Nombre": True,
            "Registraduría Nacional del Estado Civil": True,
            "Registro Nacional de Carga (RNDC)": True,
            "Registro Nacional de Medidas Correctivas (RNMC)": True,
            "Registro Único Empresarial y Social (RUES)": True,
            "Registro Único Nacional de Tránsito (RUNT)": True,
            "Registro Único Tributario (RUT)": True,
            "Sancionados contratación pública SECOP": True,
            "Servicio Nacional de Aprendizaje (SENA)": True,
            "Sistema Integrado de Multas y Sanciones de Transito (SIMIT)": True,
            "Sistema de Información de Conductores que Transportan Mercancías Peligrosa (SISCONMP)": True,
            "Sistema de Información del Registro Nacional de Abogados (SIRNA)": True,
            "Sistema de Información y Gestión del Empleo Público (SIGEP)": True,
            "Sistema de Seguridad Social Subsidiado (SISBEN)": True,
            "Vehículos inmovilizados Bogotá": True
        },
        "time": 42.67135,
        "typedoc": "CC",
        "validado": True
    }
    mock_request.return_value = mock_response

    # ID de prueba
    jobid = "6460fc34-4154-43db-9438-8c5a059304c0"

    # Llamar al método y validar la respuesta
    response = data_service.results(jobid)
    assert response["cedula"] == 111
    assert response["estado"] == "finalizado"
    assert response["hallazgos"] == "Alto"
    assert response["nombre"] == "MIGUEL FERNANDO PEREZ GOMEZ"
    assert response["validado"] is True
    assert response["results"]["Analisis Reputacional"] is True
    assert response["results"]["Sistema de Seguridad Social Subsidiado (SISBEN)"] is True

def test_report_json(data_service):
    """Prueba el método report_json contra el API real."""
    # ID de prueba
    report_id = "651c2ede72476080772781f5"

    # Ejecutar el método
    response = data_service.report_json(report_id)

    # Validaciones
    assert response["cidob"]["Cargo"] == "Primer ministro (2010-2014)"
    assert response["cidob"]["Pais"] == "Pais pruebas"
    assert response["contaduria"] is True
    assert response["errores"] == []
    assert response["nombre"] == "MIGUEL FERNANDO PEREZ GOMEZ"
    assert response["hallazgos"] == "alto"
    assert "reputacional" in response
    reputacional = response["reputacional"]

    # Validar información de noticias
    if "news" in reputacional:
        news = reputacional["news"]
        assert isinstance(news, list)  # Validar que es una lista
        assert len(news) > 0  # Verificar que tiene al menos un elemento
        assert news[0]["title"] == "Titulo de prueba"
        assert news[0]["description"] == "Se encontro que aparecio en una noticia de prueba"

    # Validar información de redes sociales
    if "social" in reputacional:
        social = reputacional["social"]
        assert isinstance(social, list)  # Validar que es una lista
        assert len(social) > 0  # Verificar que tiene al menos un elemento
        assert social[0]["title"] == "Titulo de prueba"
        assert social[0]["description"] == "Ve el perfil de prueba de MIGUEL FERNANDO PEREZ GOMEZ"

    # Validar un hallazgo específico en dict_hallazgos
    assert response["dict_hallazgos"]["altos"][0]["codigo"] == "sirna"
    assert response["dict_hallazgos"]["altos"][0]["hallazgo"] == (
        "SIRNA: Esta sancionado en el Sistema de Información del Registro Nacional de Abogados"
    )

    # Validar información básica de Europol
    assert response["europol"]["name"] == "PEREZ GOMEZ, Miguel Fernando"
    assert response["europol"]["status"] == "Wanted by prueba"

    # Validar la información de FOPEP
    assert response["fopep"]["documento"] == "111"
    assert response["fopep"]["tipo_documento"] == "CC"
    assert response["fopep"]["fecha_inclusion"] == "2014-12-01"


def test_launch_verify(data_service):
    """Prueba el método launch_verify contra el API real."""
    # Datos de prueba para la consulta
    payload = {
        "doc": 123456,
        "typedoc": "CC",
        "fechaE": "01/01/2015"
    }

    # Ejecutar el método
    response = data_service.launch_verify(payload)

    # Validaciones básicas
    assert response["data"]["nuip"] == 123456
    assert response["data"]["primer_apellido"] == "APELLIDO"
    assert response["data"]["primer_nombre"] == "APELLIDO"
    assert response["data"]["segundo_apellido"] == "NOMBRE"
    assert response["data"]["segundo_nombre"] == "NOMBRE"

    # Validar findings
    assert response["findings"] == ["Nombre no coincide", "Fecha de expedición no coincide"]

    # Validar el estado
    assert response["status"] == "true"


def test_launch_verify_nit(data_service):
    """Prueba el método launch_verify_nit contra el API real."""
    # Datos de entrada
    payload = {
        "nit": 901235691
    }

    # Ejecutar el método
    response = data_service.launch_verify_nit(payload)

    # Validaciones de respuesta
    assert response["data"]["nit"] == 901235691
    assert response["data"]["razon_social"] == "DATA FACTUM SAS"
    assert response["data"]["estado"] == "ACTIVA"
    assert response["data"]["tipo"] == "SOCIEDAD COMERCIAL"
    assert response["data"]["categoria_matricula"] == "SOCIEDAD ó PERSONA JURIDICA PRINCIPAL ó ESAL"
    assert response["data"]["clase_identificacion"] == "NIT"
    assert response["data"]["nombre_camara"] == "BOGOTA"

    # Validar findings y status
    assert response["findings"] == []
    assert response["status"] == "true"