package tasks;

import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;

public class UpdateBillingAddress implements Task {
    private final String address;
    private final String city;

    public UpdateBillingAddress(String address, String city) {
        this.address = address;
        this.city = city;
    }

    public static UpdateBillingAddress to(String address, String city) {
        return Tasks.instrumented(UpdateBillingAddress.class, address, city);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        actor.attemptsTo(
                OpenBillingAddressEditor.open(),
                FillBillingAddress.with(address, city)
        );
    }
}
