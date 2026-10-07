package tasks;

import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import net.serenitybdd.screenplay.actions.Clear;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.actions.Enter;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;
import userInterfaces.BillingAddressPage;

import java.time.Duration;

public class UpdateBillingAddress implements Task {
    private static final By BILLING_ADDRESS_EDIT_LINK = By.xpath(
            "//div[contains(@class,'woocommerce-Address')]" +
                    "[.//h2[contains(.,'facturación')]]//a[contains(@class,'edit')]"
    );

    private final String address;
    private final String city;

    public UpdateBillingAddress(String address, String city) {
        this.address = address;
        this.city = city;
    }

    public static UpdateBillingAddress to(String address, String city) {
        return Tasks.instrumented(UpdateBillingAddress.class, address, city);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        if (address == null || address.isBlank() || city == null || city.isBlank()) {
            throw new IllegalArgumentException("La dirección y la ciudad de facturación son obligatorias");
        }

        WebDriver driver = BrowseTheWeb.as(actor).getDriver();
        WebElement editLink = new WebDriverWait(driver, Duration.ofSeconds(20))
                .withMessage("No se encontró el enlace para editar la dirección de facturación")
                .until(currentDriver -> currentDriver.findElements(BILLING_ADDRESS_EDIT_LINK)
                        .stream()
                        .filter(WebElement::isDisplayed)
                        .findFirst()
                        .orElse(null));
        String editUrl = editLink.getAttribute("href");
        if (editUrl == null || editUrl.isBlank()) {
            throw new IllegalStateException("El enlace de edición de facturación no tiene una URL válida");
        }

        driver.navigate().to(editUrl);
        new WebDriverWait(driver, Duration.ofSeconds(20))
                .withMessage("No cargó el formulario de dirección de facturación")
                .until(currentDriver -> currentDriver.findElements(By.id("billing_address_1"))
                        .stream()
                        .anyMatch(WebElement::isDisplayed));

        actor.attemptsTo(
                Clear.field(BillingAddressPage.ADDRESS),
                Enter.theValue(address).into(BillingAddressPage.ADDRESS),
                Clear.field(BillingAddressPage.CITY),
                Enter.theValue(city).into(BillingAddressPage.CITY),
                Click.on(BillingAddressPage.SAVE_ADDRESS)
        );

        new WebDriverWait(driver, Duration.ofSeconds(20))
                .withMessage("El sitio no confirmó que guardó la dirección de facturación")
                .until(currentDriver -> currentDriver.findElements(By.cssSelector(".woocommerce-message"))
                        .stream()
                        .anyMatch(WebElement::isDisplayed));
    }
}
