# CDXMS — Ecosystem Core Base v1.0.0

Base completa do ecossistema CDXMS Solutions.

## Capabilities incluídas

- `[CDXMS] Json Config Manager`;
- `[CDXMS] Bootstrap`;
- `[CDXMS] Registrar Resultado`;
- `[CDXMS] Logger`;
- `[CDXMS] String Utils`;
- `[CDXMS] Artifact Manager`;
- `[CDXMS] Dependency Resolver`;
- `[CDXMS] Remote Source Manager`;
- `[CDXMS] File Integrity`;
- `[CDXMS] Java UI Framework`;
- `[CDXMS] JUIF UI Builder`.

## Homologações concluídas

- RSM control-plane: `23/23`;
- SHA-256 runtime: `7/7`;
- File Integrity: `11/11`.

## UI e Solutions Manager

O Java UI Framework e o JUIF UI Builder foram adaptados ao contrato CDXMS sem remover as definições do protótipo. O catálogo passou de 26 para 36 componentes e ganhou shell persistente com hosts independentes para navegação e conteúdo.

Essas duas capabilities estão `professionally_redesigned_ready_for_device_homologation`; ainda não devem ser marcadas como homologadas antes do teste real no MacroDroid.

## Arquitetura de entrada única

`[CDXMS] Solutions Manager` é a única macro permanente importada pelo usuário. O export incorpora as 11 capabilities v1 por `exportedActionBlocks` e executa Bootstrap antes de renderizar a UI.

```text
primeira execução -> bootstrap local offline
execuções seguintes -> manager
```

Não existe Installer separado na v1. Exports executáveis continuam exigindo Template Store ou importação manual guiada; GitHub é o plano de controle e a fonte de payloads verificados.


## UI — correção pré-homologação

O Java UI Framework e o JUIF UI Builder publicam o contrato universal sem campos legados. A homologação visual/interativa no MacroDroid ainda é gate obrigatório antes do Solutions Manager.


## UI — redesign profissional

A UI padrão agora é a documentação canônica do JUIF. Ela possui sete páginas, uma única Tab Bar contextual, Bottom Navigation fixa, drawer completo e catálogo sem duplicação de estado. O Java Action foi validado sintaticamente com parser BeanShell, mas a homologação visual em dispositivo permanece obrigatória.
- Hotfix aplicado: navegação do catálogo usa despacho adiado, renderização transacional e erro visível em runtime.

## Estado operacional

- entrada limpa: estruturalmente preparada, aguardando homologação no dispositivo;
- event bridge: recepção/validação implementada, despacho de negócio pendente;
- lifecycle mutável: desabilitado;
- distribuição oficial: somente após ref imutável e quality gate completo.
