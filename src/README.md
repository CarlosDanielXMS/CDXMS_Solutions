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

## UI antes do Solutions Manager

O Java UI Framework e o JUIF UI Builder foram adaptados ao contrato CDXMS sem remover as definições do protótipo. O catálogo passou de 26 para 36 componentes e ganhou shell persistente opcional.

Essas duas capabilities estão `ready_for_homologation`; ainda não devem ser marcadas como homologadas antes do teste real no MacroDroid.

## Arquitetura de entrada única

`[CDXMS] Solutions Manager` será a única macro permanente importada pelo usuário. O export incorporará o runtime mínimo por `exportedActionBlocks`.

```text
primeira execução -> bootstrap local offline
execuções seguintes -> manager
```

Não existe Installer separado na v1. Importação automática de `.macro`/`.ablock` continua não presumida.
