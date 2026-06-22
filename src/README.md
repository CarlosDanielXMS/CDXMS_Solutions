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
- `[CDXMS] File Integrity`.

## Homologações concluídas

- RSM control-plane: `23/23`;
- SHA-256 runtime: `7/7`;
- File Integrity: `11/11`.

## Arquitetura de entrada única

`[CDXMS] Solutions Manager` será a única macro permanente importada pelo usuário. O export incorporará o runtime mínimo por `exportedActionBlocks`.

```text
primeira execução -> bootstrap local offline
execuções seguintes -> manager
```

Não existe Installer separado na v1. Importação automática de `.macro`/`.ablock` continua não presumida.

## Estado atual

- Solutions Manager ainda não foi criado;
- catálogo continua sem solutions publicadas;
- prova mínima de Bootstrap + JCM incorporados está pronta para homologação;
- integração de payload verificado fica após a homologação da entrada única.
