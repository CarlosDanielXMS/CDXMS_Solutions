# CDXMS — Auditoria de Uso de Ações Nativas MacroDroid v1.0.0 Pré-Release

Esta auditoria substitui a leitura anterior que sugeria `v1.0.1`. Como ainda não houve release oficial, todos os ajustes permanecem dentro da versão `1.0.0`.

## Política atualizada

```text
Ações nativas primeiro quando expressarem a intenção com clareza, segurança e homologação real.
JavaScript quando houver regra composta, parse/merge complexo, JsonPath, escaping robusto ou redução significativa de complexidade.
Shell somente como último recurso, documentado e com alternativa nativa avaliada.
```

## Base atual analisada

| Capability | Action Block | Total de ações | Classes únicas | JS | Shell | FileOperation | TextManipulation |
|---|---|---:|---:|---:|---:|---:|---:|
| `json_config_manager` | `[CDXMS] Json Config Manager` | 119 | 12 | 25 | 4 | 0 | 0 |
| `bootstrap` | `[CDXMS] Bootstrap` | 107 | 10 | 9 | 0 | 0 | 0 |
| `result_manager` | `[CDXMS] Registrar Resultado` | 5 | 5 | 1 | 0 | 0 | 0 |
| `logger` | `[CDXMS] Logger` | 14 | 9 | 1 | 0 | 0 | 0 |
| `string_utils` | `[CDXMS] String Utils` | 8 | 6 | 1 | 0 | 0 | 0 |

## Conclusões

### JCM
JS permanece tecnicamente justificado por JsonPath Engine v1, merge profundo, escrita segura em nó específico, filtros, wildcard, slice e union. Shell permanece apenas como fallback controlado para criação recursiva e remoção idempotente enquanto `FileOperationV21Action`/`FileOperationAllFilesAction` não forem homologadas com path dinâmico em dispositivo real.

### Bootstrap
Foi mantido como fundação mínima dependente apenas do JCM. A dependência obrigatória do Result Manager não foi adicionada para não dificultar instalação limpa e recuperação do core.

### Result Manager
JavaScript permanece adequado, pois a capability é uma normalizadora de contrato.

### Logger
Uso híbrido adequado: JCM para estrutura, WriteToFileAction para persistência, Result Manager para saída, JS pontual para payload JSONL.

### String Utils
JavaScript permanece adequado nesta fase porque a capability centraliza várias operações e garante saída homogênea. `TextManipulationAction` deve ser usada diretamente em macros/capabilities futuras para transformações simples quando não houver necessidade de contrato multioperação.

## Plano antes de release oficial

1. Importar todos os `.ablock` no MacroDroid real.
2. Executar testes manuais por operação principal.
3. Validar comportamento do JCM em dispositivo limpo.
4. Testar `FileOperationV21Action` e `FileOperationAllFilesAction` isoladamente antes de substituir Shell.
5. Congelar a versão `1.0.0` somente após validação manual.
