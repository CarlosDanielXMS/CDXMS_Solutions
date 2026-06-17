# [CDXMS] Dependency Resolver v1.0.0

Capability responsável por resolver dependências declaradas entre artifacts CDXMS antes da instalação real.

## Escopo v1.0.0

Esta versão foca em validação, grafo, constraints de versão, detecção de ciclos, ordem de instalação e plano seguro de resolução. Ela não baixa arquivos, não altera registry e não instala artifacts fisicamente.

## Operações

- `validate_dependencies`
- `get_missing_dependencies`
- `check_version_constraints`
- `build_dependency_graph`
- `build_resolution_plan`
- `detect_dependency_cycles`
- `sort_install_order`
- `validate_install_plan`

## Saída

Saída pública única: `Resultado`.


## Remodelagem AM/DR

O Dependency Resolver é uma capability pura/stateless. Ele não depende do Artifact Manager, não escreve registry, não baixa arquivos e não instala artifacts. Seu papel é receber manifest, registry e catálogo disponível, e devolver um `resolution_plan` para que o Artifact Manager ou outro orquestrador decida o próximo passo.
