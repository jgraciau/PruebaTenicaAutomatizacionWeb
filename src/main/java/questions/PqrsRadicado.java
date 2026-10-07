package questions;

import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Question;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;

import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class PqrsRadicado implements Question<String> {
    private static final Pattern RADICADO_PATTERN = Pattern.compile(
            "(?iu)(?:n[uú]mero\\s+de\\s+)?radicado\\s*(?:es\\s*)?[:#-]?\\s*([a-z0-9-]+)"
    );

    public static PqrsRadicado fromConfirmation() {
        return new PqrsRadicado();
    }

    @Override
    public String answeredBy(Actor actor) {
        List<WebElement> messages = BrowseTheWeb.as(actor).getDriver().findElements(
                By.cssSelector("#forminator-module-1000452 .forminator-response-message")
        );
        String message = messages.stream()
                .filter(WebElement::isDisplayed)
                .map(WebElement::getText)
                .filter(text -> !text.isBlank())
                .findFirst()
                .orElseThrow(() -> new AssertionError("The PQRS confirmation message was not displayed"));

        Matcher matcher = RADICADO_PATTERN.matcher(message);
        if (!matcher.find()) {
            throw new AssertionError("The PQRS response did not include a radicado number");
        }
        return matcher.group(1);
    }
}
