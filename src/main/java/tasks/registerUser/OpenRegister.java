package tasks.registerUser;

import interactions.ClickJs;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.actions.Scroll;
import net.serenitybdd.screenplay.actions.WebElementLocator;
import org.openqa.selenium.WebElement;

import static userInterfaces.ResgisterPage.*;

public class OpenRegister implements Task {

        @Override
        public <T extends Actor> void performAs(T actor) {

            actor.attemptsTo(
                    ClickJs.en(BTTN_INICIO)
            );

            actor.attemptsTo(
                    ClickJs.en(BTTN_REGISTRAR)
            );

        }

        public static OpenRegister openRegister() {
            return Tasks.instrumented(OpenRegister.class);
        }
    }
