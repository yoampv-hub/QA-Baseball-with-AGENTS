import os
import pytest
from dotenv import load_dotenv
from pages.login_page import LoginPage
from pages.jugador_page import JugadorPage

load_dotenv()

URL = os.getenv("APP_URL")
EMAIL = os.getenv("APP_USER")
PASSWORD = os.getenv("APP_PASS")

DATOS_VALIDOS = {
    "nombre": "Juan",
    "apellidos": "Perez",
    "numero_camiseta": "25",
}


class TestCrearJugador:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.login_page = LoginPage(driver)
        self.jugador_page = JugadorPage(driver)
        self.login_page.navigate(URL)
        self.login_page.login(EMAIL, PASSWORD)
        self.login_page.wait_for_login_complete()

    def login_y_navegar(self):
        self.jugador_page.ir_a_bateadores()
        self.jugador_page.click_anadir()

    # CP-001 Happy Path: Creación exitosa de un nuevo jugador
    @pytest.mark.smoke
    @pytest.mark.happy_path
    def test_crear_jugador_exitoso(self, driver):
        self.login_y_navegar()
        self.jugador_page.llenar_formulario(DATOS_VALIDOS)
        self.jugador_page.guardar()
        mensaje = self.jugador_page.esperar_confirmacion()
        assert mensaje.is_displayed()

    # CP-002 Error Path: Botón deshabilitado con campos obligatorios vacíos
    @pytest.mark.regression
    @pytest.mark.error_path
    def test_crear_jugador_campos_vacios(self, driver):
        self.login_y_navegar()
        self.jugador_page.llenar_formulario({
            "nombre": "",
            "apellidos": "",
            "numero_camiseta": "",
        })
        # Verificar que el botón de guardar permanece deshabilitado
        assert not self.jugador_page.boton_guardar_habilitado()

    # CP-003 Edge Case: Caracteres especiales en el nombre
    @pytest.mark.regression
    @pytest.mark.edge_case
    def test_crear_jugador_nombre_caracteres_especiales(self, driver):
        self.login_y_navegar()
        datos_especiales = dict(DATOS_VALIDOS)
        datos_especiales["nombre"] = "Juán Pérez-O'Brien & García"
        maxlength = self.jugador_page.limite_caracteres_nombre()
        if maxlength and int(maxlength) < len(datos_especiales["nombre"]):
            datos_especiales["nombre"] = datos_especiales["nombre"][: int(maxlength)]
        self.jugador_page.llenar_formulario(datos_especiales)
        self.jugador_page.guardar()
        mensaje = self.jugador_page.esperar_confirmacion()
        assert mensaje.is_displayed()