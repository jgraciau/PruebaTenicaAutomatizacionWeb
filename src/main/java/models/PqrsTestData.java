package models;

import java.util.ArrayList;
import java.util.List;

public record PqrsTestData(
        String puntoVenta,
        String nombreCompleto,
        String direccion,
        String tipoDocumento,
        String numeroDocumento,
        String telefono,
        String correo,
        String tipoSolicitud,
        String descripcion,
        String causal
) {
    public static PqrsTestData fromEnvironment() {
        List<String> missing = new ArrayList<>();
        String puntoVenta = required("BONBONITE_PQRS_STORE", missing);
        String nombreCompleto = required("BONBONITE_PQRS_FULL_NAME", missing);
        String direccion = required("BONBONITE_PQRS_ADDRESS", missing);
        String tipoDocumento = required("BONBONITE_PQRS_DOCUMENT_TYPE", missing);
        String numeroDocumento = required("BONBONITE_PQRS_DOCUMENT_NUMBER", missing);
        String telefono = required("BONBONITE_PQRS_PHONE", missing);
        String correo = required("BONBONITE_PQRS_EMAIL", missing);
        String tipoSolicitud = required("BONBONITE_PQRS_REQUEST_TYPE", missing);
        String descripcion = required("BONBONITE_PQRS_DESCRIPTION", missing);
        String causal = System.getenv("BONBONITE_PQRS_CAUSE");

        if (!missing.isEmpty()) {
            throw new IllegalStateException(
                    "Missing required PQRS test environment variables: " + String.join(", ", missing)
            );
        }

        return new PqrsTestData(
                puntoVenta,
                nombreCompleto,
                direccion,
                tipoDocumento,
                numeroDocumento,
                telefono,
                correo,
                tipoSolicitud,
                descripcion,
                causal == null ? "" : causal.trim()
        );
    }

    public static List<String> missingEnvironmentVariables() {
        List<String> missing = new ArrayList<>();
        for (String variableName : List.of(
                "BONBONITE_PQRS_STORE",
                "BONBONITE_PQRS_FULL_NAME",
                "BONBONITE_PQRS_ADDRESS",
                "BONBONITE_PQRS_DOCUMENT_TYPE",
                "BONBONITE_PQRS_DOCUMENT_NUMBER",
                "BONBONITE_PQRS_PHONE",
                "BONBONITE_PQRS_EMAIL",
                "BONBONITE_PQRS_REQUEST_TYPE",
                "BONBONITE_PQRS_DESCRIPTION"
        )) {
            required(variableName, missing);
        }
        return List.copyOf(missing);
    }

    private static String required(String variableName, List<String> missing) {
        String value = System.getenv(variableName);
        if (value == null || value.isBlank()) {
            missing.add(variableName);
            return "";
        }
        return value.trim();
    }
}
