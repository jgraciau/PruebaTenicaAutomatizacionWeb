Feature: Actualizar dirección de facturación

  @ActualizarFacturacion
  Scenario: Cambiar dirección y ciudad de facturación
    Given el usuario esta en la pagina de bonBonite
    And inicia sesion con su usuario
    When actualiza su direccion de facturacion a "Cr 67 #54-77" y ciudad "Itagui"
    Then debe confirmar que la direccion de facturacion quedo guardada como "Cr 67 #54-77" en la ciudad "Itagui"
