# Corpo planejado — [CDXMS] Solutions Manager v1.0.0

## Entradas

- `Sm_RequestedOperation`: operação inicial, default `launch`.
- `Sm_RequestedArtifactType`: tipo do artifact selecionado.
- `Sm_RequestedArtifactId`: id técnico selecionado.
- `Sm_RequestedPayloadJson`: payload contextual.
- `Sm_AllowNetwork?`: permite atualização de documentos remotos.
- `Sm_ForceRefresh?`: força atualização do catálogo.
- `Sm_DryRun?`: mantém lifecycle em planejamento.

## Saída

- `Resultado` — dicionário único no contrato universal CDXMS.

## Variáveis de trabalho

Usar exclusivamente as variáveis `Tmp_Sm*` descritas em `contract.json`.

## Corpo — primeiro incremento vertical

### 01 — Inicializar sessão

1. Definir `Tmp_SmState = starting`.
2. Gerar `Tmp_SmSessionId` e `Tmp_SmCorrelationId`.
3. Definir `Tmp_SmLoopContinue = true`.
4. Normalizar operação vazia para `launch`.

### 02 — Verificar ambiente

1. Executar `[CDXMS] Bootstrap` com `Operation = get_status` e aguardar conclusão.
2. Salvar a saída em `Tmp_SmBootstrapResult`.
3. Direcionar o fluxo:
   - ausente → `bootstrapping`;
   - parcial/inválido → `repairing`;
   - pronto → `loading_context`.

### 03 — Bootstrap ou reparo

1. Ambiente ausente: Bootstrap `initialize_ecosystem`, com `Load Context? = true`.
2. Ambiente parcial: Bootstrap `repair_core`, seguido de `load_context`.
3. Em falha, propagar o resultado por `[CDXMS] Registrar Resultado` e encerrar.

### 04 — Carregar contexto

1. Extrair registry e settings do resultado do Bootstrap.
2. Preencher `Tmp_SmRegistryJson` e `Tmp_SmSettingsJson`.
3. Não repetir leituras que já estejam presentes no contexto.

### 05 — Validar ecossistema

1. Bootstrap `verify_core`.
2. RSM `get_source_status`.
3. Consolidar checks sem duplicar as regras internas das capabilities.
4. Construir o modelo de diagnóstico.

### 06 — Carregar catálogo

1. Ler cache local válido por meio do JCM.
2. Quando permitido, chamar RSM `fetch_catalog` e `fetch_release_manifest`.
3. Validar staging com File Integrity.
4. Relê-lo com JCM antes do uso.
5. Em falha remota com cache válido, operar em `degraded_read_only`.

### 07 — Construir e renderizar UI

1. Montar `Tmp_SmUiConfigJson`.
2. Carregar `ui_schema.default.json`.
3. Executar `[CDXMS] JUIF UI Builder` com `Escape Json = false`.
4. Extrair `data.juif_ui_json` para `Tmp_SmUiJson`.
5. Executar `[CDXMS] Java UI Framework`.

### 08 — Event bridge

Somente após homologação:

1. observar eventos da sessão atual;
2. rejeitar evento duplicado ou consumido;
3. copiar `action`, `payload`, `current_page` e `state`;
4. marcar evento como consumido;
5. mapear a ação para uma operação do Manager;
6. executar a operação e atualizar a UI.

### 09 — Encerramento

1. Encerrar o overlay ao receber `close`.
2. Publicar `Resultado` da sessão.
3. Limpar somente runtime efêmero.
4. Manter a macro instalada como entrada permanente.

## Restrições

- Não usar Shell como executor normal.
- Não escrever arquivos diretamente na macro.
- Não considerar cópia de `.macro`/`.ablock` como importação.
- Não habilitar lifecycle mutável antes do event bridge e do pipeline de payload verificado.
