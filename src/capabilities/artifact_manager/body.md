# Corpo — [CDXMS] Artifact Manager v1.0.0

## Entradas

- Operation: operação técnica do Artifact Manager.
- Artifact Type: tipo do artifact.
- Artifact Id: id técnico do artifact.
- Manifest Json: manifest JSON do artifact.
- Contract Json: contract JSON do artifact, quando aplicável.
- Config Json: config/default JSON do artifact, quando aplicável.
- Registry Json: registry local atual.
- Package Manifest Json: manifest de package/local bundle.
- Local Package Path: caminho local do pacote de origem.
- Target Root Path: raiz de destino CDXMS.
- Preserve User Config?: preserva config do usuário.
- Dry Run?: retorna apenas plano seguro.
- Strict Mode?: validação mais rígida.
- Session Id: sessão lógica.
- Correlation Id: correlação da execução.

## Saída

- Resultado: dicionário CDXMS padronizado.

## Variáveis de trabalho

- Tmp_ArtifactWorkJson
- Tmp_ArtifactWork

## Corpo passo a passo

### Ação 1 — Action Group

Nome: `01 — Processar Artifact`.

Objetivo: organizar visualmente o processamento principal do Artifact Manager.

### Ação 2 — JavaScript Code

Configuração:

- Engine: JetPack JavaScriptEngine.
- Block next action: habilitado.
- Saída textual: `Tmp_ArtifactWorkJson`.

Função:

1. Lê as entradas via Magic Text.
2. Normaliza booleanos localizados (`Verdadeiro`/`Falso`).
3. Valida `Operation`.
4. Faz parse seguro de `Manifest Json`, `Contract Json`, `Config Json`, `Registry Json` e `Package Manifest Json`.
5. Valida manifest mínimo.
6. Calcula paths de destino.
7. Gera `registry_entry` e `install_plan` quando aplicável.
8. Retorna JSON no contrato `Resultado`.

### Ação 3 — JSON Parse

Configuração:

- Entrada: `Tmp_ArtifactWorkJson`.
- Saída: `Resultado`.
- Chaves: raiz do dicionário.

Objetivo: publicar o Resultado final como dicionário público.

### Ação 4 — End Action Group

Encerra o grupo principal.

### Ação 5 — Exit Action Block

Encerra explicitamente o Action Block após publicar `Resultado`.
