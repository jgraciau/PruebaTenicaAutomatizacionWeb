Feature: Actualizar dirección de facturación

  @Smoke @Destructive @RequiresQAData @ActualizarFacturacion
  Scenario: Cambiar dirección y ciudad de facturación
    Given el usuario carga la informacion desde el Excel "1"
      | rutaExcel                  | hoja                  |
      | /excel/DatosPruebaWeb.xlsx | Set Datos PQRS |
    And el usuario esta en la pagina de bonBonite
    And inicia sesion con su usuario
    When actualiza su direccion de facturacion a "Cr 67 #54-77" y ciudad "Itagui"
    Then debe confirmar que la direccion de facturacion quedo guardada como "Cr 67 #54-77" en la ciudad "Itagui"
