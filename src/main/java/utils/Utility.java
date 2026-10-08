package utils;


import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import net.serenitybdd.screenplay.targets.Target;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;

import java.io.InputStream;
import java.util.*;
import java.util.logging.Logger;

public class Utility {
    private static final Logger logger = Logger.getLogger(Utility.class.getName());
    public static List<Map<String, String>> readExcelTarifas(String resourcePath, String hoja) {
        List<Map<String, String>> datos = new ArrayList<>();

        try (InputStream fis = Utility.class.getResourceAsStream(resourcePath)) {
            if (fis == null) {
                logger.info("ERROR: No se encontró el archivo en classpath: " + resourcePath);
                return datos; // Lista vacía
            }

            try (Workbook workbook = new XSSFWorkbook(fis)) {
                Sheet sheet = workbook.getSheet(hoja);
                if (sheet == null) {
                    logger.info("ERROR: Hoja no encontrada: " + hoja);
                    return datos;
                }

                // OBTENER HEADER: Fila 4 (índice 3) → Columnas B y C (índices 1 y 2)
                Row headerRow = sheet.getRow(3);
                if (headerRow == null) {
                    logger.info("ERROR: Fila de encabezado (fila 4) no encontrada.");
                    return datos;
                }

                List<String> headers = new ArrayList<>();
                for (int i = 1; i <= 2; i++) { // B y C
                    Cell celdaHeader = headerRow.getCell(i, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK);
                    headers.add(obtenerValorCeldaSeguro(celdaHeader));
                }

                // LEER DATOS: desde fila 5 (índice 4) en adelante
                for (int i = 4; i <= sheet.getLastRowNum(); i++) {
                    Row row = sheet.getRow(i);
                    if (row == null) continue;

                    Map<String, String> fila = new HashMap<>();
                    for (int j = 1; j <= 2; j++) { // Solo B y C
                        Cell celda = row.getCell(j, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK);
                        fila.put(headers.get(j - 1), obtenerValorCeldaSeguro(celda));
                    }
                    datos.add(fila);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return datos;
    }

    public static ArrayList<Map<String, String>> readExcel(String resourcePath, String sheetName) {
        ArrayList<Map<String, String>> arrayListDatoPlanTrabajo = new ArrayList<>();

        // Usar classpath: resourcePath debe ser como "/src/test/resources/excel/..."
        try (InputStream inputStream = Utility.class.getResourceAsStream(resourcePath)) {
            if (inputStream == null) {
                throw new IllegalArgumentException("No se encontró el archivo Excel en classpath: " + resourcePath);
            }

            try (XSSFWorkbook newWorkbook = new XSSFWorkbook(inputStream)) {
                Sheet sheet = newWorkbook.getSheet(sheetName);
                if (sheet == null) {
                    throw new IllegalArgumentException("No se encontró la hoja Excel: " + sheetName);
                }

                Iterator<Row> rowIterator = sheet.iterator();
                if (!rowIterator.hasNext()) {
                    throw new IllegalArgumentException("El archivo Excel está vacío: " + resourcePath);
                }

                Row titulos = rowIterator.next(); // Primera fila = encabezados

                while (rowIterator.hasNext()) {
                    Row row = rowIterator.next();
                    Map<String, String> informacionProyecto = new HashMap<>();

                    // Iterar por celdas de la fila actual
                    for (int i = 0; i < titulos.getLastCellNum(); i++) {
                        Cell headerCell = titulos.getCell(i, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK);
                        Cell dataCell = row.getCell(i, Row.MissingCellPolicy.CREATE_NULL_AS_BLANK);

                        String key = getCellValueAsString(headerCell).trim();
                        String value = getCellValueAsString(dataCell).trim();

                        informacionProyecto.put(key, value);
                    }

                    arrayListDatoPlanTrabajo.add(informacionProyecto);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }

        return arrayListDatoPlanTrabajo;
    }

    private static String getCellValueAsString(Cell cell) {
        if (cell == null) return "";

        return switch (cell.getCellType()){
            case STRING -> cell.getStringCellValue();
            case NUMERIC -> {
                if (DateUtil.isCellDateFormatted(cell)) {
                    yield  cell.getDateCellValue().toString();
                }else {
                    double num = cell.getNumericCellValue();
                    if (num == (long) num){
                        yield String.valueOf((long) num);
                    }else  {
                        yield  String.valueOf(num);
                    }
                }
            }
            case BOOLEAN -> String.valueOf(cell.getBooleanCellValue());
            case FORMULA -> getCellValueAsString(cell.getCachedFormulaResultType());
            case BLANK, _NONE, ERROR -> "";
            default -> cell.toString();
        };

    }

    private static String getCellValueAsString(CellType formulaRusltType) {
        return switch (formulaRusltType){
            case STRING -> "FÓMULA_STRING";
            case NUMERIC -> "FÓMULA_NUM";
            case BOOLEAN -> "FóMULA_BOOL";
            default -> "";
        };
    }

    private static String obtenerValorCeldaSeguro(Cell celda) {
        if (celda == null) return "";
        switch (celda.getCellType()) {
            case STRING: return celda.getStringCellValue();
            case NUMERIC: return String.valueOf(celda.getNumericCellValue());
            default: return "";
        }
    }

    public  static void ScrollTo(Actor actor, Target target) {
        WebDriver driver = BrowseTheWeb.as(actor).getDriver();
        ((JavascriptExecutor) driver).executeScript(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", target.resolveFor(actor));
    }
}
