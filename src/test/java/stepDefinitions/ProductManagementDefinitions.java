package stepDefinitions;

import io.cucumber.java.Before;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import net.serenitybdd.screenplay.actors.OnStage;
import net.serenitybdd.screenplay.actors.OnlineCast;
import questions.ObtenerResumenOrden;
import tasks.LoginBonBonite;
import tasks.PurchaseProcessProduct;
import tasks.SelectCategory;
import tasks.SelectProduct;

import static net.serenitybdd.screenplay.GivenWhenThen.seeThat;
import static org.hamcrest.Matchers.*;;


public class ProductManagementDefinitions {

    @Before
    public void setStage() {
        OnStage.setTheStage(new OnlineCast());
    }
    @And("inicia sesion con su usuario")
    public void iniciaSesionConSuUsuario() {
        OnStage.theActorInTheSpotlight().attemptsTo(
                LoginBonBonite.loginBonBonite()
        );

    }
    @And("busca la categoria de {string}")
    public void buscaLaCategoriaDe(String opcion) {
        OnStage.theActorInTheSpotlight().attemptsTo(
                SelectCategory.selectProduct(opcion)
        );
    }
    @When("selecciona un producto disponible")
    public void seleccionaUnProductoDisponible() {
        OnStage.theActorInTheSpotlight().attemptsTo(
                SelectProduct.selectProduct()
        );
    }
    @And("realizamos el proceso de compra")
    public void realizamosElProcesoDeCompra() {
        OnStage.theActorInTheSpotlight().attemptsTo(
                PurchaseProcessProduct.purchaseProcessProduct()
        );
    }

    @Then("el sistema genera mensaje de confirmacion de compra con el numero de pedido")
    public void elSistemaGeneraMensajeDeConfirmacionDeCompraConElNumeroDePedido() {
        OnStage.theActorInTheSpotlight().should(
                seeThat(
                        "Número de pedido",
                        actor -> actor.asksFor(ObtenerResumenOrden.deLaCompra()).getNumero(),
                        not(isEmptyOrNullString())

                )
        );
    }
}
