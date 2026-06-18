# Corpo — [CDXMS] Artifact Manager v1.0.0

## Entradas

- `Operation`: operação técnica.
- `Artifact Type`: tipo do artifact.
- `Artifact Id`: id técnico.
- `Manifest Json`: manifest do artifact.
- `Contract Json`: contrato opcional.
- `Config Json`: configuração/default opcional.
- `Registry Json`: registry atual usado para merge seguro.
- `Package Manifest Json`: manifest de package/local bundle quando aplicável.
- `Dependency Resolution Json`: resultado/plano produzido pelo Dependency Resolver.
- `Local Package Path`: origem local opcional.
- `Target Root Path`: raiz CDXMS de destino.
- `Preserve User Config?`: preserva config existente.
- `Dry Run?`: quando verdadeiro, retorna apenas plano.
- `Apply Changes?`: segundo gate para permitir apply físico via JCM quando `Dry Run?` for falso.
- `Strict Mode?`: validação rigorosa.
- `Session Id` / `Correlation Id`: rastreabilidade.

## Saída

- `Resultado`: dicionário CDXMS único.

## Variáveis de trabalho

- `Tmp_ArtifactWorkJson`: JSON textual gerado pelo motor interno do Artifact Manager.
- `Tmp_ArtifactWork`: dicionário intermediário após parse, quando necessário para inspeção/debug.

## Responsabilidade

O Artifact Manager **não cria diretórios nem escreve arquivos diretamente**.

A responsabilidade física é do `[CDXMS] Json Config Manager`.

```text
Artifact Manager = lifecycle, plano, validação, registro lógico e verificação
Json Config Manager = filesystem/JSON executor
Dependency Resolver = dependências sem side effects
```

## Corpo

1. **Action Group — Processar Artifact**
   - Agrupa a execução da capability.

2. **JavaScriptAction — Motor interno de lifecycle**
   - Lê as entradas.
   - Interpreta booleanos localizados (`true`, `false`, `Verdadeiro`, `Falso`, `sim`, `não`).
   - Valida `Operation`.
   - Valida `Artifact Type` e `Artifact Id` quando exigidos.
   - Valida e resume `Manifest Json`, `Contract Json`, `Config Json`, `Package Manifest Json` e `Dependency Resolution Json` quando informados.
   - Calcula paths locais.
   - Gera `registry_entry`.
   - Consome `Dependency Resolution Json` quando informado.
   - Monta `install_plan`.
   - Define `apply.should_apply` somente se:
     - operação for elegível;
     - `Dry Run? = false`;
     - `Apply Changes? = true`;
     - não houver bloqueio de dependência;
     - entradas mínimas estiverem válidas.
   - Define `apply.executor = json_config_manager`.
   - Gera `jcm_apply_plan` com operações genéricas do JCM.
   - Gera `jcm_verification_plan` com leituras/verificações pós-escrita.
   - Bloqueia falso sucesso físico: enquanto resultados JCM de verificação não forem fornecidos/observados, `apply.applied` e `apply.verified` não devem ser marcados como verdadeiros.
   - Saída textual: `Tmp_ArtifactWorkJson`.

3. **Json Parse — Tmp_ArtifactWorkJson -> Resultado**
   - Publica a saída pública única.
   - O `Resultado.data.jcm_apply_plan` deve ser executado pelo fluxo orquestrador usando `[CDXMS] Json Config Manager`.
   - O `Resultado.data.jcm_verification_plan` deve ser executado depois do apply para confirmar manifest, registry e arquivos críticos.

4. **Action Group End**
   - Fecha o grupo.

5. **Exit Action Block**
   - Encerra explicitamente o bloco.

## Plano de execução física esperado pelo orquestrador/Manager

Quando `Resultado.data.apply.should_apply = true`, o orquestrador deve executar as operações de `Resultado.data.jcm_apply_plan.operations` chamando `[CDXMS] Json Config Manager`, uma a uma, com bloqueio de próximas ações.

Cada operação deve mapear:

```text
Operation       -> operação JCM
File Path       -> quando existir
Folder Path     -> quando existir
Json Path       -> quando existir
Value Json      -> quando existir
Default Json    -> quando existir
Merge Strategy  -> quando existir
Pretty Print?   -> quando existir
```

Depois disso, deve executar `Resultado.data.jcm_verification_plan.operations` e chamar novamente o AM com `Operation = verify_local_apply` quando houver payload de resultados de verificação consolidado.

## Critério de sucesso físico

O AM só pode ser considerado fisicamente aplicado quando:

```text
apply.should_apply = true
apply.applied = true
apply.verified = true
apply.executor = json_config_manager
```

Qualquer cenário sem verificação pós-escrita deve retornar `blocked`, `partial` ou `error`, nunca sucesso físico.
