# CDXMS Solutions

Ecossistema modular de solutions e capabilities para MacroDroid.

Esta consolidação fecha a fundação de integridade/entrada única e adiciona as capabilities de UI que antecedem o `[CDXMS] Solutions Manager`.

## Estado

- branch-base: `feat/create-ecosystem-core`;
- commit-base documental: `626c37a02fe0beb5b806b4df33f801749ba6bf9b` + formalização remota da entrada única;
- Remote Source Manager, plano de controle: homologado `23/23`;
- SHA-256 runtime: homologado `7/7`;
- File Integrity de produção: homologado `11/11`;
- Java UI Framework v1.0.0: preparado para homologação;
- JUIF UI Builder v1.0.0: preparado para homologação;
- Solutions Manager: próxima etapa após a homologação das capabilities de UI.

## Capabilities de UI

- `[CDXMS] Java UI Framework` — renderer JUIF com 36 componentes e shell declarativo no conteúdo rolável;
- `[CDXMS] JUIF UI Builder` — normalizador de schema, bindings, state, mapping e shell.

Os 26 componentes do protótipo foram preservados. Foram adicionados componentes de navegação, busca, filtros e estados vazios/carregamento.

## Decisão de entrada

O usuário importará apenas `[CDXMS] Solutions Manager`. Na primeira execução, a macro atuará como bootstrapper; nas seguintes, como manager. Não haverá Installer separado na v1.

## Validação estática

```bash
python src/scripts/validate_ui_capabilities_v1_0_0.py
python src/capabilities/bootstrap/scripts/validate_bootstrap_incremental.py
python src/capabilities/file_integrity/scripts/validate_file_integrity_incremental.py
python src/scripts/validate_remote_distribution_readiness_v1_0_0.py
```


## Correção aplicada

As capabilities de UI foram corrigidas para seguir `core/result_contract.json`; a hierarquia-base do renderer do protótipo foi restaurada e os validadores agora rejeitam campos legados proibidos.
