# [CDXMS] File Integrity v1.0.0

Capability homologada para calcular e verificar SHA-256 de arquivos locais dentro do escopo seguro do CDXMS.

## Estado

- executor runtime homologado: `/system/bin/sha256sum`;
- contexto homologado: non-root, sem MacroDroid Helper e sem Shizuku;
- probe de executor: `[CDXMS] Homologar SHA-256 Runtime v1.0.1 TEMP` — `7/7`;
- homologação da capability de produção: `[CDXMS] Homologar File Integrity v1.0.0 TEMP` — `11/11`;
- concluída em `2026-06-21`;
- alteração indevida de registry: nenhuma.

## Responsabilidade

- validar a operação e o caminho;
- calcular SHA-256 com executor fixo e homologado;
- validar a saída como 64 caracteres hexadecimais;
- comparar o digest esperado em `verify_sha256`;
- retornar `Resultado` universal;
- nunca baixar, instalar, aplicar ou registrar artifacts.

## Operações

- `calculate_sha256`;
- `verify_sha256`.

## Dependência

- `[CDXMS] Json Config Manager` para preparar e remover o relatório efêmero usado como bridge de saída da ação Shell Script.

## Segurança

- somente paths absolutos iniciados por `/storage/emulated/0/Documents/CDXMS_Solutions/`;
- traversal e caracteres de shell são rejeitados antes da execução;
- o comando é fixo: `/system/bin/sha256sum FILE`;
- nenhum comando é recebido por entrada;
- o path validado é colocado entre aspas;
- o relatório temporário é removido pelo JCM após a leitura.

## Saída principal

`Resultado.data` informa algoritmo, executor, contexto runtime, caminho, hash esperado, hash calculado, correspondência, estado de verificação e limpeza do relatório.

## Limites

A capability não faz HTTP, não interpreta remote manifests, não instala arquivos, não altera registry e não importa `.macro` ou `.ablock`.
