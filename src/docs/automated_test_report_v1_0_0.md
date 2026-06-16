# CDXMS Core Capabilities v1.0.0 — Relatório de Testes Automatizados

## Escopo executado

Foram executados testes automatizados e estáticos sobre a base `CDXMS Core Capabilities v1.0.0`. A validação cobre integridade de pacote, JSON, checksums, manifests, contracts, remote manifests, exports `.ablock`, saídas públicas, dependências declaradas e scripts de validação por capability.

Estes testes **não substituem** a importação e execução real dentro do aplicativo MacroDroid; eles validam a consistência técnica dos artifacts fora do app.

## Resultado final

```text
VALIDATION OK — CDXMS core capabilities v1.0.0 pre-release sanitized
PASS=114 WARN=0 FAIL=0
```

## Correções aplicadas durante a execução

- Corrigido `capabilities/json_config_manager/remote_manifest.json`: `source.base_raw_url` agora termina com `/src`, mantendo `target_path` sem `src/`.
- Corrigidos scripts individuais de validação para localizarem corretamente a raiz `src/` no layout atual do repositório/package.
- Ajustados scripts individuais para comparar operações quando `contract.operations` estiver modelado como dicionário por operação.
- Recalculados `src/checksums.json` e `PACKAGE_CHECKSUMS.json`.
- Nenhuma versão foi alterada; todas as capabilities permanecem em `1.0.0`.

## Estatísticas dos Action Blocks

| Capability | Entradas | Saídas | Ações | Classes | JS | Shell | FileOperationV21 | TextManipulation | ActionBlockAction |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| `json_config_manager` | 9 | `Resultado` | 119 | 12 | 25 | 4 | 0 | 0 | 0 |
| `bootstrap` | 8 | `Resultado` | 107 | 10 | 9 | 0 | 0 | 0 | 58 |
| `result_manager` | 15 | `Resultado` | 5 | 5 | 1 | 0 | 0 | 0 | 0 |
| `logger` | 17 | `Resultado` | 14 | 9 | 1 | 0 | 0 | 0 | 2 |
| `string_utils` | 16 | `Resultado` | 8 | 6 | 1 | 0 | 0 | 0 | 1 |

## Comandos executados

### `python src/scripts/validate_core_capabilities_v1_0_0_sanitized.py`

Exit code: `0`

```text
VALIDATION OK — CDXMS core capabilities v1.0.0 pre-release sanitized
```

### `python scripts/run_core_capabilities_v1_0_0_automated_tests.py`

Exit code: `0`

```text
PASS=114 WARN=0 FAIL=0
```

### `python capabilities/bootstrap/scripts/validate_bootstrap_incremental.py`

Exit code: `0`

```text
[OK] Bootstrap v1.0.0 estruturalmente válido.
```

### `python capabilities/logger/scripts/validate_logger_incremental.py`

Exit code: `0`

```text
[OK] Logger v1.0.0 estruturalmente válido.
```

### `python capabilities/result_manager/scripts/validate_result_manager_incremental.py`

Exit code: `0`

```text
[OK] Result Manager v1.0.0 estruturalmente válido.
```

### `python capabilities/string_utils/scripts/validate_string_utils_incremental.py`

Exit code: `0`

```text
[OK] String Utils v1.0.0 estruturalmente válido.
```

## Limitação restante

Ainda não foi possível executar a homologação dentro do app MacroDroid real. Portanto, continuam pendentes testes manuais de importação dos `.ablock`, execução das operações reais e validação de efeitos colaterais em dispositivo Android.
