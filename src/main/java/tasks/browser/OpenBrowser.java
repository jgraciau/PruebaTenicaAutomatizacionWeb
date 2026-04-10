package tasks.browser;

import net.serenitybdd.core.environment.EnvironmentSpecificConfiguration;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import net.thucydides.core.environment.SystemEnvironmentVariables;
import net.thucydides.core.util.EnvironmentVariables;
import utils.MyChromeDriver;

import static jxl.biff.FormatRecord.logger;
import static net.serenitybdd.screenplay.actors.OnStage.theActorInTheSpotlight;

public class OpenBrowser implements Task {

    public static OpenBrowser openBrowser(){
        return Tasks.instrumented(OpenBrowser.class);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        EnvironmentVariables environmentVariables = SystemEnvironmentVariables.createEnvironmentVariables();

        //Obtener la url
        String ambienteEjecucion = EnvironmentSpecificConfiguration.from(environmentVariables)
                .getProperty("webdriver.base.url");
        theActorInTheSpotlight().can(BrowseTheWeb.with(MyChromeDriver.chromeBrowserWeb().onTheUrl(ambienteEjecucion)));
        logger.info("Url ambiente QA: " + ambienteEjecucion);
    }
}
