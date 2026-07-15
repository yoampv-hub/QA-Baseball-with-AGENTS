from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JugadorPage:
    """Page Object para la gestión de bateadores.

    Nota sobre selectores: se priorizan `ID` cuando la app los expone
    (campos del formulario). Para los elementos de navegación del SPA
    (botones sin id ni data-testid estable) se usan XPath *relativos* por
    texto como último recurso permitido por SKILL.md — nunca XPath absolutos.
    """

    # Campos del formulario (IDs estables expuestos por la app)
    FIRST_NAME = (By.ID, "first_name")
    LAST_NAME = (By.ID, "last_name")
    JERSEY_NUMBER = (By.ID, "jersey_number")

    # Navegación / acciones (XPath relativo por texto — fallback documentado)
    NAV_BATEADORES = (By.XPATH, "//button[contains(., 'Bateadores')]")
    SECCION_BATEADORES = (
        By.XPATH,
        "//*[contains(text(), 'Bateadores') or contains(text(), 'Añadir')]",
    )
    BTN_ANADIR = (By.XPATH, "//button[text()='Añadir']")
    BTN_CREAR = (By.XPATH, "//button[text()='Crear Bateador']")
    BTN_CREAR_HABILITADO = (
        By.XPATH,
        "//button[text()='Crear Bateador' and not(@disabled)]",
    )

    # Toasts (sonner)
    TOAST_EXITO = (
        By.XPATH,
        "//*[@data-sonner-toast or contains(@class, 'toast')]"
        "[contains(., 'creado') or contains(., 'Bateador')]",
    )
    TOAST_ERROR = (
        By.XPATH,
        "//*[@data-sonner-toast or contains(@class, 'toast')]"
        "[contains(., 'Error') or contains(., 'error') or contains(., 'requerido')]",
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def ir_a_bateadores(self):
        """Navega a Bateadores vía sidebar link (mantiene auth del SPA)."""
        btn = self.wait.until(EC.presence_of_element_located(self.NAV_BATEADORES))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.visibility_of_element_located(self.SECCION_BATEADORES))

    def click_anadir(self):
        """Hace click en botón 'Añadir' y espera el formulario."""
        self.wait.until(EC.element_to_be_clickable(self.BTN_ANADIR)).click()
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))

    def llenar_formulario(self, datos):
        """Llena el formulario de creación de bateador (campos obligatorios)."""
        self.wait.until(
            EC.visibility_of_element_located(self.FIRST_NAME)
        ).send_keys(datos["nombre"])
        self.driver.find_element(*self.LAST_NAME).send_keys(datos["apellidos"])
        self.driver.find_element(*self.JERSEY_NUMBER).send_keys(datos["numero_camiseta"])

    def guardar(self):
        """Click en 'Crear Bateador' esperando a que esté habilitado."""
        self.wait.until(EC.element_to_be_clickable(self.BTN_CREAR_HABILITADO)).click()

    def boton_guardar_habilitado(self):
        """Devuelve True si el botón 'Crear Bateador' está habilitado."""
        return self.driver.find_element(*self.BTN_CREAR).is_enabled()

    def esperar_confirmacion(self):
        """Espera el toast de éxito (sonner)."""
        return self.wait.until(EC.visibility_of_element_located(self.TOAST_EXITO))

    def esperar_error(self):
        """Espera el toast de error."""
        return self.wait.until(EC.visibility_of_element_located(self.TOAST_ERROR))

    def limite_caracteres_nombre(self):
        """Obtiene el maxlength del campo nombre (o None si no está definido)."""
        return self.driver.find_element(*self.FIRST_NAME).get_attribute("maxlength")
