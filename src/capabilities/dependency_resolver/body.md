# Corpo — [CDXMS] Dependency Resolver v1.0.0

## Entradas

- `Operation`: operação técnica do Dependency Resolver.
- `Artifact Manifest Json`: manifest JSON do artifact alvo cujas dependências serão resolvidas.
- `Installed Registry Json`: registry local atual com artifacts instalados.
- `Available Catalog Json`: catálogo disponível com artifacts que podem satisfazer dependências ausentes.
- `Dependency Policy Json`: política opcional de resolução.
- `Strict Mode?`: quando verdadeiro, inconsistências bloqueiam o resultado.
- `Session Id`: identificador lógico da sessão.
- `Correlation Id`: identificador de correlação para logs/resultados.

## Saída

- `Resultado`: dicionário único no contrato CDXMS.

## Variáveis de trabalho

- `Tmp_DependencyWorkJson`: JSON textual intermediário retornado pelo motor interno.
- `Tmp_DependencyWork`: dicionário reservado para inspeção/futuras composições.

## Corpo passo a passo

### Ação 1 — Action Group

- Ação: `ActionGroupAction`.
- Nome: `01 — Resolver Dependências`.
- Objetivo: agrupar o processamento interno da capability.

### Ação 2 — JavaScript

- Ação: `JavaScriptAction`.
- Engine: `JetPack JavascriptEngine`.
- `blockNextAction`: `true`.
- Saída textual: `Tmp_DependencyWorkJson`.
- Objetivo: ler as entradas por Magic Text, validar JSONs, extrair dependências, consultar registry/catálogo, calcular constraints, grafo, ciclos, ordem e plano de resolução.
- Observação: parsing de booleanos aceita `true/false`, `Verdadeiro/Falso`, `sim/não`, `yes/no`, `1/0`.

### Ação 3 — JSON Parse

- Ação: `JsonParseAction`.
- Entrada: `Tmp_DependencyWorkJson`.
- Saída: `Resultado`.
- Objetivo: publicar diretamente o Resultado, evitando passagem frágil de JSON por outro Action Block.

### Ação 4 — End Action Group

- Ação: `ActionGroupEndAction`.
- Objetivo: encerrar o agrupamento lógico.

### Ação 5 — Exit Action Block

- Ação: `ExitActionBlockAction`.
- Configuração: saída já publicada em `Resultado`.
- Objetivo: finalizar a capability explicitamente.
