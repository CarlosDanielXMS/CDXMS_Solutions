# Testes manuais — [CDXMS] Dependency Resolver v1.0.0

## Cenários mínimos

1. Manifest sem dependências deve retornar plano `ready`.
2. Manifest com dependências já instaladas deve retornar `ready` e constraints satisfeitas.
3. Manifest com dependência ausente mas presente no catálogo deve retornar plano com ordem de instalação.
4. Manifest com dependência ausente e fora do catálogo deve retornar `blocked` com `MISSING_DEPENDENCY`.
5. Manifest com versão incompatível deve retornar `VERSION_CONFLICT`.
6. Catálogo com ciclo deve retornar `DEPENDENCY_CYCLE_DETECTED`.

## Critério de aceite

Todas as operações devem retornar `Resultado` preenchido e respeitar o contrato CDXMS.
