# Auditoría — 2026-09-15

## Estado observado

- Rama principal: `main`.
- Commit certificado observado antes de este cambio: `a9008e29ea63e100c2c922c29bc862cfed2b17be`.
- El manifiesto canónico existe en `corpus/manifest.json`.
- El estado del corpus es `PROVENANCE_READY_NOT_INGESTED`.
- La fuente primaria declarada es el Papiro de Ani, British Museum, inventario `EA10470`.
- La fuente permanece explícitamente en `not_ingested`; no se incorpora texto primario sin ingestión verificable.

## Controles verificados por inspección

1. El manifiesto exige identidad de corpus, versión, estado, fuente primaria, fuentes y política.
2. La validación determinista detecta claves ausentes, fuentes duplicadas, referencia primaria inválida y políticas no habilitadas.
3. Las pruebas existentes cubren contrato de esquema, política antificción y estado de ingestión de la fuente primaria.
4. El árbol remoto actual contiene únicamente el núcleo mínimo de gobernanza/validación; el andamio local histórico no debe asumirse sincronizado.

## Corrección aplicada

Se añadió un workflow de GitHub Actions que ejecuta en `push` a `main` y en `pull_request` contra `main`:

- `python -m src.validacion.corpus_manifest`
- `python -m pytest -q`

El runner instala explícitamente `pytest` antes de ejecutar las pruebas.

## Límite de auditoría

La ejecución de comandos dentro del entorno local Termux/Kali no es demostrable desde el conector GitHub. Por tanto, no se declara como ejecutada la validación del árbol local hasta que el árbol local sea sincronizado y sus resultados sean aportados por ejecución local o por un entorno CI reproducible.

## Próximo salto lógico

1. Integrar este gate de validación mediante PR.
2. Esperar y auditar el resultado de GitHub Actions.
3. Sincronizar el árbol local con `origin/main` sin `force push`.
4. Comparar el árbol local con el remoto y separar infraestructura de cualquier contenido placeholder.
5. Sólo después iniciar la primera ingestión primaria trazable, con identificador de unidad, procedencia, hash y estado de validación.
