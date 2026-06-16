# CDXMS — Saneamento Pré-Release das Capabilities v1.0.0

Este documento registra os ajustes realizados nas capabilities atuais sem alteração de versão pública. Todas continuam em `1.0.0`, pois ainda não houve release oficial para usuários finais.

## Regra aplicada

```text
Antes da primeira release/tag oficial, ajustes estruturais, revisão de ações internas, documentação, checksums e refinamentos de export continuam pertencendo à v1.0.0.
```

## Capabilities analisadas

| Capability | Action Block | Ações | Classes únicas | JS | Shell | FileOperation | TextManipulation |
|---|---|---:|---:|---:|---:|---:|---:|
| `json_config_manager` | `[CDXMS] Json Config Manager` | 119 | 12 | 25 | 4 | 0 | 0 |
| `bootstrap` | `[CDXMS] Bootstrap` | 107 | 10 | 9 | 0 | 0 | 0 |
| `result_manager` | `[CDXMS] Registrar Resultado` | 5 | 5 | 1 | 0 | 0 | 0 |
| `logger` | `[CDXMS] Logger` | 14 | 9 | 1 | 0 | 0 | 0 |
| `string_utils` | `[CDXMS] String Utils` | 8 | 6 | 1 | 0 | 0 | 0 |

## Decisões por capability

### `json_config_manager`

- Versão mantida: `1.0.0`.
- Action Block: `[CDXMS] Json Config Manager`.
- JS: `25`.
- Shell: `4`.
- Decisão: Mantém ações nativas de leitura/escrita/parse onde elas já expressam a intenção; mantém JavaScript como engine interna de JsonPath/merge; mantém ShellScriptAction como fallback controlado para mkdir -p e rm -f até homologação real de FileOperationV21Action/FileOperationAllFilesAction com paths dinâmicos e criação recursiva.
- Próximo teste recomendado: Criar teste mínimo real no MacroDroid para FileOperationV21Action com m_folderName dinâmico e FileOperationAllFilesAction delete por all-files path antes de substituir o Shell.

### `bootstrap`

- Versão mantida: `1.0.0`.
- Action Block: `[CDXMS] Bootstrap`.
- JS: `9`.
- Shell: `0`.
- Decisão: Mantém o Bootstrap minimalista, com dependência direta apenas do JCM. Não foi adicionada dependência obrigatória do Result Manager para não fragilizar a inicialização limpa do core.
- Próximo teste recomendado: A partir do Artifact Manager, usar Result Manager nas novas capabilities; Bootstrap pode continuar publicando Resultado próprio enquanto for bloco de fundação.

### `result_manager`

- Versão mantida: `1.0.0`.
- Action Block: `[CDXMS] Registrar Resultado`.
- JS: `1`.
- Shell: `0`.
- Decisão: Mantém JavaScript por ser fábrica/normalizadora de Resultado. Reescrever em ações visuais aumentaria ações e risco sem ganho.
- Próximo teste recomendado: Sem ajuste funcional necessário antes da release 1.0.0.

### `logger`

- Versão mantida: `1.0.0`.
- Action Block: `[CDXMS] Logger`.
- JS: `1`.
- Shell: `0`.
- Decisão: Mantém JCM para garantia de estrutura, WriteToFileAction para persistência e Result Manager para publicação; JavaScript fica restrito à montagem da linha JSONL e validação do payload.
- Próximo teste recomendado: Validar append JSONL em dispositivo limpo e permissões all-files/SAF.

### `string_utils`

- Versão mantida: `1.0.0`.
- Action Block: `[CDXMS] String Utils`.
- JS: `1`.
- Shell: `0`.
- Decisão: Mantém JavaScript centralizado porque o Action Block precisa suportar 17 operações por Operation e retornar Resultado homogêneo. TextManipulationAction será preferida em fluxos externos simples, mas dentro desta capability o script reduz duplicação e edge cases.
- Próximo teste recomendado: Se a UI do MacroDroid confirmar TextManipulationAction com trim/case/regex adequados, criar teste comparativo antes de trocar branches específicos.

## Resultado do saneamento

- Nenhuma capability recebeu version bump.
- Todos os manifests declaram `implementation_audit.stage = pre_release_1_0_0_sanitization`.
- O catálogo de ações nativas foi incorporado em `docs/macro_droid_action_catalog_v0_1.md` e `.json`.
- O pacote inclui validação automatizada de estrutura e consistência de versão.
- Shell permanece apenas no JCM como fallback controlado e explicitamente documentado.

## Critério para trocar Shell por FileOperation

A troca só deve ocorrer após teste real no MacroDroid confirmando:

1. criação recursiva de pasta equivalente a `mkdir -p`;
2. delete idempotente equivalente a `rm -f`;
3. suporte confiável a caminho dinâmico por Magic Text;
4. preservação de permissões em dispositivo limpo;
5. retorno/espera compatível com `waitToComplete` ou equivalente.

Até esse teste, a troca manual no export seria mais arriscada que manter o fallback controlado.
