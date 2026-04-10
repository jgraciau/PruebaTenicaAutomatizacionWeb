Feature: Registro de usuario

  @register
  Scenario Outline: Registro exitoso
    Given el usuario carga la informacion desde el Excel "<fila>"
      | rutaExcel                  | hoja           |
      | /excel/DatosPruebaWeb.xlsx | Datos Registro |
    And el usuario esta en la pagina de bonBonite
    When ingresa al formulario de registro
    And ingresa sus datos correctamente
    Then deberia ver confirmacion de registro exitoso
    Examples:
      | fila |
      | 1    |