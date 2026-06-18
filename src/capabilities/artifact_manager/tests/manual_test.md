# Teste manual — Artifact Manager v1.0.0 local apply via JCM

## Cenário seguro

Use `Target Root Path` apontando para uma área de homologação:

```text
/storage/emulated/0/Documents/CDXMS_Solutions/runtime/homologation/am_local_apply
```

## Teste 1 — Dry-run

Entradas principais:

- `Operation = install_local_artifact`
- `Artifact Type = capability`
- `Artifact Id = logger`
- `Dry Run? = true`
- `Apply Changes? = false`

Esperado:

```text
Resultado.success = true
Resultado.data.install_plan.side_effects_enabled = false
Resultado.data.apply.should_apply = false
Resultado.data.apply.applied = false
Resultado.data.apply.verified = false
Resultado.data.apply.executor = json_config_manager
Resultado.data.jcm_apply_plan.operations = [] ou plano não executável
```

Nenhum arquivo deve ser criado pelo Artifact Manager.

## Teste 2 — Plano de apply via JCM

Entradas principais:

- `Operation = install_local_artifact`
- `Artifact Type = capability`
- `Artifact Id = logger`
- `Dry Run? = false`
- `Apply Changes? = true`
- `Manifest Json` válido.
- `Contract Json` válido quando aplicável.
- `Config Json` válido quando aplicável.

Esperado:

```text
Resultado.success = true
Resultado.data.apply.should_apply = true
Resultado.data.apply.applied = false
Resultado.data.apply.verified = false
Resultado.data.apply.executor = json_config_manager
Resultado.data.jcm_apply_plan.executor = json_config_manager
Resultado.data.jcm_apply_plan.operations contém ensure_folder/write_json/merge_json
Resultado.data.jcm_verification_plan.operations contém read_json/exists
```

Observação: o AM não deve criar arquivos diretamente neste teste. O próximo passo do orquestrador/Manager é executar `jcm_apply_plan` chamando `[CDXMS] Json Config Manager`.

## Teste 3 — Execução do plano via JCM

Execute cada operação de `Resultado.data.jcm_apply_plan.operations` usando `[CDXMS] Json Config Manager`.

Arquivos esperados sob o `Target Root Path` de homologação:

```text
capabilities/<artifact_id>/manifest.json
capabilities/<artifact_id>/contract.json
capabilities/<artifact_id>/config.json
core/registry.json
runtime/capabilities/<artifact_id>.state.json
packages/installed/capabilities/<artifact_id>/install_manifest.json
```

Depois execute as operações de `Resultado.data.jcm_verification_plan.operations`.

Esperado nos resultados JCM:

```text
Tmp_JCM_ReadAppliedManifest.success = Verdadeiro
Tmp_JCM_ReadAppliedRegistry.success = Verdadeiro
```

## Teste 4 — Bloqueio de falso sucesso

Repita o Teste 2 sem executar o plano JCM.

Esperado:

```text
Resultado.data.apply.should_apply = true
Resultado.data.apply.applied = false
Resultado.data.apply.verified = false
```

O Artifact Manager não pode retornar sucesso físico sem verificação pós-escrita.

## Teste 5 — Shell proibido

Audite o export `.ablock`.

Esperado:

```text
Nenhuma Action com m_classType = ShellScriptAction
Nenhum campo side_effects_delegated_to_shell
Nenhuma mensagem indicando que Shell é executor normal do AM
```
