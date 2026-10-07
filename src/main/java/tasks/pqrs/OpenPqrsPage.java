package tasks.pqrs;

import net.serenitybdd.core.environment.EnvironmentSpecificConfiguration;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import net.thucydides.core.environment.SystemEnvironmentVariables;
import net.thucydides.core.util.EnvironmentVariables;

public class OpenPqrsPage implements Task {
    public static OpenPqrsPage open() {
        return Tasks.instrumented(OpenPqrsPage.class);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        EnvironmentVariables environmentVariables = SystemEnvironmentVariables.createEnvironmentVariables();
        String baseUrl = EnvironmentSpecificConfiguration.from(environmentVariables)
                .getProperty("webdriver.base.url");
        if (baseUrl == null || baseUrl.isBlank()) {
            throw new IllegalStateException("The webdriver.base.url property must be configured");
        }

        String pqrsUrl = baseUrl.endsWith("/") ? baseUrl + "pqrs/" : baseUrl + "/pqrs/";
        BrowseTheWeb.as(actor).getDriver().navigate().to(pqrsUrl);
    }
}
