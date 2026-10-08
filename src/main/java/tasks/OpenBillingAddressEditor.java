package tasks;

import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Tasks;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.actions.Scroll;
import net.serenitybdd.screenplay.waits.WaitUntil;

import java.time.Duration;

import static net.serenitybdd.screenplay.matchers.WebElementStateMatchers.isVisible;
import static userInterfaces.BillingAddressPage.BILLING_SECTION;
import static userInterfaces.BillingAddressPage.DATA_LINK;
import static userInterfaces.BillingAddressPage.EDIT_BILLING_ADDRESS;
import static userInterfaces.BillingAddressPage.ADDRESS_MODAL;

public class OpenBillingAddressEditor implements Task {
    public static OpenBillingAddressEditor open() {
        return Tasks.instrumented(OpenBillingAddressEditor.class);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        actor.attemptsTo(
                WaitUntil.the(DATA_LINK, isVisible()).forNoMoreThan(Duration.ofSeconds(20)),
                Click.on(DATA_LINK),
                WaitUntil.the(BILLING_SECTION, isVisible()).forNoMoreThan(Duration.ofSeconds(20)),
                Scroll.to(BILLING_SECTION),
                WaitUntil.the(EDIT_BILLING_ADDRESS, isVisible()).forNoMoreThan(Duration.ofSeconds(20)),
                Click.on(EDIT_BILLING_ADDRESS),
                WaitUntil.the(ADDRESS_MODAL, isVisible()).forNoMoreThan(Duration.ofSeconds(20))
        );
    }
}
