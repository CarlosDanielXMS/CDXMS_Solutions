# Arquitetura — [CDXMS] Bootstrap v1.0.0

O Bootstrap é a segunda capability estrutural do ecossistema, construída incrementalmente sobre o JCM já presente na branch `feat/create-ecosystem-core`.

## O que o Bootstrap faz

- Garante inicialização local do ecossistema.
- Verifica core mínimo.
- Repara core por meio do JCM quando autorizado.
- Prepara runtime/cache/logs/packages/backups.
- Carrega contexto completo para reduzir chamadas repetidas ao JCM.

## O que o Bootstrap não faz

- Não baixa arquivos da CDN.
- Não instala artifact remoto.
- Não registra capability/solution.
- Não resolve dependências complexas.
- Não renderiza UI.

Essas responsabilidades pertencem às próximas camadas: Artifact Manager, Dependency Resolver e Manager.

## Estrutura remota vs dispositivo

No GitHub os arquivos ficam sob `src/`.

No dispositivo do usuário, `src/` não existe.

O `remote_manifest.json` usa `base_raw_url` terminando em `/src`, e os `target_path` continuam sem `src/`.
