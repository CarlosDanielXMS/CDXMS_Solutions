# Distribuição remota GitHub — Arquitetura v1.0.0

## Estado homologado

- Remote Source Manager para documentos JSON do plano de controle: homologado em `2026-06-20`, `23/23`;
- executor SHA-256: homologado com `/system/bin/sha256sum`, `7/7`;
- `[CDXMS] File Integrity`: homologado em `2026-06-21`, `11/11`;
- payload verificado e instalação remota: ainda não promovidos para o fluxo oficial.

## Ordem arquitetural

Antes de ampliar o transporte remoto, o ecossistema deve provar sua entrada única em dispositivo vazio.

```text
[CDXMS] Solutions Manager importado uma vez
  -> bootstrap local offline
  -> runtime mínimo validado
  -> plano de controle remoto
  -> payload verificado
  -> importação guiada
  -> receipt
  -> registry
```

## Separação de responsabilidades

- **Solutions Manager:** única macro permanente de entrada e orquestração;
- **Bootstrap:** inicialização, verificação e reparo local;
- **Json Config Manager:** filesystem e JSON;
- **Remote Source Manager:** source, URL, HTTP e staging;
- **File Integrity:** cálculo e comparação SHA-256;
- **Dependency Resolver:** resolução pura de dependências;
- **Artifact Manager:** planejamento e lifecycle via JCM.

## Plano de controle remoto já homologado

```text
Sources/Catalog control JSON
  -> Remote Source Manager
      -> valida source/url/path
      -> HTTP Request GET
      -> staging temporário
      -> valida status/schema/namespace/identidade
      -> JCM relê o JSON
  -> chamador recebe Resultado + cache.file_path
```

## Integridade homologada

Remote manifests e `checksums.json` publicam SHA-256. A validação local deve ser delegada ao `[CDXMS] File Integrity`, que foi homologado com executor fixo, non-root, sem Helper e sem Shizuku.

## Payload verificado futuro

```text
remote_manifest.files[]
  -> RSM baixa um arquivo para staging
  -> File Integrity verifica checksum_sha256
  -> somente matches=true produz staged_verified
```

`staged_verified` não significa `installed`.

## Importação no MacroDroid

A v1 não presume importação automática de `.macro` ou `.ablock`. O baseline será:

```text
download -> checksum -> awaiting_import -> importação manual guiada -> receipt -> runtime_detected -> registered
```

## Regras de segurança

- HTTPS obrigatório;
- host permitido: `raw.githubusercontent.com`;
- `/blob/` bloqueado;
- remote path relativo e sem traversal;
- download sempre em staging;
- `allowAnyCertificate = false`;
- transporte remoto nunca sobrescreve diretamente um artifact instalado;
- registry só muda após evidência real de runtime.
