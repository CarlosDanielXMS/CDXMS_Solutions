# Changelog

## 1.0.0 — Dependency Resolver

- Adicionada capability `[CDXMS] Dependency Resolver`.
- Adicionado contrato para validação de dependências, constraints de versão, grafo, ciclos e plano de resolução.
- Mantido escopo sem efeitos colaterais físicos: não baixa, não instala e não altera registry.
- Package incremental mesclado sobre Core + Artifact Manager.


## 1.0.0 — Homologation fix pre-release

- Mantida versão 1.0.0.
- Corrigida interpretação de booleanos localizados em JCM, Bootstrap, Result Manager, Logger e String Utils.
- Corrigida serialização de Data Json em String Utils/Logger para cenários com aspas e JSON embutido.


## 1.0.0 — Saneamento pré-release das capabilities core

- Mantida a versão `1.0.0` para todas as capabilities.
- Adicionada auditoria de uso de ações nativas, JavaScript e Shell nos manifests.
- Adicionado catálogo local de estruturas de ações MacroDroid em `docs/`.
- Adicionada auditoria nativa revisada em `docs/native_action_audit_v1_0_0_pre_release.md`.
- Adicionado relatório consolidado em `docs/pre_release_capability_sanitization_report.md`.
- Adicionado script de validação estrutural consolidada.
- JCM mantém JavaScript como engine e Shell como fallback controlado até teste real de FileOperation.
- Bootstrap permanece fundação mínima dependente apenas do JCM.
- Result Manager, Logger e String Utils mantêm decisões de implementação documentadas.

## 1.0.0 — Logger

- Adicionada capability `[CDXMS] Logger`.
- Adicionado contrato para observabilidade local em JSON Lines.
- Adicionados enums e erros de Logger ao core.
- Action Block exportado em `capabilities/logger/macrodroid/`.

## 1.0.0 — Result Manager

- Adicionada capability `[CDXMS] Registrar Resultado`.
- Adicionado contrato para construção, normalização, validação e propagação de `Resultado`.
- Mantido padrão de saída pública única.

## 1.0.0 final — Json Config Manager

- Adicionada JCM JsonPath Engine v1.
- Suporte a filtros práticos e JsonPath canônico.
- Resultado mantém `data` como dicionário oficial.


## Homologation fix 2 — String Utils v1.0.0

- Mantida versão 1.0.0.
- Ajustada publicação de Resultado da String Utils para evitar falha de Data Json ao atravessar Magic Text para Result Manager.
- Validação estrutural automatizada mantida com PASS=114 WARN=0 FAIL=0.


## 1.0.0 — Artifact Manager v1.0.0 incremental merged

- Mantida versão pública `1.0.0`.
- Adicionada capability `[CDXMS] Artifact Manager`.
- Atualizados `core/enums.json`, `core/errors.json`, `release.json`, `checksums.json`, `README.md` e documentação em `docs/`.
- Package corrigido para ser incremental mesclado, contendo toda a base Core homologada anterior mais as alterações do Artifact Manager.
- Download remoto e Dependency Resolver permanecem fora do escopo desta entrega.


## Artifact Manager v1.0.0 — Homologation fix 1

- Mantida versão `1.0.0`.
- Corrigida publicação de `Resultado` no Action Block `[CDXMS] Artifact Manager`.
- `JavaScriptAction` agora grava em `Tmp_ArtifactWorkJson`, que é a variável lida pelo `JsonParseAction`.
- Macro temporária de homologação deve retornar `Tmp_AM_*` preenchidas após esta correção.
