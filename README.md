# CDXMS Solutions

Ecossistema modular de solutions e capabilities para MacroDroid.

Esta consolidação fecha a homologação do `[CDXMS] File Integrity` e formaliza a arquitetura de **entrada única** da v1.

## Estado

- branch-base: `feat/create-ecosystem-core`;
- commit-base consultado: `626c37a02fe0beb5b806b4df33f801749ba6bf9b`;
- Remote Source Manager, plano de controle: homologado `23/23`;
- SHA-256 runtime: homologado `7/7`;
- File Integrity de produção: homologado `11/11`;
- Solutions Manager: ainda não implementado;
- prova de macro única + Action Blocks incorporados: pronta para homologação.

## Decisão de entrada

O usuário importará apenas:

```text
[CDXMS] Solutions Manager
```

Na primeira execução, a macro atuará como bootstrapper. Nas seguintes, como manager. Não haverá uma macro Installer separada na arquitetura v1.

## Próximo gate

Importar `[CDXMS] Homologar Entrada Única Bootstrap v1.0.0 TEMP` em um ambiente sem os Action Blocks TEMP correspondentes e confirmar `7/7` verificações.

## Validação estática

```bash
python src/scripts/validate_single_entry_bootstrap_homologation_v1_0_0.py
python src/capabilities/bootstrap/scripts/validate_bootstrap_incremental.py
python src/capabilities/file_integrity/scripts/validate_file_integrity_incremental.py
python src/scripts/validate_remote_distribution_readiness_v1_0_0.py
```
