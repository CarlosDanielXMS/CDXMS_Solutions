# Distribuição remota GitHub — Remote Source Manager v1.0.0

## Estado de homologação

O plano de controle remoto foi homologado no dispositivo em `2026-06-20` com `[CDXMS] Homologar Remote Source Manager v1.0.6 TEMP` e `23/23` verificações aprovadas. O escopo confirmado inclui fonte/URL/path, HTTP GET, persistência em staging, validação JSON, releitura JCM, tratamento de falhas e ausência de alteração no registry.

Payloads de artifacts, SHA-256 em runtime, instalação e importação automática permanecem fora do escopo homologado.

## Fluxo implementado

```text
Sources/Catalog control JSON
  -> [CDXMS] Remote Source Manager
      -> valida source/url/path
      -> HTTP Request GET
      -> salva em staging temporário
      -> valida status/schema/namespace/identidade
      -> JCM relê e verifica staging
  -> chamador recebe Resultado + cache.file_path
```

## Separação de responsabilidades

- **Remote Source Manager:** fonte, URL, transporte HTTP, validação remota e staging.
- **Json Config Manager:** preparação de pasta e verificação do JSON baixado.
- **Dependency Resolver:** dependências, sem side effects.
- **Artifact Manager:** lifecycle e apply final via JCM.
- **Solutions Manager/Installer futuro:** orquestra o fluxo completo.

## Fonte de homologação

`catalogs/sources.json` mantém uma única fonte oficial apontando para `develop`. Release estável futura usará tag imutável.

## Escopo deliberado da v1.0.0

São suportados apenas documentos JSON do plano de controle:

- catálogo;
- `release.json`;
- `remote_manifest.json`;
- JSON CDXMS genérico com `schema_version` e `namespace`.

Não são executados download em lote, instalação, update de registry, ZIP, GitHub API, repositório privado ou importação automática de exports MacroDroid.

## Integridade

Os remote manifests e `checksums.json` já publicam SHA-256. Entretanto, o catálogo nativo auditado do MacroDroid não expõe ação simples de checksum. Conforme a Knowledge Base, a capability não declara checksum como verificado e bloqueia payloads críticos até existir validação nativa homologada ou capability específica.

## Regras de segurança

- HTTPS obrigatório.
- Host permitido: `raw.githubusercontent.com`.
- `/blob/` bloqueado.
- Remote Path relativo, sem `..`, URL completa, query ou fragmento.
- Download sempre em staging temporário.
- `allowAnyCertificate = false`.
- Nenhum arquivo instalado é sobrescrito pelo transporte remoto.
