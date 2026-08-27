# CDXMS Solutions

Ecossistema modular de solutions e capabilities para MacroDroid.

Esta consolidação fecha a arquitetura de entrada única, incorpora o runtime inicial ao `[CDXMS] Solutions Manager` e endurece o gate de distribuição.

## Estado

- base remota consultada: `feat/solutions-manager@95e23dd`;
- Remote Source Manager, plano de controle: homologado `23/23`;
- SHA-256 runtime: homologado `7/7`;
- File Integrity de produção: homologado `11/11`;
- Java UI Framework v1.0.0: redesign profissional preparado para homologação;
- JUIF UI Builder v1.0.0: preparado para homologação;
- Solutions Manager: export estrutural com Bootstrap, event receiver e 11 Action Blocks incorporados; homologação em dispositivo limpo pendente;
- lifecycle remoto mutável: bloqueado até payload verificado, despacho e homologação end-to-end.

## Capabilities de UI

- `[CDXMS] Java UI Framework` — renderer JUIF com 36 componentes e shell persistente em hosts independentes;
- `[CDXMS] JUIF UI Builder` — normalizador de schema, bindings, state, mapping e shell.

Os 26 componentes do protótipo foram preservados. Foram adicionados componentes de navegação, busca, filtros e estados vazios/carregamento.

## Decisão de entrada

O usuário importará apenas `[CDXMS] Solutions Manager`. Na primeira execução, a macro atuará como bootstrapper; nas seguintes, como manager. Não haverá Installer separado na v1, pois download de `.macro`/`.ablock` não equivale a importação no MacroDroid.

## Validação estática

```bash
python src/scripts/validate_ui_capabilities_v1_0_0.py
python src/capabilities/bootstrap/scripts/validate_bootstrap_incremental.py
python src/capabilities/file_integrity/scripts/validate_file_integrity_incremental.py
python src/scripts/validate_remote_distribution_readiness_v1_0_0.py
python src/solutions/solutions_manager/scripts/validate_solutions_manager_foundation.py
```


## Correção aplicada

As capabilities de UI foram corrigidas para seguir `core/result_contract.json`; a hierarquia-base do renderer do protótipo foi restaurada e os validadores agora rejeitam campos legados proibidos.


## Redesign profissional da UI

O shell do Java UI Framework foi reorganizado para manter Top App Bar, Tab Bar, Navigation Rail, Bottom Navigation e Navigation Drawer fora do conteúdo rolável. Os dez componentes novos foram alinhados ao sistema visual dark gold e a documentação padrão passou a usar uma única navegação de catálogo, com sete páginas e cobertura integral dos 36 componentes.
- Hotfix aplicado: navegação do catálogo usa despacho adiado, renderização transacional e erro visível em runtime.

## Distribuição

- GitHub raw/release: manifests, catálogos, configs, checksums e payloads de filesystem;
- Template Store ou importação manual: exports executáveis `.macro`/`.ablock`;
- produção: ref imutável por tag ou commit; `develop` permanece exclusivo da pré-release.
