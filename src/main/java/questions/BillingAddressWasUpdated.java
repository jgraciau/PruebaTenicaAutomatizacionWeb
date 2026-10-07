package questions;

import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Question;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;

public class BillingAddressWasUpdated implements Question<Boolean> {
    private final String expectedAddress;
    private final String expectedCity;

    public BillingAddressWasUpdated(String expectedAddress, String expectedCity) {
        this.expectedAddress = expectedAddress;
        this.expectedCity = expectedCity;
    }

    public static BillingAddressWasUpdated to(String address, String city) {
        return new BillingAddressWasUpdated(address, city);
    }

    @Override
    public Boolean answeredBy(Actor actor) {
        var driver = BrowseTheWeb.as(actor).getDriver();
        boolean successMessageVisible = driver.findElements(By.cssSelector(".woocommerce-message"))
                .stream()
                .anyMatch(WebElement::isDisplayed);
        String savedAddress = driver.findElement(By.id("billing_address_1")).getAttribute("value");
        String savedCity = driver.findElement(By.id("billing_city")).getAttribute("value");

        return successMessageVisible
                && expectedAddress.equals(savedAddress)
                && expectedCity.equals(savedCity);
    }
}
