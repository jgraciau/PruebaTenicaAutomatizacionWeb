package questions;

import models.Orden;
import net.serenitybdd.screenplay.Question;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.questions.Text;

import static jxl.biff.FormatRecord.logger;
import static userInterfaces.ProductHome.*;

public class ObtenerResumenOrden implements Question<Orden> {

    public static ObtenerResumenOrden deLaCompra() {
        return new ObtenerResumenOrden();
    }

    @Override
    public Orden answeredBy(Actor actor) {

        // 🔥 Validación clave: estás en la página correcta
        String titulo = Text.of(TITULO_CHECKOUT).answeredBy(actor);

        if (!titulo.equalsIgnoreCase("Finalizar compra")) {
            throw new AssertionError("No estás en la página de checkout");
        }

        String numero = Text.of(NUMERO_PEDIDO).answeredBy(actor).trim();
        String fecha = Text.of(FECHA_PEDIDO).answeredBy(actor).trim();
        String total = Text.of(TOTAL_PEDIDO).answeredBy(actor).trim();
        String metodo = Text.of(METODO_PAGO).answeredBy(actor).trim();

        logger.info("======================Datos del Pedido===========================");
        logger.info("Número de pedido: " + numero);
        logger.info("Fecha: " + fecha);
        logger.info("Total: " + total);
        logger.info("Método de pago: " + metodo);

        return new Orden(numero, fecha, total, metodo);
    }
}
