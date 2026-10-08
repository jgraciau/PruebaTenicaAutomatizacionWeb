package tasks;

import interactions.ClickJs;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import utils.Utility;

import static userInterfaces.ProductHome.*;

public class PurchaseProcessProduct implements Task {

    public static PurchaseProcessProduct purchaseProcessProduct() {
        return Tasks.instrumented(PurchaseProcessProduct.class);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {

        actor.attemptsTo(ClickJs.en(BOTON_COMPRAR_AHORA_URL));
        Utility.ScrollTo(actor,BOTON_FINALIZAR_COMPRA);
        actor.attemptsTo(ClickJs.en(BOTON_FINALIZAR_COMPRA));
        Utility.ScrollTo(actor,BOTON_CONTINUAR);
        actor.attemptsTo(ClickJs.en(BOTON_CONTINUAR));

        actor.attemptsTo(ClickJs.en(CHECKBOX_TERMINOS));
        actor.attemptsTo(ClickJs.en(BOTON_REALIZAR_PEDIDO));
    }
}
