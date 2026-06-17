# CDXMS — Ecosystem Core Base v1.0.0

Base inicial do ecossistema CDXMS Solutions para MacroDroid.

## Capabilities incluídas

- `[CDXMS] Json Config Manager`
- `[CDXMS] Bootstrap`
- `[CDXMS] Registrar Resultado`
- `[CDXMS] Logger`
- `[CDXMS] String Utils`
- `[CDXMS] Artifact Manager`
- `[CDXMS] Dependency Resolver`

## Saneamento pré-release v1.0.0

Este pacote consolida todas as capabilities já criadas sem alteração de versão pública. A versão permanece `1.0.0` porque ainda não houve release oficial, disponibilização estável para usuários finais ou validação completa em dispositivo limpo.

Principais ajustes:

- Manifest de cada capability recebeu `implementation_audit`.
- Catálogo de ações MacroDroid incorporado em `docs/`.
- Auditoria nativa reescrita sem sugerir `v1.0.1`.
- Checksums recalculados para a árvore consolidada.
- Script único de validação estrutural adicionado em `scripts/`.
- Shell continua restrito ao JCM como fallback controlado pendente de homologação real com FileOperation.

## Como validar

```bash
python src/scripts/validate_core_capabilities_v1_0_0_sanitized.py
```

Depois, importar os `.ablock` no MacroDroid real e executar os testes manuais de cada capability.


## Homologation fix — v1.0.0 pre-release

- Mantida versão 1.0.0.
- Corrigida interpretação de booleanos localizados (`Verdadeiro`/`Falso`) em Magic Text.
- Reforçada serialização de dados textuais com aspas para Result Manager.


## Homologation fix 2 — String Utils v1.0.0

- Mantida versão 1.0.0.
- Ajustada publicação de Resultado da String Utils para evitar falha de Data Json ao atravessar Magic Text para Result Manager.
- Validação estrutural automatizada mantida com PASS=114 WARN=0 FAIL=0.


## Artifact Manager v1.0.0 — Fase 3

Esta entrega adiciona `[CDXMS] Artifact Manager` à base Core v1.0.0 já homologada.

Diferente de um pacote diferencial isolado, este package é incremental mesclado: contém todos os arquivos anteriores da base Core homologada e adiciona/atualiza os arquivos necessários para registrar o Artifact Manager.

Escopo inicial:

- validar manifests e contratos de artifacts;
- gerar status local de artifact;
- construir entrada de registry;
- calcular paths de destino;
- montar plano local seguro de instalação;
- manter operações persistentes/destrutivas em modo planejado até homologação completa do lifecycle.

Fora do escopo desta entrega:

- download remoto via GitHub;
- resolução completa de dependências;
- instalação automática de `.macro`/`.ablock` dentro do MacroDroid.

Validação recomendada:

```bash
python src/scripts/validate_core_plus_artifact_manager_v1_0_0.py
python src/capabilities/artifact_manager/scripts/validate_artifact_manager_incremental.py
```


## Artifact Manager homologation fix 1 — v1.0.0

- Mantida versão `1.0.0`.
- Corrigida inconsistência interna do Action Block `[CDXMS] Artifact Manager`: o JavaScript escrevia em `Tmp_StringWorkJson`, mas o `JsonParseAction` lia `Tmp_ArtifactWorkJson`.
- Após a correção, as saídas `Tmp_AM_*` da macro de homologação devem ser preenchidas.


## Dependency Resolver v1.0.0

- Mantida versão 1.0.0.
- Adicionada capability `[CDXMS] Dependency Resolver`.
- Resolve dependências declaradas em manifests, valida constraints, detecta ciclos e gera plano seguro.
- Não instala, não baixa e não altera registry nesta versão.


## Integração AM + DR — v1.0.0 pre-release

- Mantida versão 1.0.0.
- Adicionada macro temporária para homologar a integração por orquestração entre Artifact Manager e Dependency Resolver.
- Mantido `Dry Run? = true` para impedir efeitos físicos durante homologação.
- Definido que a fase remota futura usará `develop` como ref inicial de homologação.


## AM/DR Concept Remodel — v1.0.0

- Dependency Resolver não depende mais do Artifact Manager.
- Artifact Manager continua como orquestrador de lifecycle.
- Artifact Manager aceita `Dependency Resolution Json` para compor planos dependency-aware.
- Não foi criado Action Block intermediário nesta etapa.
