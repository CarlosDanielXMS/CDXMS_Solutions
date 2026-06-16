# Arquitetura — CDXMS Logger v1.0.0

O Logger é a capability de observabilidade local da base CDXMS. Ele não participa de lifecycle remoto, instalação, registry ou resolução de dependências. Sua função é registrar fatos operacionais em JSON Lines para auditoria, diagnóstico e suporte.

## Posição na base

```text
JCM -> Bootstrap -> Result Manager -> Logger
```

- O JCM garante filesystem/JSON local.
- O Bootstrap prepara core/runtime.
- O Result Manager padroniza a saída `Resultado`.
- O Logger registra eventos e resultados em arquivos locais.

## Formato JSON Lines

Cada linha gravada é independente e possui:

- `schema_version`
- `namespace`
- `log_type`
- `level`
- `event_type`
- `message`
- `timestamp`
- `source`
- `correlation_id`
- `session_id`
- `tags`
- `data`
- `error`
- `result`
- `warnings`

## Decisões

- Append-only por padrão.
- Um arquivo por escopo e dia.
- `get_log_status` não grava arquivo.
- CDN/GitHub fora do escopo.
- Rotação avançada fica para política futura de runtime/manager, não para o Logger v1.0.0.
