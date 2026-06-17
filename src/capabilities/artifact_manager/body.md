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
- `Apply Changes?`: segundo gate para aplicar fisicamente quando `Dry Run?` for falso.
- `Strict Mode?`: validação rigorosa.
- `Session Id` / `Correlation Id`: rastreabilidade.

## Saída

- `Resultado`: dicionário CDXMS único.

## Variáveis de trabalho

- `Tmp_ArtifactWorkJson`: JSON textual gerado pelo motor interno.
- `Tmp_ArtifactWork`: dicionário intermediário usado pela aplicação shell controlada.

## Corpo

1. **Action Group — Processar Artifact**
   - Agrupa a execução da capability.

2. **JavaScriptAction — Motor interno**
   - Lê as entradas.
   - Interpreta booleanos localizados (`true`, `false`, `Verdadeiro`, `Falso`, `sim`, `não`).
   - Valida o manifest.
   - Calcula paths locais.
   - Gera registry entry.
   - Consome `Dependency Resolution Json` quando informado.
   - Monta `install_plan`.
   - Define `apply.should_apply` somente se a operação for elegível, `Dry Run? = false`, `Apply Changes? = true` e não houver bloqueio de dependência.
   - Gera `apply_payload` com JSONs de manifest, contract, config, registry, runtime state e install marker.
   - Saída textual: `Tmp_ArtifactWorkJson`.

3. **Json Parse — Tmp_ArtifactWorkJson -> Tmp_ArtifactWork**
   - Disponibiliza os campos gerados para o `ShellScriptAction`.

4. **Shell Script — Aplicação local controlada**
   - Non-root.
   - Executa apenas quando `Tmp_ArtifactWork[data][apply][should_apply]` for verdadeiro.
   - Cria diretórios de destino com `mkdir -p`.
   - Escreve `manifest.json`, `contract.json` e `config.json` quando aplicável.
   - Escreve `core/registry.json` quando a operação exige registry.
   - Escreve runtime state e install marker.
   - Não importa `.ablock`/`.macro` automaticamente.

5. **Json Parse — Tmp_ArtifactWorkJson -> Resultado**
   - Publica a saída pública única.

6. **Action Group End**
   - Fecha o grupo.

7. **Exit Action Block**
   - Encerra explicitamente o bloco.
