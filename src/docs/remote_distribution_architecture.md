# Distribuição remota GitHub — preparação mínima v1.0.0

## Decisão

```text
GitHub raw -> camada remota futura -> cache via JCM -> Dependency Resolver -> Artifact Manager -> apply/verify via JCM
```

Nesta etapa não é criada uma capability de download. A entrega apenas padroniza os contratos e arquivos de controle necessários.

## Fonte de homologação

`catalogs/sources.json` contém uma única fonte oficial habilitada, apontando para `develop`. Usuários finais não devem instalar de `develop`; a release estável futura trocará `ref` e `base_raw_url` por uma tag/release.

## Catálogo

`catalogs/local_catalog.default.json` lista o core e as capabilities atuais. Ele aponta para manifests e remote manifests; não duplica o conteúdo completo dos artifacts.

## Remote manifest schema v1

Cada artifact mantém:

- `source.type`;
- `source.repository`;
- `source.ref`;
- `source.base_raw_url`;
- `files[].path`;
- `files[].target_path`;
- `files[].write_policy`;
- `files[].checksum_sha256`;
- dependências e metadados do export MacroDroid.

## Regras

- Nunca usar `/blob/` como arquivo cru.
- Config defaults viram `config.json` por criação/merge, sem sobrescrita destrutiva.
- O download futuro deve ocorrer primeiro em cache.
- O AM não baixa nem grava diretamente.
- O JCM executa filesystem/JSON.
- `.macro` e `.ablock` continuam exigindo importação manual até homologação específica.
