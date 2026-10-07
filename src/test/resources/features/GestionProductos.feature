Feature: Gestion de compras de productos

  @Zapatos @RegresionCompra
  Scenario Outline: Compra exitosa de zapatos
    Given el usuario carga la informacion desde el Excel "<fila>"
      | rutaExcel                  | hoja                |
      | /excel/DatosPruebaWeb.xlsx | Set Datos Productos |
    And el usuario esta en la pagina de bonBonite
    And inicia sesion con su usuario
    When busca la categoria de "zapatos"
    And selecciona un producto disponible
    And realizamos el proceso de compra
    Then el sistema genera mensaje de confirmacion de compra con el numero de pedido
    Examples:
      | fila |
      | 1    |
      | 2    |

  @Bolsos @RegresionCompra
  Scenario Outline: Compra exitosa de bolsos
    Given el usuario carga la informacion desde el Excel "<fila>"
      | rutaExcel                  | hoja                |
      | /excel/DatosPruebaWeb.xlsx | Set Datos Productos |
    And el usuario esta en la pagina de bonBonite
    And inicia sesion con su usuario
    When busca la categoria de "bolsos"
    And selecciona un producto disponible
    And realizamos el proceso de compra
    Then el sistema genera mensaje de confirmacion de compra con el numero de pedido

    Examples:
      | fila |
      | 2    |

  @Cinturones @RegresionCompra
  Scenario Outline: Compra exitosa de cinturones
    Given el usuario carga la informacion desde el Excel "<fila>"
      | rutaExcel                  | hoja                |
      | /excel/DatosPruebaWeb.xlsx | Set Datos Productos |
    And el usuario esta en la pagina de bonBonite
    And inicia sesion con su usuario
    When busca la categoria de "cinturones"
    And selecciona un producto disponible
    And realizamos el proceso de compra
    Then el sistema genera mensaje de confirmacion de compra con el numero de pedido

    Examples:
      | fila |
      | 3    |

  @Accesorios @RegresionCompra
  Scenario Outline: Compra exitosa de accesorios
    Given el usuario carga la informacion desde el Excel "<fila>"
      | rutaExcel                  | hoja                |
      | /excel/DatosPruebaWeb.xlsx | Set Datos Productos |
    And el usuario esta en la pagina de bonBonite
    And inicia sesion con su usuario
    When busca la categoria de "accesorios"
    And selecciona un producto disponible
    And realizamos el proceso de compra
    Then el sistema genera mensaje de confirmacion de compra con el numero de pedido
    Examples:
      | fila |
      | 4    |

  @Outlet @RegresionCompra
  Scenario Outline: Compra exitosa en outlet
    Given el usuario carga la informacion desde el Excel "<fila>"
      | rutaExcel                  | hoja                |
      | /excel/DatosPruebaWeb.xlsx | Set Datos Productos |
    And el usuario esta en la pagina de bonBonite
    And inicia sesion con su usuario
    When busca la categoria de "outlet"
    And selecciona un producto disponible
    And realizamos el proceso de compra
    Then el sistema genera mensaje de confirmacion de compra con el numero de pedido

    Examples:
      | fila |
      | 5    |