package tasks.registerUser;

import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import net.thucydides.core.environment.SystemEnvironmentVariables;
import net.thucydides.core.util.EnvironmentVariables;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class OpenRegister implements Task {

        @Override
        public <T extends Actor> void performAs(T actor) {
            EnvironmentVariables environmentVariables = SystemEnvironmentVariables.createEnvironmentVariables();
            String baseUrl = net.serenitybdd.core.environment.EnvironmentSpecificConfiguration
                    .from(environmentVariables).getProperty("webdriver.base.url");
            String accountUrl = baseUrl.endsWith("/") ? baseUrl + "mi-cuenta/" : baseUrl + "/mi-cuenta/";
            WebDriver driver = BrowseTheWeb.as(actor).getDriver();
            driver.navigate().to(accountUrl);

            WebElement registerToggle = new WebDriverWait(driver, Duration.ofSeconds(20))
                    .withMessage("The registration form toggle did not load")
                    .until(currentDriver -> currentDriver.findElements(By.id("show_register")).stream()
                            .filter(WebElement::isDisplayed)
                            .findFirst()
                            .orElse(null));
            registerToggle.click();

            new WebDriverWait(driver, Duration.ofSeconds(20))
                    .withMessage("The registration form did not open")
                    .until(currentDriver -> currentDriver.findElements(By.id("reg_username")).stream()
                            .anyMatch(WebElement::isDisplayed));

        }

        public static OpenRegister openRegister() {
            return Tasks.instrumented(OpenRegister.class);
        }
    }
