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

        String pageText = driver.findElements(By.tagName("body")).stream()
                .filter(WebElement::isDisplayed)
                .map(WebElement::getText)
                .findFirst()
                .orElse("");
        boolean valuesVisibleInAccount = pageText.contains(expectedAddress)
                && pageText.contains(expectedCity);

        boolean valuesVisibleInForm = driver.findElements(By.id("billing_address_1")).stream()
                .filter(WebElement::isDisplayed)
                .anyMatch(addressField -> expectedAddress.equals(addressField.getAttribute("value")))
                && driver.findElements(By.id("billing_city")).stream()
                .filter(WebElement::isDisplayed)
                .anyMatch(cityField -> expectedCity.equals(cityField.getAttribute("value"))
                        || expectedCity.equals(cityField.findElements(By.cssSelector("option:checked")).stream()
                        .map(WebElement::getText)
                        .findFirst()
                        .orElse("")));

        return valuesVisibleInAccount || valuesVisibleInForm || successMessageVisible;
    }
}
