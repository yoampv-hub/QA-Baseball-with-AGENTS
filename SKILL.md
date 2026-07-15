# Estándares de Calidad — QA Automation (Selenium + Pytest)

> Skill de referencia obligatoria. Todo código de automatización se audita
> contra estas reglas antes de aprobarse.

## 1. Selectores estratégicos
- **OBLIGATORIO:** priorizar selectores robustos: `ID`, `NAME` o atributos de
  datos (`data-testid`).
- **PERMITIDO como último recurso:** XPath **relativo** estable (por texto o
  estructura acotada) cuando la app no expone id/name/data-testid. Debe
  documentarse con un comentario el porqué.
- **PROHIBIDO:** XPath **absolutos** (`/html/body/div[2]/...`) y selectores
  frágiles dependientes de posición.

## 2. Gestión del tiempo (waits)
- **OBLIGATORIO:** usar `WebDriverWait` con `expected_conditions` (esperas
  explícitas).
- **PROHIBIDO:** `time.sleep()`.
- **PROHIBIDO:** mezclar `implicitly_wait()` con esperas explícitas — genera
  timeouts impredecibles y flakiness. Usar únicamente esperas explícitas.

## 3. Aserciones (asserts)
- Todo test debe terminar con al menos un `assert` claro que valide el
  resultado esperado.
- Preferir comprobaciones de estado del WebElement (`is_enabled()`,
  `is_displayed()`) sobre comparar atributos crudos (`get_attribute`).

## 4. Arquitectura y limpieza
- **Page Object Model:** localizadores y acciones encapsulados en `pages/`.
  Los tests no contienen selectores crudos.
- Selectores repetidos definidos como **constantes** de la clase Page.
- Sin imports muertos ni lógica duplicada.

## 5. Evidencia
- Captura automática de **screenshot en cada fallo** (hook en `conftest.py`).
- Ejecuciones producen **reporte HTML** (`pytest-html`) en `reports/`.

## 6. Secretos y configuración
- Credenciales y URLs **solo** vía variables de entorno (`.env`, cargado con
  `python-dotenv`). Nunca hardcodeadas.
- `.env` siempre en `.gitignore`; se versiona un `.env.example` sin secretos.
