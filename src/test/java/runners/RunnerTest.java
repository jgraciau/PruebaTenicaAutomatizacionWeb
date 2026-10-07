package runners;

import io.cucumber.junit.CucumberOptions;
import net.serenitybdd.cucumber.CucumberWithSerenity;
import org.junit.runner.RunWith;

@RunWith(CucumberWithSerenity.class)
@CucumberOptions(
        plugin = {"pretty", "json:target/cucumber-json-report.json"},
        features = "src/test/resources/features",
        glue = "stepDefinitions",
        snippets = CucumberOptions.SnippetType.CAMELCASE
)
public class RunnerTest {
}
