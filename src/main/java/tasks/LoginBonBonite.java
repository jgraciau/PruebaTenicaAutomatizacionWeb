package tasks;

import interactions.ClickJs;
import net.serenitybdd.core.Serenity;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import net.serenitybdd.screenplay.actions.Enter;

import java.util.Map;

import static userInterfaces.LoginBonBonitePage.*;
import static userInterfaces.ResgisterPage.*;


public class LoginBonBonite implements Task {
    @Override
    public <T extends Actor> void performAs(T actor) {

        Map<String, String> datosFila = Serenity.sessionVariableCalled("datoFila");

        String usuario = datosFila.get("Usuario");
        String pass = datosFila.get("Contraseña");

        actor.attemptsTo(
                ClickJs.en(BTTN_INICIO)
        );

        actor.attemptsTo(
                Enter.theValue(usuario).into(INPUT_USER),
                Enter.theValue(pass).into(INPUT_PASS)
        );

        actor.attemptsTo(
                ClickJs.en(BTTN_LOGIN)
        );

    }

    public static LoginBonBonite loginBonBonite() {
        return Tasks.instrumented(LoginBonBonite.class);
    }
}
