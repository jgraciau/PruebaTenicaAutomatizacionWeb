package tasks.registerUser;

import interactions.ClickJs;
import net.serenitybdd.core.Serenity;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.actions.Enter;
import userInterfaces.CreateAccountHome;

import java.util.Map;

public class CreateAccount implements Task {
    @Override
    public <T extends Actor> void performAs(T actor) {

        Map<String, String> datosFila = Serenity.sessionVariableCalled("datoFila");

        String cedula = datosFila.get("Numero de cedula");
        String nombre = datosFila.get("Nombres");
        String apellido = datosFila.get("Apellidos");
        String correo = datosFila.get("Correo electronico");
        String pass = datosFila.get("Contraseña");
        String confirmaPass = datosFila.get("Confirmar contraseña");

        actor.attemptsTo(
                Enter.theValue(cedula).into(CreateAccountHome.INPUT_ID),
                Enter.theValue(nombre).into(CreateAccountHome.INPUT_FIRSTNAME),
                Enter.theValue(apellido).into(CreateAccountHome.INPUT_LASTNAME),
                Enter.theValue(correo).into(CreateAccountHome.INPUT_EMAIL),
                Enter.theValue(pass).into(CreateAccountHome.INPUT_PASSWORD),
                Enter.theValue(confirmaPass).into(CreateAccountHome.INPUT_PASSWORD2)
        );

        actor.attemptsTo(
                Click.on(CreateAccountHome.SELECT_AUTORIZATION)
        );

        actor.attemptsTo(
                ClickJs.en(CreateAccountHome.BTTN_REGISTER)
        );
    }

    public static CreateAccount createAccount() {
        return Tasks.instrumented(CreateAccount.class);
    }
}
