package userInterfaces;


import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public class ResgisterPage {
    public static final Target BTTN_INICIO = Target.the("Ingreso al iniciar sesion")
            .located(By.xpath("(//a[contains(@href,'www.bon-bonite.com/mi-cuenta')])[3]"));

    public static final Target BTTN_REGISTRAR = Target.the("Ingreso al iniciar sesion")
            .located(By.id("show_register"));
}