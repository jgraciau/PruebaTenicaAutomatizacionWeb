# Automatización web Bon-Bonite

Suite de automatización de interfaz web construida con Java, Gradle, Serenity BDD, Cucumber y Selenium. Los escenarios describen flujos de registro, compras, PQRS y actualización de la dirección de facturación en el sitio Bon-Bonite.

## Arquitectura

El proyecto usa el patrón Screenplay de Serenity:

1. Los archivos `.feature` expresan los escenarios en Gherkin.
2. Las definiciones de pasos de Cucumber traducen esos pasos a acciones.
3. Las `tasks` encapsulan acciones de los actores, como iniciar sesión o seleccionar un producto.
4. Las clases `userInterfaces` centralizan los selectores de la página.
5. Las `questions` consultan el estado de la interfaz para validar resultados.
6. `RunnerTest` inicia Cucumber mediante JUnit y Serenity genera los reportes.

### Estructura principal

| Ruta | Responsabilidad |
| --- | --- |
| `src/test/resources/features/` | Escenarios Gherkin para PQRS, compras, registro y facturación |
| `src/test/java/stepDefinitions/` | Enlace entre pasos de Cucumber y acciones Screenplay |
| `src/test/java/runners/RunnerTest.java` | Runner JUnit/Cucumber |
| `src/main/java/tasks/` | Acciones y flujos de usuario |
| `src/main/java/userInterfaces/` | Selectores de interfaz |
| `src/main/java/questions/` | Consultas y verificaciones |
| `src/main/java/utils/` | WebDriver y lectura de datos Excel |
| `src/test/resources/excel/` | Datos usados por los escenarios |

## Tecnologías y configuración

| Tecnología | Uso |
| --- | --- |
| Java 17 | Lenguaje y toolchain configurada en Gradle |
| Gradle 8.14.4 Wrapper | Construcción y ejecución reproducible |
| Serenity BDD 3.6.12 | Automatización Screenplay e informes |
| Cucumber 7.11.2 | Especificación BDD en Gherkin |
| JUnit 4.13.2 | Integración de pruebas |
| Selenium 4.18.1 | Automatización del navegador |
| WebDriverManager 5.7.0 | Gestión del controlador de Chrome |
| Apache POI 5.2.5 | Lectura de archivos Excel |

La codificación de compilación Java está fijada en UTF-8 para que la compilación sea consistente en sistemas con distintas configuraciones regionales.
Gradle pasa al proceso de pruebas solo propiedades `webdriver.*`, `serenity.*` y `cucumber.*`; no debe copiar propiedades internas como `java.home`, porque el proceso de pruebas utiliza el JDK de la toolchain.

## Requisitos previos

- Windows con PowerShell.
- JDK 17. El Wrapper descarga Gradle; la toolchain de Gradle debe poder localizar un JDK 17.
- Google Chrome instalado y acceso a Maven Central y al sitio bajo prueba para ejecutar escenarios de navegador.

Comprueba la versión de Java con:

```powershell
java -version
```

En el entorno donde se revisó este proyecto, Gradle localizó una instalación de JDK 17 aunque `java` en el `PATH` apuntaba a Java 21.

## Verificación rápida

Desde la carpeta del proyecto, ejecuta:

```powershell
.\gradlew.bat clean testClasses
```

Esto compila el código de producción y de pruebas, sin iniciar Chrome ni enviar datos al sitio. Es la verificación rápida recomendada para confirmar que el proyecto y sus dependencias compilan.

Para compilar y ejecutar el runner de Cucumber:

```powershell
.\gradlew.bat test --tests runners.RunnerTest
```

**Precaución:** la configuración predeterminada apunta a `https://www.bon-bonite.com/`. El único runner incluye todos los features, sin filtro de tags: registro, cinco outlines de compra (seis casos de ejemplo, dos para zapatos), PQRS y actualización de facturación, para nueve casos en total. Los escenarios de compra hacen clic en `place_order` y pueden crear pedidos reales; el registro puede crear una cuenta y el escenario de facturación guarda cambios persistentes en la cuenta. Ejecuta la suite completa únicamente contra un ambiente autorizado y con datos de prueba aprobados.

Las pruebas de compra requieren un usuario QA en el entorno del proceso que lanza Gradle; no vuelven a las credenciales obsoletas del Excel:

```powershell
$env:BONBONITE_TEST_USER = "<usuario QA autorizado>"
$env:BONBONITE_TEST_PASSWORD = "<contraseña QA>"
```

El registro requiere un correo de prueba controlado por el equipo. Debe aceptar alias `+` porque se añade un sufijo único para cada ejecución. La contraseña se toma de `BONBONITE_TEST_PASSWORD`:

```powershell
$env:BONBONITE_REGISTER_EMAIL = "<correo QA controlado>"
```

No guardes estos valores en el repositorio ni en la línea de comandos; define las variables en la sesión local antes de ejecutar. El test genera un identificador distinto y añade un sufijo al correo para evitar colisiones.

El escenario `@ActualizarFacturacion` reutiliza las credenciales QA `BONBONITE_TEST_USER` y `BONBONITE_TEST_PASSWORD`. Cambia y guarda la dirección por `Cr 67 #54-77` y la ciudad por `Itagui`. Para ejecutarlo únicamente en un ambiente QA autorizado:

```powershell
.\gradlew.bat test --tests runners.RunnerTest '-Dcucumber.filter.tags=@ActualizarFacturacion'
```

Esta ejecución modifica la información de facturación de la cuenta y persiste los valores; no es un dry-run.

El E2E de PQRS usa el formulario público y toma sus datos de variables de entorno, no del repositorio:

```powershell
$env:BONBONITE_PQRS_STORE = "<punto de venta visible en el formulario>"
$env:BONBONITE_PQRS_FULL_NAME = "<nombre de prueba autorizado>"
$env:BONBONITE_PQRS_ADDRESS = "<dirección de prueba>"
$env:BONBONITE_PQRS_DOCUMENT_TYPE = "CC"
$env:BONBONITE_PQRS_DOCUMENT_NUMBER = "<documento de prueba autorizado>"
$env:BONBONITE_PQRS_PHONE = "<teléfono de prueba>"
$env:BONBONITE_PQRS_EMAIL = "<correo de prueba>"
$env:BONBONITE_PQRS_REQUEST_TYPE = "Queja"
$env:BONBONITE_PQRS_DESCRIPTION = "<descripción de prueba>"
.\gradlew.bat test --tests runners.RunnerTest -Dheadless.mode=false
```

Usa únicamente identidad y valores de prueba aprobados. La propiedad `headless.mode=false` es necesaria porque Serenity se configura headless de forma predeterminada y el reCAPTCHA requiere interacción visible. El escenario espera hasta cinco minutos a que una persona lo resuelva; después envía la solicitud y valida el número de radicado. La ejecución crea una solicitud persistente. `BONBONITE_PQRS_CAUSE` se debe definir si el tipo elegido muestra un campo de causal obligatorio.

Se puede sobreescribir la URL de Serenity con una propiedad de Gradle:

```powershell
.\gradlew.bat test --tests runners.RunnerTest -Dwebdriver.base.url=https://<url-autorizada-de-qa>/
```

Usa únicamente una URL de QA autorizada y asegúrate de que los datos Excel correspondan a cuentas de prueba. No incluyas credenciales reales en el código o en la documentación.

## Reportes

Serenity genera reportes bajo `target/site/serenity`. Gradle también configura la salida JSON de Cucumber en `target/cucumber-json-report.json`.

## Estado y limitaciones conocidas

- `RunnerTest` ejecuta todos los features del proyecto; no utiliza filtro de tags.
- Análisis de la última ejecución E2E completa antes de los cambios recientes: 7 escenarios; zapatos y bolsos pasaron. PQRS no tenía configuradas las nueve variables de datos; cinturones no encontró la variante seleccionada al cargar; accesorios y outlet no encontraron el enlace de cuenta; el registro no llegó a una sesión autenticada. Esta ejecución no se debe confundir con el `dry-run`.
- Mantenimiento aplicado: login y registro navegan directamente a `/mi-cuenta/` en vez de depender de una posición fija de enlace; la selección de producto espera el enlace y las variantes asíncronas; la confirmación de compra espera el número de orden de WooCommerce; el registro espera la sesión autenticada o un error de formulario antes de validar el resultado.
- Reanálisis autorizado posterior, solo para los cuatro casos que habían fallado: cinturones, accesorios y outlet se detuvieron antes de buscar productos o enviar pedidos porque el sitio rechazó el usuario configurado; el registro agotó el tiempo esperando una respuesta tras enviar el formulario. Los tres casos de compra no llegaron a enviar pedidos en esa ejecución. El estado final del registro no se pudo confirmar; verifica el resultado en el sitio antes de repetir el registro para evitar duplicados.
- Ajuste tras ese reanálisis: login y registro requieren credenciales QA suministradas por entorno (sin fallback al Excel), distinguen rechazo de espera agotada y reportan fallos de validación de forma explícita.
- Los cuatro nombres de producto inicialmente descontinuados se reemplazaron por opciones publicadas: Baleta en cuero borgoña (talla 35), Manos libres en cuero luna, Cinturón en cuero negro (talla 14) y Baleta en cuero con glitter color negro ónix (talla 39). La fila de accesorios se conserva.
- PQRS usa el formulario real y valida el radicado, pero no se envía si faltan datos de prueba aprobados; en ese caso Cucumber lo reporta como pendiente. No se inventan datos para producción.
- Verificación segura posterior a corregir el paso Then de registro: `.\gradlew.bat clean testClasses` compiló correctamente y `.\gradlew.bat test --tests runners.RunnerTest '-Dcucumber.execution.dry-run=true'` resolvió los 8 casos. El `dry-run` no abre navegador ni comprueba el comportamiento E2E.
- El último intento de reejecución quedó detenido antes de Gradle porque las variables `BONBONITE_TEST_USER`, `BONBONITE_TEST_PASSWORD` y `BONBONITE_REGISTER_EMAIL` no estaban disponibles en el entorno del proceso. No se inició otra sesión de navegador.
- Verificación del pre-requisito de PQRS: al filtrar `@PQRS` sin variables, el hook detuvo el escenario antes de abrir Chrome; Gradle reporta `PendingException` como fallo, no como test ignorado. Esto evita presentar una solicitud vacía, pero la suite seguirá roja hasta configurar datos de prueba aprobados.
- No se relanzaron los escenarios mutadores después del último ajuste: los casos de compra aprobados antes ya pueden haber creado pedidos; completar los escenarios de cinturones, accesorios u outlet puede crear pedidos adicionales, y el registro podría crear otra cuenta. PQRS crea un expediente real y exige CAPTCHA visible. Para un E2E completo se requiere QA/CAPTCHA de prueba o autorización específica de cada efecto persistente.
- La URL predeterminada es el sitio público. Para automatización habitual conviene configurar un ambiente de QA y datos de prueba dedicados antes de ejecutar E2E.
