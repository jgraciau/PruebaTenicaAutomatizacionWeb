Feature: Gestión de PQR

  @PQRS
  Scenario Outline: Crear una PQR exitosamente
    Given el usuario carga la informacion desde el Excel "<fila>"
      | rutaExcel                  | hoja           |
      | /excel/DatosPruebaWeb.xlsx | Set Datos PQRS |
    And el usuario esta en la pagina de bonBonite
    And inicia sesion con su usuario
    When ingresa a la opcion crear solicitud PQRS
    And diligencia el formulario con los datos requeridos
    Then el sistema generar  mensaje de confirmación con el numero de radicado

    Examples:
      | fila |
      | 1    |