package tasks;

import interactions.ClickJs;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import net.serenitybdd.screenplay.actions.Enter;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import net.thucydides.core.environment.SystemEnvironmentVariables;
import net.thucydides.core.util.EnvironmentVariables;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import static userInterfaces.LoginBonBonitePage.*;


public class LoginBonBonite implements Task {
    @Override
    public <T extends Actor> void performAs(T actor) {

        String usuario = requiredCredential("BONBONITE_TEST_USER");
        String pass = requiredCredential("BONBONITE_TEST_PASSWORD");
        WebDriver driver = BrowseTheWeb.as(actor).getDriver();
        EnvironmentVariables environmentVariables = SystemEnvironmentVariables.createEnvironmentVariables();
        String baseUrl = net.serenitybdd.core.environment.EnvironmentSpecificConfiguration
                .from(environmentVariables).getProperty("webdriver.base.url");
        String accountUrl = baseUrl.endsWith("/") ? baseUrl + "mi-cuenta/" : baseUrl + "/mi-cuenta/";
        driver.navigate().to(accountUrl);

        if (driver.findElements(By.cssSelector("a[href*='customer-logout']")).stream()
                .anyMatch(WebElement::isDisplayed)) {
            return;
        }

        new WebDriverWait(driver, Duration.ofSeconds(20))
                .withMessage("The account login form did not load")
                .until(currentDriver -> currentDriver.findElements(By.id("username")).stream()
                        .anyMatch(WebElement::isDisplayed));

        actor.attemptsTo(
                Enter.theValue(usuario).into(INPUT_USER),
                Enter.theValue(pass).into(INPUT_PASS)
        );

        actor.attemptsTo(
                ClickJs.en(BTTN_LOGIN)
        );

        Boolean loggedIn = new WebDriverWait(driver, Duration.ofSeconds(20))
                .withMessage("Login did not reach an authenticated account state")
                .until(currentDriver -> {
                    boolean logoutVisible = currentDriver.findElements(
                                    By.cssSelector("a[href*='customer-logout']"))
                            .stream()
                            .anyMatch(WebElement::isDisplayed);
                    if (logoutVisible) {
                        return true;
                    }

                    boolean errorVisible = currentDriver.findElements(
                                    By.cssSelector(".woocommerce-error, .woocommerce-notices-wrapper .woocommerce-error"))
                            .stream()
                            .anyMatch(WebElement::isDisplayed);
                    return errorVisible ? false : null;
                });
        if (!loggedIn) {
            throw new IllegalStateException("The site rejected the configured test account");
        }
    }

    private String requiredCredential(String environmentVariable) {
        String value = System.getenv(environmentVariable);
        if (value == null || value.isBlank()) {
            throw new IllegalStateException("Configure " + environmentVariable + " with an authorized test account");
        }
        return value.trim();
    }

    public static LoginBonBonite loginBonBonite() {
        return Tasks.instrumented(LoginBonBonite.class);
    }
}
