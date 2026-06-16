# CDXMS Solutions — Ecosystem Core

Raiz distribuível do ecossistema CDXMS Solutions para MacroDroid.

Esta pasta `src/` é usada apenas no repositório. No dispositivo do usuário, a estrutura final não deve conter `src/`.

## Capabilities estruturais atuais

```text
capabilities/json_config_manager/
capabilities/bootstrap/
```

## JCM

`[CDXMS] Json Config Manager` é o kernel primitivo de JSON/filesystem.

Responsabilidades:

- core mínimo local;
- leitura/escrita/merge de JSON;
- JCM JsonPath Engine v1;
- saída pública única `Resultado`;
- dados úteis em `Resultado.data`.

## Bootstrap

`[CDXMS] Bootstrap` coordena a inicialização local do ecossistema sobre o JCM.

Responsabilidades:

- verificar core;
- reparar core quando autorizado;
- preparar runtime;
- carregar contexto completo para reduzir chamadas repetidas ao JCM;
- retornar status local.

Bootstrap não baixa da CDN, não instala artifacts remotos e não registra artifacts. Essas responsabilidades pertencem às próximas capabilities.

## Regra de distribuição

Remote manifests devem usar:

```text
base_raw_url = https://raw.githubusercontent.com/CarlosDanielXMS/CDXMS_Solutions/<ref>/src
```

E os `target_path` devem permanecer sem `src/`.
