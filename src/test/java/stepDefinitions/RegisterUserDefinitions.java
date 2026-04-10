package stepDefinitions;

import io.cucumber.datatable.DataTable;
import io.cucumber.java.Before;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import net.serenitybdd.core.Serenity;
import net.serenitybdd.screenplay.actors.OnStage;
import net.serenitybdd.screenplay.actors.OnlineCast;
import questions.SuccessfulRegistration;
import tasks.browser.OpenBrowser;
import tasks.registerUser.CreateAccount;
import tasks.registerUser.OpenRegister;
import utils.Utility;

import java.util.List;
import java.util.Map;

import static jxl.biff.FormatRecord.logger;
import static net.serenitybdd.screenplay.GivenWhenThen.seeThat;
import static net.serenitybdd.screenplay.actors.OnStage.theActorCalled;

public class RegisterUserDefinitions {

    @Before
    public void setStage() {
        OnStage.setTheStage(new OnlineCast());
    }

    @Given("^el usuario carga la informacion desde el Excel \"([^\"]*)\"$")
    public void elUsuarioCargaLaInformacionDesdeElExcel(String fila, DataTable dataTable) {
        List<Map<String, String>> data = dataTable.asMaps(String.class, String.class);
        String rutaExcel = data.get(0).get("rutaExcel");
        String hoja = data.get(0).get("hoja");

        int numeroFila = Integer.parseInt(fila);

        if (rutaExcel.startsWith("src/test/resources")) {
            rutaExcel = rutaExcel.substring("src/test/resources".length());
        }
        rutaExcel = rutaExcel.replace("\\", "/");
        if (!rutaExcel.startsWith("/")){
            rutaExcel = "/" + rutaExcel;
        }

        Serenity.setSessionVariable("rutaExcel").to(rutaExcel);
        Serenity.setSessionVariable("hoja").to(hoja);
        Serenity.setSessionVariable("numeroFila").to(numeroFila);

        List<Map<String, String>> lecturaExcel;
        if (rutaExcel.contains("prueba.xlsx")) {
            lecturaExcel = Utility.readExcelTarifas(rutaExcel, hoja);
        }else{
            lecturaExcel = Utility.readExcel(rutaExcel, hoja);
        }

        //Validamos fila
        if (numeroFila < 1 || numeroFila > lecturaExcel.size()) {
            throw new IllegalStateException("La fila especifica no existe en el archivo Excel");
        }

        Map<String, String> datoFila = lecturaExcel.get(numeroFila - 1);
        Serenity.setSessionVariable("datoFila").to(datoFila);


        String ambiente = datoFila.getOrDefault("ambiente", "QA").trim();
        Serenity.setSessionVariable("ambiente").to(ambiente);
        logger.info("Ambiente capturado desde el Excel: " + ambiente);
    }

    @And("el usuario esta en la pagina de bonBonite")
    public void elUsuarioEstaEnLaPaginaDeBonBonite() {
        theActorCalled("Jhon").wasAbleTo(
                OpenBrowser.openBrowser()
        );
    }

    @When("ingresa al formulario de registro")
    public void ingresaAlFormularioDeRegistro() {
        OnStage.theActorInTheSpotlight().attemptsTo(
                OpenRegister.openRegister()
        );
    }

    @And("ingresa sus datos correctamente")
    public void ingresaSusDatosCorrectamente() {
        OnStage.theActorInTheSpotlight().attemptsTo(
                CreateAccount.createAccount()
        );
    }

    @Then("deberia ver confirmacion de registro exitoso")
    public void deberiaVerConfirmacionDeRegistroExitoso() {
       OnStage.theActorInTheSpotlight().should(
                seeThat(SuccessfulRegistration.isConfirmed())
        );
    }
}
