package questions;

import net.serenitybdd.core.Serenity;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Question;
import net.serenitybdd.screenplay.targets.Target;
import userInterfaces.CreateAccountHome;

import java.util.Map;

public class SuccessfulRegistration implements Question<Boolean> {

    public static SuccessfulRegistration isConfirmed() {
        return new SuccessfulRegistration();
    }

    @Override
    public Boolean answeredBy(Actor actor) {

        Map<String, String> datosFila = Serenity.sessionVariableCalled("datoFila");
        String nombre = datosFila.get("Nombres");

        String text = CreateAccountHome.WELCOMEMESSAGE.resolveFor(actor).getText()
                .replace(" ", "")
                .replace(".", "")
                .toLowerCase();

        String expected = ("Hola," + nombre)
                .replace(" ", "")
                .replace(".", "")
                .toLowerCase();

        return text.contains(expected);
    }
}
