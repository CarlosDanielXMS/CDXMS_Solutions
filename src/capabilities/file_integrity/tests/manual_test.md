# Homologação manual — [CDXMS] File Integrity v1.0.0

## Estado

Homologação concluída no dispositivo em `2026-06-21` com `[CDXMS] Homologar File Integrity v1.0.0 TEMP`.

Resultado consolidado:

- casos: `11`;
- aprovados: `11`;
- falhas: `0`;
- executor: `/system/bin/sha256sum`;
- non-root: `true`;
- Helper: `false`;
- Shizuku: `false`;
- registry alterado: `false`.

## Casos homologados

1. `calculate_sha256` para arquivo contendo `abc`;
2. `verify_sha256` com digest correto;
3. digest divergente retornando `CHECKSUM_MISMATCH`;
4. arquivo vazio;
5. path com espaços;
6. arquivo de 1024 bytes;
7. arquivo inexistente retornando `FILE_NOT_FOUND`;
8. hash esperado malformado bloqueado antes do shell;
9. path inseguro bloqueado antes do shell;
10. operação desconhecida bloqueada;
11. `core/registry.json` preservado.

## Regressão obrigatória

Qualquer alteração no Action Block deve repetir os onze casos. A homologação não autoriza download, instalação, alteração de registry nem importação automática de artifacts.
