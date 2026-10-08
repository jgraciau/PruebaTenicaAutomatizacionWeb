package tasks;

import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import net.serenitybdd.screenplay.actions.Clear;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.actions.Enter;
import net.serenitybdd.screenplay.actions.SelectFromOptions;
import net.serenitybdd.screenplay.waits.WaitUntil;

import java.time.Duration;

import static net.serenitybdd.screenplay.matchers.WebElementStateMatchers.isVisible;
import static userInterfaces.BillingAddressPage.ADDRESS;
import static userInterfaces.BillingAddressPage.CITY;
import static userInterfaces.BillingAddressPage.SAVE_ADDRESS;
import static userInterfaces.BillingAddressPage.SUCCESS_MESSAGE;

public class FillBillingAddress implements Task {
    private final String address;
    private final String city;

    public FillBillingAddress(String address, String city) {
        this.address = address;
        this.city = city;
    }

    public static FillBillingAddress with(String address, String city) {
        return Tasks.instrumented(FillBillingAddress.class, address, city);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        if (address == null || address.isBlank() || city == null || city.isBlank()) {
            throw new IllegalArgumentException("La dirección y la ciudad de facturación son obligatorias");
        }
        actor.attemptsTo(
                WaitUntil.the(ADDRESS, isVisible()).forNoMoreThan(Duration.ofSeconds(20)),
                Clear.field(ADDRESS),
                Enter.theValue(address).into(ADDRESS),
                SelectFromOptions.byVisibleText(city).from(CITY),
                Click.on(SAVE_ADDRESS),
                WaitUntil.the(SUCCESS_MESSAGE, isVisible()).forNoMoreThan(Duration.ofSeconds(20))
        );
    }
}
