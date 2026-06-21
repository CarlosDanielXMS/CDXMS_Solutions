# Distribuição remota GitHub — Remote Source Manager v1.0.0

## Estado de homologação

O plano de controle remoto foi homologado no dispositivo em `2026-06-20` com `[CDXMS] Homologar Remote Source Manager v1.0.6 TEMP` e `23/23` verificações aprovadas. O escopo confirmado inclui fonte/URL/path, HTTP GET, persistência em staging, validação JSON, releitura JCM, tratamento de falhas e ausência de alteração no registry.

Payloads de artifacts, instalação e importação automática permanecem fora do escopo homologado. A homologação SHA-256 em runtime permanece em prova controlada. A tentativa v1.0.0 foi inconclusiva porque o relatório fallback não foi sobrescrito; a v1.0.1 executa no contexto non-root nativo sem Helper e adiciona estágios diagnósticos.

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

Os remote manifests e `checksums.json` já publicam SHA-256. O catálogo nativo auditado do MacroDroid não expõe ação simples de checksum. Por isso, antes de alterar o RSM ou criar uma capability, foi preparado um harness isolado de runtime.

### Harness SHA-256

Macro: `[CDXMS] Homologar SHA-256 Runtime v1.0.1 TEMP`.

O harness testa, sem root, cinco formas possíveis de obter SHA-256 e só seleciona um executor que reproduza um digest conhecido. Em seguida exige `7/7` checks, incluindo path com espaços, arquivo de 1024 bytes e rejeição de arquivo inexistente.

Esta fase não habilita payloads nem declara checksum homologado. O resultado real do dispositivo decidirá se o mecanismo pode ser promovido para uma capability reutilizável.

## Regras de segurança

- HTTPS obrigatório.
- Host permitido: `raw.githubusercontent.com`.
- `/blob/` bloqueado.
- Remote Path relativo, sem `..`, URL completa, query ou fragmento.
- Download sempre em staging temporário.
- `allowAnyCertificate = false`.
- Nenhum arquivo instalado é sobrescrito pelo transporte remoto.


## Próxima fronteira

```text
Remote manifest file
  -> RSM baixa para staging
  -> File Integrity verifica checksum_sha256
  -> somente matches=true produz staged_verified
```

Essa integração ainda não está habilitada nesta entrega.
