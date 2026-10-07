package tasks;

import net.serenitybdd.core.Serenity;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;
import java.util.Map;

import static userInterfaces.ProductHome.*;

public class SelectProduct implements Task {

    public static SelectProduct selectProduct() {
       return Tasks.instrumented(SelectProduct.class);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {

        Map<String, String> datosFila = Serenity.sessionVariableCalled("datoFila");

        String producto = datosFila.get("Nombre Producto");
        String talla = datosFila.get("Talla");

        WebDriver driver = BrowseTheWeb.as(actor).getDriver();
        WebElement productLink = new WebDriverWait(driver, Duration.ofSeconds(20))
                .withMessage("Product is not listed or available: " + producto)
                .until(currentDriver -> {
                    var links = currentDriver.findElements(
                            By.xpath("//h4[normalize-space()='" + producto
                                    + "']/ancestor::div[contains(@class,'group')][1]"
                                    + "//a[contains(@href,'/producto/')]")
                    );
                    return links.stream().filter(WebElement::isDisplayed).findFirst().orElse(null);
                });
        productLink.click();

        if (talla != null && !talla.trim().isBlank()) {
            WebElement sizeOption = new WebDriverWait(driver, Duration.ofSeconds(20))
                    .withMessage("Requested size " + talla + " is unavailable for product " + producto)
                    .until(currentDriver -> {
                        var sizes = currentDriver.findElements(By.xpath(
                                "//button[@data-attribute_name='attribute_pa_talla' and @data-value='"
                                        + talla + "']"
                        ));
                        return sizes.stream()
                                .filter(WebElement::isDisplayed)
                                .filter(WebElement::isEnabled)
                                .findFirst()
                                .orElse(null);
                    });
            ((org.openqa.selenium.JavascriptExecutor) driver)
                    .executeScript("arguments[0].scrollIntoView({block:'center'});", sizeOption);
            sizeOption.click();
        }

    }
}
