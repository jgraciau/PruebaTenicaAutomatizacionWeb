package stepDefinitions;

import io.cucumber.java.Before;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import net.serenitybdd.screenplay.actors.OnStage;
import net.serenitybdd.screenplay.actors.OnlineCast;
import questions.BillingAddressWasUpdated;
import tasks.UpdateBillingAddress;

import static net.serenitybdd.screenplay.GivenWhenThen.seeThat;
import static org.hamcrest.Matchers.is;

public class BillingAddressDefinitions {

    @Before
    public void setStage() {
        OnStage.setTheStage(new OnlineCast());
    }

    @When("actualiza su direccion de facturacion a {string} y ciudad {string}")
    public void actualizaSuDireccionDeFacturacion(String address, String city) {
        OnStage.theActorInTheSpotlight().attemptsTo(
                UpdateBillingAddress.to(address, city)
        );
    }

    @Then("debe confirmar que la direccion de facturacion quedo guardada como {string} en la ciudad {string}")
    public void debeConfirmarDireccionDeFacturacion(String address, String city) {
        OnStage.theActorInTheSpotlight().should(
                seeThat(BillingAddressWasUpdated.to(address, city), is(true))
        );
    }
}
