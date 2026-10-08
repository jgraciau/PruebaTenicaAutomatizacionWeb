Feature: Gestión de PQR

  @PQRS @Destructive @ManualGate @RequiresQAData
  Scenario: Crear una PQR exitosamente
    Given el usuario esta en la pagina de PQRS
    When ingresa a la opcion crear solicitud PQRS
    And diligencia el formulario con los datos requeridos
    Then el sistema genera un mensaje de confirmacion con el numero de radicado