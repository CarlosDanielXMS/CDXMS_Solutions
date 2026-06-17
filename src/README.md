# CDXMS — Ecosystem Core Base v1.0.0

Base inicial do ecossistema CDXMS Solutions para MacroDroid.

## Capabilities incluídas

- `[CDXMS] Json Config Manager`
- `[CDXMS] Bootstrap`
- `[CDXMS] Registrar Resultado`
- `[CDXMS] Logger`
- `[CDXMS] String Utils`

## Saneamento pré-release v1.0.0

Este pacote consolida todas as capabilities já criadas sem alteração de versão pública. A versão permanece `1.0.0` porque ainda não houve release oficial, disponibilização estável para usuários finais ou validação completa em dispositivo limpo.

Principais ajustes:

- Manifest de cada capability recebeu `implementation_audit`.
- Catálogo de ações MacroDroid incorporado em `docs/`.
- Auditoria nativa reescrita sem sugerir `v1.0.1`.
- Checksums recalculados para a árvore consolidada.
- Script único de validação estrutural adicionado em `scripts/`.
- Shell continua restrito ao JCM como fallback controlado pendente de homologação real com FileOperation.

## Como validar

```bash
python src/scripts/validate_core_capabilities_v1_0_0_sanitized.py
```

Depois, importar os `.ablock` no MacroDroid real e executar os testes manuais de cada capability.


## Homologation fix — v1.0.0 pre-release

- Mantida versão 1.0.0.
- Corrigida interpretação de booleanos localizados (`Verdadeiro`/`Falso`) em Magic Text.
- Reforçada serialização de dados textuais com aspas para Result Manager.


## Homologation fix 2 — String Utils v1.0.0

- Mantida versão 1.0.0.
- Ajustada publicação de Resultado da String Utils para evitar falha de Data Json ao atravessar Magic Text para Result Manager.
- Validação estrutural automatizada mantida com PASS=114 WARN=0 FAIL=0.
