# CDXMS Core Capabilities v1.0.0 — Homologation Fix Report

Data: 2026-06-16T23:41:27Z
Versão mantida: 1.0.0

## Motivo

A execução da macro temporária de homologação mostrou que o MacroDroid localiza valores booleanos como `Verdadeiro`/`Falso` ao expor variáveis de dicionário em Magic Text. Alguns scripts internos estavam aceitando apenas `true`/`false` em inglês.

## Sintomas observados

- `ensure_folder`, `write_json` e `read_json` retornaram erro de path inválido mesmo com caminhos dentro de `/storage/emulated/0/Documents/CDXMS_Solutions`.
- Vários resultados estavam com `status = success`, `error = null`, mas `success = Falso`.
- `escape_json_string` falhou ao repassar `Data Json` com aspas para o Result Manager.
- `bootstrap_status` retornou `incomplete` porque as verificações de existência eram interpretadas como falsas.

## Correções aplicadas

### Json Config Manager

- Adicionado parser booleano tolerante a `true`, `false`, `Verdadeiro`, `Falso`, `sim`, `não`, `1` e `0`.
- Corrigida leitura de `Tmp_Work[valid_file_path]`, `Tmp_Work[valid_folder_path]`, `Tmp_Work[create_if_missing]` e `Tmp_Work[pretty_print]`.

### Bootstrap

- Corrigida interpretação de flags e resultados de checks vindos do JCM.
- `get_status`, `verify_core` e `repair_core` passam a aceitar booleanos localizados.

### Result Manager

- Corrigida entrada `Success?` para aceitar booleanos localizados.

### Logger

- Corrigida entrada `Strict Mode?`.
- Tornada a serialização de `data_json` mais segura para passagem via Magic Text.

### String Utils

- Corrigida entrada `Allow Slash?`.
- Tornada a serialização de `data_json`/`error_json` mais segura para textos com aspas, barras e JSON embutido.

## Validação automatizada

Os exports foram validados estruturalmente como JSON e mantiveram `macroExportVersion = 1`. A homologação funcional ainda precisa ser repetida dentro do MacroDroid real com a macro temporária.

## Ordem de importação recomendada

1. `[CDXMS] Json Config Manager`
2. `[CDXMS] Registrar Resultado`
3. `[CDXMS] Bootstrap`
4. `[CDXMS] Logger`
5. `[CDXMS] String Utils`
6. `[CDXMS] Homologar Core v1.0.0 TEMP`
