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
