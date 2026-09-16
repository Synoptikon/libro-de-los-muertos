# Source Verification Gate — 2026-09-15

## Objetivo

Impedir que una URI sea tratada por sí sola como prueba de identidad o procedencia de una fuente primaria.

## Contrato

El gate exige coincidencia exacta entre la identidad registrada y la identidad observada por un adaptador de descubrimiento:

- `source_id`
- `repository`
- `inventory_number`
- `source_uri`
- `identified_source_id`
- `identified_inventory_number`
- `verification_method`

Una coincidencia positiva produce `verification_status=VERIFIED`.

## Límite

El gate no descarga contenido, no calcula hashes y no afirma autenticidad material del objeto. Esos controles pertenecen a adquisición e integridad posteriores.

## Regla de transición

`REGISTERED_REFERENCE -> VERIFIED_IDENTITY -> ACQUISITION`

Una referencia que no tenga identidad coincidente permanece fuera del corpus adquirido.
