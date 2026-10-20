# Reporte de arquitectura | Automatizacion Web Bon-Bonite

**serenity · java · Screenplay**

> Se identificaron 8 escenarios distribuidos en 4 flujos de negocio. El código contiene 14 tareas reutilizables y 4 validaciones detectadas. 51 de 51 pasos tienen una definición de código asociada por análisis estático.

## Resumen para producto

- **Escenarios:** 8 en 4 flujos.
- **Trazabilidad estimada:** 51 de 51 (100%, estimación estática).
- **Acciones reutilizables:** 14 Tasks y 3 Interactions.
- **Validaciones detectadas:** 4 Questions.

## Cobertura del inventario

| Flujo de negocio | Escenarios | Pasos con definición / total |
|---|---:|---:|
| Actualizar dirección de facturación | 1 | 5 / 5 |
| Gestión de PQR | 1 | 6 / 6 |
| Gestion de compras de productos | 5 | 35 / 35 |
| Registro de usuario | 1 | 5 / 5 |

## Inventario de componentes

| Qué representa | Elementos detectados |
|---|---:|
| Flujos de negocio | 4 |
| Escenarios | 8 |
| Pasos definidos | 51 |
| Actores | 2 |
| Tareas reutilizables | 14 |
| Validaciones | 4 |
| Interacciones técnicas | 3 |
| Elementos de interfaz | 65 |
| Modelos de datos | 3 |
| Implementaciones de pasos | 4 |

## Escenarios y pasos

## Actualizar dirección de facturación

### Cambiar dirección y ciudad de facturación

Pasos identificados en código: 5 de 5.

- ✓ el usuario carga la informacion desde el Excel "1"
- ✓ el usuario esta en la pagina de bonBonite
- ✓ inicia sesion con su usuario
- ✓ actualiza su direccion de facturacion a "Cr 67 #54-77" y ciudad "Itagui"
- ✓ debe confirmar que la direccion de facturacion quedo guardada como "Cr 67 #54-77" en la ciudad "Itagui"

Acciones identificadas: CreateAccount, LoginBonBonite, OpenBrowser, OpenRegister, PurchaseProcessProduct, SelectCategory, SelectProduct, UpdateBillingAddress

## Gestión de PQR

### Crear una PQR exitosamente

Pasos identificados en código: 6 de 6.

- ✓ el usuario carga la informacion PQRS desde el Excel "<fila>"
- ✓ el usuario PQRS abre la pagina de bonBonite
- ✓ el usuario PQRS inicia sesion
- ✓ ingresa a la opcion crear solicitud PQRS
- ✓ diligencia el formulario con los datos requeridos
- ✓ el sistema genera un mensaje de confirmacion con el numero de radicado

Acciones identificadas: CreateAccount, LoginBonBonite, OpenBrowser, OpenPqrsPage, OpenRegister, SubmitPqrsRequest

## Gestion de compras de productos

### Compra exitosa de zapatos

Pasos identificados en código: 7 de 7.

- ✓ el usuario carga la informacion desde el Excel "<fila>"
- ✓ el usuario esta en la pagina de bonBonite
- ✓ inicia sesion con su usuario
- ✓ busca la categoria de "zapatos"
- ✓ selecciona un producto disponible
- ✓ realizamos el proceso de compra
- ✓ el sistema genera mensaje de confirmacion de compra con el numero de pedido

Acciones identificadas: CreateAccount, LoginBonBonite, OpenBrowser, OpenRegister, PurchaseProcessProduct, SelectCategory, SelectProduct

### Compra exitosa de bolsos

Pasos identificados en código: 7 de 7.

- ✓ el usuario carga la informacion desde el Excel "<fila>"
- ✓ el usuario esta en la pagina de bonBonite
- ✓ inicia sesion con su usuario
- ✓ busca la categoria de "bolsos"
- ✓ selecciona un producto disponible
- ✓ realizamos el proceso de compra
- ✓ el sistema genera mensaje de confirmacion de compra con el numero de pedido

Acciones identificadas: CreateAccount, LoginBonBonite, OpenBrowser, OpenRegister, PurchaseProcessProduct, SelectCategory, SelectProduct

### Compra exitosa de cinturones

Pasos identificados en código: 7 de 7.

- ✓ el usuario carga la informacion desde el Excel "<fila>"
- ✓ el usuario esta en la pagina de bonBonite
- ✓ inicia sesion con su usuario
- ✓ busca la categoria de "cinturones"
- ✓ selecciona un producto disponible
- ✓ realizamos el proceso de compra
- ✓ el sistema genera mensaje de confirmacion de compra con el numero de pedido

Acciones identificadas: CreateAccount, LoginBonBonite, OpenBrowser, OpenRegister, PurchaseProcessProduct, SelectCategory, SelectProduct

### Compra exitosa de accesorios

Pasos identificados en código: 7 de 7.

- ✓ el usuario carga la informacion desde el Excel "<fila>"
- ✓ el usuario esta en la pagina de bonBonite
- ✓ inicia sesion con su usuario
- ✓ busca la categoria de "accesorios"
- ✓ selecciona un producto disponible
- ✓ realizamos el proceso de compra
- ✓ el sistema genera mensaje de confirmacion de compra con el numero de pedido

Acciones identificadas: CreateAccount, LoginBonBonite, OpenBrowser, OpenRegister, PurchaseProcessProduct, SelectCategory, SelectProduct

### Compra exitosa en outlet

Pasos identificados en código: 7 de 7.

- ✓ el usuario carga la informacion desde el Excel "<fila>"
- ✓ el usuario esta en la pagina de bonBonite
- ✓ inicia sesion con su usuario
- ✓ busca la categoria de "outlet"
- ✓ selecciona un producto disponible
- ✓ realizamos el proceso de compra
- ✓ el sistema genera mensaje de confirmacion de compra con el numero de pedido

Acciones identificadas: CreateAccount, LoginBonBonite, OpenBrowser, OpenRegister, PurchaseProcessProduct, SelectCategory, SelectProduct

## Registro de usuario

### Registro exitoso

Pasos identificados en código: 5 de 5.

- ✓ el usuario carga la informacion desde el Excel "<fila>"
- ✓ el usuario esta en la pagina de bonBonite
- ✓ ingresa al formulario de registro
- ✓ ingresa sus datos correctamente
- ✓ deberia ver confirmacion de registro exitoso

Acciones identificadas: CreateAccount, OpenBrowser, OpenRegister

## Próximas acciones recomendadas

1. Los pasos de los escenarios tienen una definición asociada por análisis estático; confirmar la correspondencia durante una ejecución de pruebas.
2. Ejecutar la suite de automatización para conocer resultados, fallos y estabilidad; este análisis no ejecuta pruebas ni valida la aplicación.

## Alcance y calidad del análisis

Este reporte describe lo encontrado en el código y las especificaciones; no ejecuta pruebas, no confirma que la aplicación funcione y no equivale a cobertura de pruebas aprobadas. La relación entre un paso escrito y su definición de código es una estimación heurística.

Errores de lectura: 0.

- No se registraron errores de lectura.
