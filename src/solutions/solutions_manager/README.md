# [CDXMS] Solutions Manager v1.0.0

Entrada única e permanente do ecossistema CDXMS Solutions.

## Decisão arquitetural

O artifact baixado da Template Store deve ser o próprio `[CDXMS] Solutions Manager`, não uma macro instaladora descartável. O motivo é uma limitação concreta da plataforma: o MacroDroid consegue baixar arquivos, mas não oferece uma ação nativa geral para importar automaticamente um `.macro` ou `.ablock` recém-baixado.

Por isso, o modelo correto é:

```text
uma importação pelo usuário
  -> Solutions Manager com Action Blocks incorporados
  -> primeira execução inicializa o core local
  -> execuções seguintes abrem o gerenciador
```

O GitHub permanece como fonte oficial do plano de controle, manifests, catálogos, configs, checksums e payloads de release. Exports MacroDroid são distribuídos pela Template Store ou por importação manual guiada.

## Estado executável atual

- export `.macro` presente;
- 11 Action Blocks incorporados, suficientes para dispositivo vazio;
- Bootstrap executado antes da UI;
- Builder e renderer protegidos por resultado de sucesso;
- interface JUIF completa incorporada ao export;
- Intent bridge funcional com broadcast explícito, validação de protocolo e deduplicação;
- download validado da Solution de Teste implementado, com importação manual guiada;
- lifecycle de instalação, atualização, reparo e remoção ainda bloqueado;
- homologação final em dispositivo limpo obrigatória.

## Garantias

- nenhuma dependência CDXMS pré-instalada na primeira importação;
- nenhuma gravação direta de filesystem pela macro orquestradora;
- nenhum uso de Shell como transporte HTTP ou instalador;
- nenhuma declaração de instalação antes de verificação pós-escrita;
- nenhuma suposição de importação automática de exports MacroDroid.

## Reconstrução reproduzível

Depois de alterar qualquer capability incorporada, execute:

```bash
python src/solutions/solutions_manager/scripts/build_solutions_manager_export.py
python src/solutions/solutions_manager/scripts/validate_solutions_manager_foundation.py
```

O primeiro script recompõe a closure incorporada e o fluxo inicial do export; o segundo rejeita GUIDs, dependências, ações, variáveis ou contratos divergentes.

## Próximo gate

1. Importar o `.macro` em dispositivo limpo com MacroDroid 5.67.x ou superior.
2. Confirmar a criação do core e runtime.
3. Homologar visualmente a abertura e fechamento da UI.
4. Acionar `Baixar solution de teste` e confirmar o arquivo em staging.
5. Importar manualmente o export baixado e executar a Solution de Teste.
