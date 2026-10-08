package userInterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public class BillingAddressPage {
    public static final Target DATA_LINK = Target.the("opción Datos de la cuenta")
            .located(By.xpath("(//ul[contains(@class,'whitespace-nowrap')]//li[contains(concat(' ', normalize-space(@class), ' '), ' woocommerce-MyAccount-navigation-link--edit-account ')]//a[contains(@href,'/mi-cuenta/edit-account/') and normalize-space()='Datos'])[1]"));

    public static final Target BILLING_SECTION = Target.the("sección dirección de facturación")
            .located(By.cssSelector("#billing-address-view"));

    public static final Target EDIT_BILLING_ADDRESS = Target.the("editar dirección de facturación")
            .located(By.xpath("//*[@id='billing-address-view']/ancestor::*[contains(@class,'address-section')][1]//button[contains(@class,'edit-address-button') and @data-address-type='billing']"));

    public static final Target ADDRESS_MODAL = Target.the("modal de dirección")
            .located(By.id("address-form-container"));

    public static final Target ADDRESS = Target.the("dirección de facturación")
            .located(By.cssSelector("#address-form-container input[name='billing_address_1'], #billing_address_1"));

    public static final Target CITY = Target.the("ciudad de facturación")
            .located(By.cssSelector("#address-form-container #billing_city, #address-form-container select[name='billing_city'], #billing_city"));

    public static final Target SAVE_ADDRESS = Target.the("guardar dirección de facturación")
            .located(By.cssSelector("#address-form-container button[type='submit'], #address-form-container input[type='submit']"));

    public static final Target SUCCESS_MESSAGE = Target.the("confirmación de dirección guardada")
            .located(By.xpath("//*[contains(normalize-space(.),'Dirección guardada correctamente') or contains(normalize-space(.),'dirección guardada correctamente')]"));
}
