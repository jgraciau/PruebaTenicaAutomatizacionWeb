package userInterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public class ProductHome {
    public static final Target CATEGORIA = Target.the("categoría {0}")
            .locatedBy("//ul[@id='menu-categories-menu']//a[normalize-space()='{0}']");

    public static final Target PRODUCTO_LINK = Target.the("link producto {0}")
            .locatedBy("//h4[normalize-space()='{0}']/ancestor::div[contains(@class,'group')][1]"
                    + "//a[contains(@href,'/producto/')]");

    public static final Target TALLA = Target.the("talla {0}")
            .locatedBy("//button[@data-attribute_name='attribute_pa_talla' and @data-value='{0}']");

    public static final Target BOTON_COMPRAR_AHORA_URL = Target.the("botón comprar ahora")
            .locatedBy("//a[contains(@href,'add-to-cart')]");

    public static final Target BOTON_FINALIZAR_COMPRA = Target.the("botón finalizar compra")
            .locatedBy("//a[contains(@href,'finalizar-compra')]");

    public static final Target BOTON_CONTINUAR = Target.the("botón continuar")
            .locatedBy("//button[normalize-space()='Continuar']");



    public static final Target CHECKBOX_TERMINOS = Target.the("checkbox términos y condiciones")
            .locatedBy("//input[@id='terms']");

    public static final Target BOTON_REALIZAR_PEDIDO = Target.the("botón realizar compra")
            .located(By.id("place_order"));

    public static final Target TITULO_CHECKOUT = Target.the("título finalizar compra")
            .locatedBy("//h1[normalize-space()='Finalizar compra']");

    public static final Target NUMERO_PEDIDO = Target.the("número de pedido")
            .locatedBy(".woocommerce-order-overview__order strong");

    public static final Target FECHA_PEDIDO = Target.the("fecha del pedido")
            .locatedBy(".woocommerce-order-overview__date strong");

    public static final Target TOTAL_PEDIDO = Target.the("total del pedido")
            .locatedBy(".woocommerce-order-overview__total strong");

    public static final Target METODO_PAGO = Target.the("método de pago")
            .locatedBy(".woocommerce-order-overview__payment-method strong");
}
