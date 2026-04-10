package utils;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.util.List;

public class MyChromeDriver {
    public  static WebDriver chromeDriver;

    public static  MyChromeDriver chromeBrowserWeb(){
        WebDriverManager.chromedriver().setup();
        ChromeOptions options = new ChromeOptions();

        options.setExperimentalOption("excludeSwitches", List.of("enable-logging"));
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--disable-gpu");
        options.addArguments("--start-maximized");
        options.addArguments("--ignore-certificate-errors");
        options.addArguments("--disable-infobars");
        options.addArguments("--remote-allow-origins=*");

        //creamos la instancia
        MyChromeDriver myChromeDriver = new MyChromeDriver();
        MyChromeDriver.chromeDriver = new ChromeDriver(options);

        return myChromeDriver;
    }

    public WebDriver onTheUrl(String url){
        chromeDriver.get(url);
        return chromeDriver;
    }
}
