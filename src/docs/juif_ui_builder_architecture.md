# Arquitetura — JUIF UI Builder v1.0.0

## Papel

Compiler/normalizador puro entre o schema amigável de UI e o contrato de runtime do Java UI Framework.

## Fronteiras

```text
Config Json + UI Schema Json
→ validação
→ hidratação por bind
→ state + mapping
→ normalização de componentes/shell
→ JUIF UI Json
```

## Compatibilidade

- mantém sections, fields, lists, components e actions;
- mantém os 26 tipos do protótipo;
- adiciona 10 tipos;
- aceita `shell` e alias `navigation`;
- rejeita componente desconhecido antes da renderização.

## Persistência

O Builder não persiste. `mapping_json` orienta a macro/solution a aplicar alterações posteriormente pelo JCM.
