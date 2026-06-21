# Homologação manual — [CDXMS] File Integrity v1.0.0

## Pré-requisitos

1. Importar `[CDXMS] Json Config Manager`.
2. Importar `[CDXMS] File Integrity`.
3. Conceder All Files Access ao MacroDroid.
4. Confirmar que `/system/bin/sha256sum` permanece disponível.

## Casos obrigatórios

1. `calculate_sha256` para arquivo contendo `abc` → digest `ba7816...15ad`.
2. `verify_sha256` com digest correto → `success=true`, `matches=true`.
3. `verify_sha256` com digest divergente → `CHECKSUM_MISMATCH`.
4. arquivo vazio → `e3b0c442...b855`.
5. path com espaços → sucesso.
6. arquivo de 1024 bytes usado no probe → digest `4613a38a...b8b`.
7. arquivo inexistente → `FILE_NOT_FOUND`.
8. hash esperado malformado → `INVALID_INPUT_TYPE` antes do shell.
9. path fora do base path ou com traversal → `UNSAFE_FILE_PATH` antes do shell.
10. operação desconhecida → `UNSUPPORTED_OPERATION`.
11. `core/registry.json` permanece idêntico antes e depois.
12. relatórios efêmeros não permanecem em `cache/file_integrity/runtime` após casos executados.

## Critério de conclusão

A capability só poderá ser marcada como homologada quando todos os casos passarem no dispositivo e o Resultado confirmar executor fixo, contexto non-root sem Helper/Shizuku e ausência de alterações no registry.
