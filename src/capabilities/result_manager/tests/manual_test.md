# Testes manuais — [CDXMS] Registrar Resultado v1.0.0

## Teste 1 — build_result sucesso

Entradas:

```text
Operation = build_result
Source Artifact Type = capability
Source Artifact Id = result_manager
Source Operation = build_result
Success? = true
Message = Operação executada com sucesso.
Data Json = {"value":"ok"}
Strict Mode? = true
```

Esperado:

```text
Resultado.success = true
Resultado.status = success
Resultado.data.value = ok
```

## Teste 2 — validate_result bloqueia data_json

Entradas:

```text
Operation = validate_result
Result Json = {"success":true,"status":"success","data_json":"{}"}
Strict Mode? = true
```

Esperado:

```text
Resultado.success = false
Resultado.error.code = RESULT_FORBIDDEN_TOP_LEVEL_FIELD
```

## Teste 3 — normalize_result

Entradas:

```text
Operation = normalize_result
Result Json = {"success":true,"message":"OK","data":{"x":1}}
Strict Mode? = false
```

Esperado:

```text
Resultado.success = true
Resultado.data.normalized = true
Resultado.data.value.success = true
```

## Teste 4 — propagate_result erro filho

Entradas:

```text
Operation = propagate_result
Source Artifact Type = capability
Source Artifact Id = bootstrap
Source Operation = initialize_ecosystem
Result Json = {"success":false,"status":"error","message":"Falha filha.","data":{},"error":{"code":"TEST_ERROR","message":"Erro teste.","details":{},"recoverable":false}}
Context Json = {"caller":"bootstrap"}
```

Esperado:

```text
Resultado.success = false
Resultado.status = error
Resultado.error.code = TEST_ERROR
Resultado.data.propagated = true
```
