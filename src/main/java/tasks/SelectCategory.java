package tasks;

import interactions.ClickJs;
import net.serenitybdd.core.Serenity;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;

import java.util.Map;

import static userInterfaces.ProductHome.*;

public class SelectCategory implements Task {

    private final String opcion;

    public SelectCategory(String opcion) {
        this.opcion = opcion;
    }

    public static SelectCategory selectProduct(String opcion) {
        return Tasks.instrumented(SelectCategory.class, opcion);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {

        Map<String, String> datosFila = Serenity.sessionVariableCalled("datoFila");

        String categoria = datosFila.get("Nombre Categoria");

        switch (opcion) {
            case "zapatos", "bolsos", "cinturones", "accesorios", "outlet":
                actor.attemptsTo(ClickJs.en(CATEGORIA.of(categoria)));
                break;

            default:
                throw new IllegalArgumentException("No se encontro el producto");
        }
    }
}