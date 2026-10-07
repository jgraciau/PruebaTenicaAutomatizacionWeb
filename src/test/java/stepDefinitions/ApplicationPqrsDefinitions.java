package stepDefinitions;

import io.cucumber.java.Before;
import io.cucumber.java.PendingException;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import net.serenitybdd.screenplay.actions.Scroll;
import net.serenitybdd.screenplay.actors.OnStage;
import net.serenitybdd.screenplay.actors.OnlineCast;
import questions.PqrsRadicado;
import tasks.pqrs.OpenPqrsPage;
import tasks.pqrs.SubmitPqrsRequest;
import models.PqrsTestData;
import userInterfaces.PqrsHome;

import static net.serenitybdd.screenplay.GivenWhenThen.seeThat;
import static net.serenitybdd.screenplay.actors.OnStage.theActorCalled;
import static org.hamcrest.Matchers.not;
import static org.hamcrest.Matchers.isEmptyOrNullString;

public class ApplicationPqrsDefinitions {
    @Before
    public void setStage() {
        OnStage.setTheStage(new OnlineCast());
    }

    @Before("@PQRS")
    public void requireConfiguredPqrsTestData() {
        var missing = PqrsTestData.missingEnvironmentVariables();
        if (!missing.isEmpty()) {
            throw new PendingException(
                    "PQRS was not submitted: configure authorized test data variables "
                            + String.join(", ", missing)
            );
        }
    }

    @Given("el usuario esta en la pagina de PQRS")
    public void elUsuarioEstaEnLaPaginaDePQRS() {
        theActorCalled("Cliente").wasAbleTo(OpenPqrsPage.open());
    }

    @When("ingresa a la opcion crear solicitud PQRS")
    public void ingresaALaOpcionCrearSolicitudPQRS() {
        OnStage.theActorInTheSpotlight().attemptsTo(Scroll.to(PqrsHome.PUNTO_VENTA));
    }

    @And("diligencia el formulario con los datos requeridos")
    public void diligenciaElFormularioConLosDatosRequeridos() {
        OnStage.theActorInTheSpotlight().attemptsTo(SubmitPqrsRequest.withConfiguredTestData());
    }

    @Then("el sistema genera un mensaje de confirmacion con el numero de radicado")
    public void elSistemaGeneraUnMensajeDeConfirmacionConElNumeroDeRadicado() {
        OnStage.theActorInTheSpotlight().should(
                seeThat(PqrsRadicado.fromConfirmation(), not(isEmptyOrNullString()))
        );
    }
}
