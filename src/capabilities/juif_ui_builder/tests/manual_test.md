# Teste manual — JUIF UI Builder v1.0.0

## Pré-condições

- importar `[CDXMS] JUIF UI Builder`;
- importar `[CDXMS] Java UI Framework` para o teste end-to-end.

## Casos obrigatórios

1. `Config Json = {}` e schema mínimo válido retornam `success=true`.
2. JSON vazio retorna `MISSING_REQUIRED_INPUT`.
3. JSON inválido retorna `INVALID_JSON`.
4. Componente desconhecido retorna `INVALID_ENUM_VALUE`.
5. `bind` hidrata state e cria entrada em `mapping_json`.
6. `Escape Json=false` mantém a cópia não escapada.
7. Todos os 26 componentes legados permanecem aceitos.
8. Os 10 componentes v1.0.0 aparecem em `supported_components`.
9. `shell.top_app_bar`, `bottom_navigation`, `navigation_rail`, `navigation_drawer` e `tab_bar` são normalizados.
10. Aliases `top_bar`, `bottom_bar`, `rail`, `drawer` e `tabs` funcionam.
11. O JSON produzido é aceito pelo Java UI Framework.
12. Apenas `Resultado` aparece como saída pública.

## Aceite

Registrar quantidade aprovada/reprovada. Não marcar a capability como homologada antes da execução real no dispositivo.
