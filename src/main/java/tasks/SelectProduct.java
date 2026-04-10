package tasks;

import interactions.ClickJs;
import net.serenitybdd.core.Serenity;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import net.serenitybdd.screenplay.actions.Scroll;
import net.serenitybdd.screenplay.actions.ScrollTo;
import utils.Utility;

import java.util.Map;

import static userInterfaces.ProductHome.*;

public class SelectProduct implements Task {

    public static SelectProduct selectProduct() {
       return Tasks.instrumented(SelectProduct.class);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {

        Map<String, String> datosFila = Serenity.sessionVariableCalled("datoFila");

        String producto = datosFila.get("Nombre Producto");
        String talla = datosFila.get("Talla");

        actor.attemptsTo(ClickJs.en(PRODUCTO_LINK.of(producto)));

        if (talla != null && !talla.trim().isBlank()) {

            Utility.ScrollTo(actor,TALLA.of(talla));
            actor.attemptsTo(
                    ClickJs.en(TALLA.of(talla))
            );
        }

    }
}
