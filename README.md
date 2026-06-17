# CDXMS Capabilities Audit & Hardening v1.0.0

Package incremental mesclado contendo toda a base atual do ecossistema e a correção preventiva dos pontos de quebra identificados nas capabilities.

## Principal correção

O Artifact Manager local apply agora expõe diagnóstico explícito de gates (`debug_inputs`), `apply`, `apply_payload` e `side_effects_delegated_to_shell`. Em Strict Mode, aplicação física sem `Apply Changes? = true` retorna `blocked`.

## Validação

```bash
python src/scripts/validate_capabilities_hardening_v1_0_0.py
```
