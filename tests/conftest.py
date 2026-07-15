import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")


def _headless_enabled():
    return os.getenv("HEADLESS", "true").lower() != "false"


@pytest.fixture(scope="function")
def driver():
    options = Options()
    if _headless_enabled():
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    # Solo esperas explícitas (WebDriverWait). No mezclar implicit + explicit waits.
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura un screenshot automáticamente cuando un test falla."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"FAIL_{item.name}_{timestamp}.png"
            path = os.path.join(SCREENSHOTS_DIR, filename)
            try:
                drv.save_screenshot(path)
                print(f"\n[EVIDENCIA] Screenshot del fallo guardado en: {path}")
            except Exception as exc:  # pragma: no cover - evidencia best-effort
                print(f"\n[EVIDENCIA] No se pudo capturar screenshot: {exc}")
