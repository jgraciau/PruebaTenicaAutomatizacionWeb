package userInterfaces;


import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public class ResgisterPage {
    public static final Target BTTN_INICIO = Target.the("Ingreso al iniciar sesion")
            .located(By.cssSelector("a[href*='/mi-cuenta']"));

    public static final Target BTTN_REGISTRAR = Target.the("Ingreso al iniciar sesion")
            .located(By.id("show_register"));
}