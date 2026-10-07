package userInterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public class PqrsHome {
    public static final Target PUNTO_VENTA = Target.the("punto de venta")
            .located(By.name("select-1"));
    public static final Target NOMBRE = Target.the("nombre completo del cliente")
            .located(By.name("name-1"));
    public static final Target DIRECCION = Target.the("dirección y ciudad")
            .located(By.name("address-1-street_address"));
    public static final Target TIPO_DOCUMENTO = Target.the("tipo de documento")
            .located(By.name("select-2"));
    public static final Target NUMERO_DOCUMENTO = Target.the("número de documento")
            .located(By.name("text-1"));
    public static final Target TELEFONO = Target.the("teléfono")
            .located(By.name("phone-1"));
    public static final Target CORREO = Target.the("correo electrónico")
            .located(By.name("email-1"));
    public static final Target TIPO_SOLICITUD = Target.the("tipo de solicitud")
            .located(By.name("select-3"));
    public static final Target CAUSAL = Target.the("causal de la solicitud")
            .located(By.name("select-4"));
    public static final Target DESCRIPCION = Target.the("descripción de la solicitud")
            .located(By.name("textarea-1"));
    public static final Target AUTORIZACION = Target.the("autorización de tratamiento de datos")
            .located(By.name("consent-1"));
    public static final Target ENVIAR = Target.the("crear PQRS")
            .locatedBy("#forminator-module-1000452 button[type='submit']");
    public static final Target MENSAJE_RESPUESTA = Target.the("mensaje de respuesta de PQRS")
            .locatedBy("#forminator-module-1000452 .forminator-response-message");
}
