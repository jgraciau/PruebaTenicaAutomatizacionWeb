package userInterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public class LoginBonBonitePage {

    public static final Target INPUT_USER = Target.the("Ingreso el usuario")
            .located(By.id("username"));

    public static final Target INPUT_PASS = Target.the("Ingreso la contraseña")
            .located(By.id("password"));

    public static final Target BTTN_LOGIN = Target.the("Iniciar sesion")
            .located(By.name("login"));
}