# Auditoría — Raw Acquisition Gate

Fecha: 2026-09-15

## Objetivo

Impedir que un artefacto sea aceptado como fuente primaria raw si su identidad no está verificada o si su longitud/hash no coinciden con los bytes suministrados.

## Controles

- El contenido debe ser `bytes` no vacío.
- El registro debe cumplir el contrato de adquisición existente.
- `verification_status` debe ser `VERIFIED`.
- `content_length_bytes` debe coincidir exactamente con `len(content)`.
- `sha256` debe coincidir con SHA-256 de los bytes suministrados.
- `transformations` debe permanecer como `[]`.

## Límite

Este gate no demuestra autenticidad histórica por sí mismo. Sólo demuestra consistencia entre una identidad previamente verificada, su registro de adquisición y los bytes entregados al validador.

## Estado

`READY_FOR_CI`
