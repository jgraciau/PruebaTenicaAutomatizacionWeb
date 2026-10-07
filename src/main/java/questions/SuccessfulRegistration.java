package questions;

import net.serenitybdd.core.Serenity;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Question;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;

public class SuccessfulRegistration implements Question<Boolean> {
    private static final String ACCOUNT_CONTENT = ".woocommerce-MyAccount-content";
    private static final String REGISTRATION_ERRORS = ".woocommerce-error, .woocommerce-notices-wrapper .woocommerce-error";
    private static final String ACCOUNT_LOGOUT = "a[href*='customer-logout']";

    public static SuccessfulRegistration isConfirmed() {
        return new SuccessfulRegistration();
    }

    @Override
    public Boolean answeredBy(Actor actor) {
        var driver = BrowseTheWeb.as(actor).getDriver();

        try {
            return new WebDriverWait(driver, Duration.ofSeconds(15))
                    .until(currentDriver -> {
                        boolean registrationError = currentDriver.findElements(
                                        By.cssSelector(REGISTRATION_ERRORS))
                                .stream()
                                .anyMatch(WebElement::isDisplayed);
                        if (registrationError) {
                            return false;
                        }

                        boolean accountPageVisible = currentDriver.findElements(
                                        By.cssSelector(ACCOUNT_CONTENT))
                                .stream()
                                .anyMatch(WebElement::isDisplayed);
                        boolean loggedIn = currentDriver.findElements(
                                        By.cssSelector(ACCOUNT_LOGOUT))
                                .stream()
                                .anyMatch(WebElement::isDisplayed);
                        return accountPageVisible && loggedIn ? true : null;
                    });
        } catch (org.openqa.selenium.TimeoutException timeoutException) {
            return false;
        }
    }
}
