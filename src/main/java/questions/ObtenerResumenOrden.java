package questions;

import models.Orden;
import net.serenitybdd.screenplay.Question;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;
import static jxl.biff.FormatRecord.logger;
import static userInterfaces.ProductHome.*;

public class ObtenerResumenOrden implements Question<Orden> {

    public static ObtenerResumenOrden deLaCompra() {
        return new ObtenerResumenOrden();
    }

    @Override
    public Orden answeredBy(Actor actor) {
        var driver = BrowseTheWeb.as(actor).getDriver();
        String numero = new WebDriverWait(driver, Duration.ofSeconds(60))
                .withMessage("No se confirmó la orden después de enviarla")
                .until(currentDriver -> {
                    List<WebElement> orderNumbers = currentDriver.findElements(
                            By.cssSelector(".woocommerce-order-overview__order strong")
                    );
                    if (orderNumbers.isEmpty()) {
                        orderNumbers = currentDriver.findElements(By.xpath("//li[contains(@class,'order')]//strong"));
                    }
                    return orderNumbers.stream()
                            .filter(WebElement::isDisplayed)
                            .map(WebElement::getText)
                            .map(String::trim)
                            .filter(value -> !value.isEmpty())
                            .findFirst()
                            .orElse(null);
                });
        String fecha = readOrderDetail(driver, ".woocommerce-order-overview__date strong",
                "//li[contains(@class,'date')]//strong");
        String total = readOrderDetail(driver, ".woocommerce-order-overview__total strong",
                "//li[contains(@class,'total')]//strong");
        String metodo = readOrderDetail(driver, ".woocommerce-order-overview__payment-method strong",
                "//li[contains(@class,'method')]//strong");

        logger.info("======================Datos del Pedido===========================");
        logger.info("Número de pedido: " + numero);
        logger.info("Fecha: " + fecha);
        logger.info("Total: " + total);
        logger.info("Método de pago: " + metodo);

        return new Orden(numero, fecha, total, metodo);
    }

    private String readOrderDetail(org.openqa.selenium.WebDriver driver, String cssSelector, String xpath) {
        List<WebElement> elements = driver.findElements(By.cssSelector(cssSelector));
        if (elements.isEmpty()) {
            elements = driver.findElements(By.xpath(xpath));
        }
        return elements.stream()
                .filter(WebElement::isDisplayed)
                .map(WebElement::getText)
                .map(String::trim)
                .findFirst()
                .orElse("");
    }
}
