package tasks.pqrs;

import models.PqrsTestData;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.actions.Enter;
import net.serenitybdd.screenplay.actions.SelectFromOptions;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import userInterfaces.PqrsHome;

import java.time.Duration;
import java.util.List;

public class SubmitPqrsRequest implements Task {
    private static final Logger LOGGER = LoggerFactory.getLogger(SubmitPqrsRequest.class);

    public static SubmitPqrsRequest withConfiguredTestData() {
        return Tasks.instrumented(SubmitPqrsRequest.class);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        PqrsTestData data = PqrsTestData.fromEnvironment();

        actor.attemptsTo(
                SelectFromOptions.byVisibleText(data.puntoVenta()).from(PqrsHome.PUNTO_VENTA),
                Enter.theValue(data.nombreCompleto()).into(PqrsHome.NOMBRE),
                Enter.theValue(data.direccion()).into(PqrsHome.DIRECCION),
                SelectFromOptions.byValue(data.tipoDocumento()).from(PqrsHome.TIPO_DOCUMENTO),
                Enter.theValue(data.numeroDocumento()).into(PqrsHome.NUMERO_DOCUMENTO),
                Enter.theValue(data.telefono()).into(PqrsHome.TELEFONO),
                Enter.theValue(data.correo()).into(PqrsHome.CORREO),
                SelectFromOptions.byVisibleText(data.tipoSolicitud()).from(PqrsHome.TIPO_SOLICITUD),
                Enter.theValue(data.descripcion()).into(PqrsHome.DESCRIPCION)
        );

        fillCausalWhenRequired(actor, data.causal());
        actor.attemptsTo(Click.on(PqrsHome.AUTORIZACION));

        WebDriver driver = BrowseTheWeb.as(actor).getDriver();
        awaitManualCaptcha(driver);
        actor.attemptsTo(Click.on(PqrsHome.ENVIAR));
        awaitResponseMessage(driver);
    }

    private void fillCausalWhenRequired(Actor actor, String causal) {
        WebElement field = BrowseTheWeb.as(actor).getDriver().findElement(By.name("select-4"));
        if (!field.isDisplayed()) {
            return;
        }
        if (causal.isBlank()) {
            throw new IllegalStateException(
                    "BONBONITE_PQRS_CAUSE is required for the selected PQRS request type"
            );
        }
        actor.attemptsTo(SelectFromOptions.byVisibleText(causal).from(PqrsHome.CAUSAL));
    }

    private void awaitManualCaptcha(WebDriver driver) {
        LOGGER.info("Solve the reCAPTCHA challenge in the browser to continue the PQRS test");
        new WebDriverWait(driver, Duration.ofMinutes(5))
                .withMessage("Timed out waiting for the user to solve the PQRS reCAPTCHA challenge")
                .until(currentDriver -> {
                    List<WebElement> responses = currentDriver.findElements(By.name("g-recaptcha-response"));
                    return !responses.isEmpty()
                            && responses.stream().anyMatch(element -> {
                                String value = element.getAttribute("value");
                                return value != null && !value.isBlank();
                            });
                });
    }

    private void awaitResponseMessage(WebDriver driver) {
        new WebDriverWait(driver, Duration.ofSeconds(60))
                .withMessage("The PQRS form did not display a response after submission")
                .until(currentDriver -> {
                    List<WebElement> messages = currentDriver.findElements(
                            By.cssSelector("#forminator-module-1000452 .forminator-response-message")
                    );
                    return messages.stream().anyMatch(
                            message -> message.isDisplayed() && !message.getText().isBlank()
                    );
                });
    }
}
