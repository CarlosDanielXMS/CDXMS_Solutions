# [CDXMS] Registrar Resultado

Capability pura responsável por construir, normalizar, validar e propagar `Resultado` conforme o contrato universal CDXMS.

Ela não acessa GitHub, não escreve arquivos e não instala artifacts. Seu objetivo é reduzir duplicação de montagem de resultado nas demais capabilities.

## Operações

- `build_result`
- `normalize_result`
- `validate_result`
- `propagate_result`
- `wrap_error`
- `register_result`

## Saída

Saída pública única:

```text
Resultado
```

Dados úteis sempre em:

```text
Resultado.data
```

Campos proibidos no topo:

```text
data_json
error_code
error_message
error_json
```

## Efeito colateral

Nenhum. Esta capability é pura.

## Saneamento pré-release v1.0.0

A capability permanece na versão `1.0.0`. Este ajuste registra a auditoria de ações nativas, JS e Shell antes da primeira release oficial.

- Política: `native_first_when_safe_clear_and_homologated`.
- JS: `1` ocorrência(s).
- Shell: `0` ocorrência(s).
- Decisão: Mantém JavaScript por ser fábrica/normalizadora de Resultado. Reescrever em ações visuais aumentaria ações e risco sem ganho.

