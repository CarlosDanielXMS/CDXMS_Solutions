# CDXMS — Auditoria de Pontos de Quebra das Capabilities v1.0.0

## Escopo

Capabilities auditadas:

- Json Config Manager
- Bootstrap
- Registrar Resultado
- Logger
- String Utils
- Artifact Manager
- Dependency Resolver

## Achados principais

### 1. Booleanos localizados

Risco já conhecido: MacroDroid pode expor booleanos como `Verdadeiro`/`Falso`. As capabilities atuais devem usar parser robusto, aceitando `true/false`, `Verdadeiro/Falso`, `sim/não`, `1/0`, `yes/no`.

Status: preservado. Nenhum padrão rígido `toLowerCase() === "true"` foi mantido como regra única.

### 2. Saída pública única

Todas as capabilities devem publicar somente `Resultado` como output público. Variáveis `Tmp_*` permanecem internas.

Status: preservado.

### 3. Travessia Magic Text com JSON

Risco: JSON grande ou com aspas/backslashes pode quebrar ao atravessar Magic Text para outra capability. Por isso, String Utils e Dependency Resolver publicam `Resultado` diretamente por `JavaScriptAction -> JsonParseAction`.

Status: preservado.

### 4. Artifact Manager local apply

Problema observado em homologação: `side_effects_enabled` retornou `false` e campos `apply`/`side_effects_delegated_to_shell` não apareceram, indicando uso de versão antiga do Action Block ou gate de aplicação não diagnosticado.

Correção aplicada:

- `Apply Changes?` reforçado como gate explícito.
- Lifecycle operations retornam `apply`, `apply_payload`, `side_effects_delegated_to_shell` e `debug_inputs`.
- Em `Strict Mode`, operações aplicáveis com `Dry Run? = false` e `Apply Changes?` diferente de verdadeiro retornam `blocked` com `ARTIFACT_APPLY_GATE_DISABLED`.
- O plano inclui `apply_gate.reason`, permitindo diagnosticar `dry_run_enabled`, `apply_changes_gate_disabled`, `dependency_resolution_blocked` ou `double_gate_authorized`.

## Resultado esperado no AM Local Apply

Para aplicação física real controlada:

```text
Dry Run? = false
Apply Changes? = true
Strict Mode? = true
```

O resultado esperado em `Tmp_AM_InstallLocalApply` é:

```text
data.apply.should_apply = Verdadeiro
data.apply.reason = double_gate_authorized
data.install_plan.side_effects_enabled = Verdadeiro
data.side_effects_delegated_to_shell = Verdadeiro
data.debug_inputs.apply_changes_parsed = Verdadeiro
data.debug_inputs.dry_run_parsed = Falso
```

## Observação operacional

Se esses campos não aparecerem, o MacroDroid provavelmente está executando uma versão antiga do `[CDXMS] Artifact Manager`. Nesse caso, reimporte o `.ablock` corrigido ou remova manualmente o Action Block antigo antes de importar a macro de homologação.
