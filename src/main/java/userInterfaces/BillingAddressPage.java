package userInterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public class BillingAddressPage {

    public static final Target ADDRESS = Target.the("dirección de facturación")
            .located(By.id("billing_address_1"));

    public static final Target CITY = Target.the("ciudad de facturación")
            .located(By.id("billing_city"));

    public static final Target SAVE_ADDRESS = Target.the("guardar dirección de facturación")
            .located(By.name("save_address"));

    public static final Target SUCCESS_MESSAGE = Target.the("confirmación de dirección guardada")
            .located(By.cssSelector(".woocommerce-message"));
}
