package models;

public class Orden {

    private final String numero;
    private final String fecha;
    private final String total;
    private final String metodoPago;

    public Orden(String numero, String fecha, String total, String metodoPago) {
        this.numero = numero;
        this.fecha = fecha;
        this.total = total;
        this.metodoPago = metodoPago;
    }

    public String getNumero() { return numero; }
    public String getFecha() { return fecha; }
    public String getTotal() { return total; }
    public String getMetodoPago() { return metodoPago; }
}
