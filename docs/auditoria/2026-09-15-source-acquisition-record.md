# Auditoría — contrato de adquisición de fuente

## Objetivo

Establecer el siguiente límite reproducible después del contrato de ingestión raw: una adquisición debe conservar procedencia, identidad, longitud, hash SHA-256 y ausencia de transformaciones.

## Resultado

Se añadió `src/ingestion/acquisition_record.py` con validación determinista para:

- identificación de la fuente y número de inventario;
- URI HTTP(S) absoluta;
- marca temporal ISO-8601;
- longitud positiva en bytes;
- SHA-256 hexadecimal de 64 caracteres;
- método de adquisición;
- `transformations: []`;
- estado explícito `UNVERIFIED` o `VERIFIED`.

## Regla de integridad

`UNVERIFIED` es un estado válido de registro, pero no autoriza a tratar el contenido como fuente verificada. La implementación tampoco descarga, OCRiza, normaliza, translitera ni traduce contenido.

## Estado del corpus

El manifiesto canónico continúa en `PROVENANCE_READY_NOT_INGESTED`. La referencia `MAN_ANI / EA10470` permanece registrada como referencia primaria, sin afirmar que se haya adquirido o verificado contenido.

## Siguiente transición

1. localizar una URI primaria verificable para `EA10470`;
2. adquirir el archivo real sin transformación;
3. calcular SHA-256 y longitud;
4. registrar el acquisition record;
5. validar por CI;
6. sólo después habilitar normalización/transliteración con trazabilidad al artefacto raw.
