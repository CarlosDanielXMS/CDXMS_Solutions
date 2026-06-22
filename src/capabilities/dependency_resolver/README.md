# [CDXMS] Dependency Resolver v1.0.0

Resolvedor puro/stateless de dependências, versões, ciclos e ordem de instalação.

## Responsabilidade

Esta capability executa somente o domínio descrito em seu contrato. A saída pública única é `Resultado`.

## Operações

- `validate_dependencies`
- `get_missing_dependencies`
- `check_version_constraints`
- `build_dependency_graph`
- `build_resolution_plan`
- `detect_dependency_cycles`
- `sort_install_order`
- `validate_install_plan`

## Dependências

{"result_manager": ">=1.0.0", "string_utils": ">=1.0.0"}

## Distribuição

O export MacroDroid está em `macrodroid/[CDXMS]_Dependency_Resolver.ablock`. A importação continua manual até homologação específica de importação automática.
