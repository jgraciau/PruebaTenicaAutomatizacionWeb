package userInterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public class CreateAccountHome {

    public static final Target INPUT_ID = Target.the("Ingreso la cedula del usuario")
            .located(By.id("reg_username"));

    public static final Target INPUT_FIRSTNAME = Target.the("Ingreso el nombre del usuario")
            .located(By.id("first_name"));

    public static final Target INPUT_LASTNAME = Target.the("Ingreso los apellidos del usuario")
            .located(By.id("last_name"));

    public static final Target INPUT_EMAIL = Target.the("Ingreso el correo del usuario")
            .located(By.id("reg_email"));

    public static final Target INPUT_PASSWORD = Target.the("Ingreso la  password del usuario")
            .located(By.id("reg_password"));

    public static final Target INPUT_PASSWORD2  = Target.the("Ingreso la confirmacion del usuario")
            .located(By.id("reg_password2"));

    public static final Target SELECT_AUTORIZATION  = Target.the("Seleccionar autorizar tratamiento")
            .located(By.id("privacy_policy_reg"));

    public static final Target BTTN_REGISTER  = Target.the("boton registrar")
            .located(By.name("register"));

}
