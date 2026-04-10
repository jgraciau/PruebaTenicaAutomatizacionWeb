package interactions;

import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.targets.Target;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.JavascriptExecutor;

public class ClickJs implements Task {

    private final Target target;

    public ClickJs(Target target) {
        this.target = target;
    }

    public static ClickJs en(Target target) {
        return new ClickJs(target);
    }

    @Override
    public <T extends Actor> void performAs(T actor) {
        JavascriptExecutor js = (JavascriptExecutor)
                BrowseTheWeb.as(actor).getDriver();

        // ✅ FIX
        js.executeScript("arguments[0].click();", target.resolveFor(actor));
    }
}
