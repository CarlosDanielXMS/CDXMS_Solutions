# Dependency Resolver — Arquitetura v1.0.0

O Dependency Resolver é a segunda capability da Fase 3. Ele não instala artifacts. Sua responsabilidade é impedir que o Artifact Manager avance com instalação quando dependências estão ausentes, incompatíveis ou cíclicas.

## Relação com Artifact Manager

Fluxo futuro:

```text
Artifact Manager
→ validate_artifact
→ Dependency Resolver
→ build_resolution_plan
→ Artifact Manager
→ build_install_plan / install_local_artifact
```

## Fonte de dados

- Manifest do artifact alvo.
- Registry local instalado.
- Catálogo disponível local/remoto.
- Política opcional de resolução.

## Escopo v1.0.0

- validação de dependências;
- comparação com registry;
- constraints de versão;
- grafo lógico;
- detecção de ciclos;
- ordem de instalação;
- plano seguro.
