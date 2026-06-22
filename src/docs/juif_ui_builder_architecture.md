# Arquitetura — JUIF UI Builder v1.0.0

## Papel

Compiler/normalizador puro entre o schema amigável e o contrato de runtime do Java UI Framework.

## Fluxo

```text
Config Json + UI Schema Json
→ validação
→ hidratação por bind
→ state + mapping
→ normalização de pages/components/shell
→ JUIF UI Json
```

## Compatibilidade

- mantém sections, fields, lists, components e actions;
- mantém os 26 tipos do protótipo;
- adiciona dez tipos;
- aceita `shell` e alias `navigation`;
- rejeita componente desconhecido antes da renderização;
- preserva propriedades de runtime desconhecidas pelo Builder quando elas pertencem ao schema.

## Shell

O Builder normaliza:

- `top_app_bar`;
- `tab_bar`;
- `navigation_rail`;
- `bottom_navigation`;
- `navigation_drawer`.

Também preserva:

- `visible_pages`;
- `hidden_pages`;
- `active_pages`;
- `active_prefix`;
- `use_page_title`.

Essas propriedades são interpretadas pelo renderer, não pelo Builder.

## UI padrão

A UI canônica usa sete páginas, uma única Tab Bar para o catálogo e seleção agrupada por `active_pages`. O contrato final cobre os 36 componentes e possui 21 bindings.

## Persistência

O Builder não persiste. `mapping_json` orienta a macro ou solution a aplicar alterações posteriormente por meio das capabilities adequadas.
