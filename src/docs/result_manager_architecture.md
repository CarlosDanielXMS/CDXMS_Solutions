# Result Manager Architecture

O Result Manager é uma capability pura do núcleo CDXMS.

Ele existe para impedir que cada capability monte seu próprio `Resultado` de forma divergente.

## Decisões

1. Não depende de GitHub/CDN.
2. Não depende do JCM.
3. Não grava arquivos.
4. Não altera variáveis globais.
5. Não registra logs. Logging pertence à capability Logger.
6. Publica apenas `Resultado`.
7. Garante que dados úteis fiquem sempre em `Resultado.data`.

## Uso esperado

Capabilities simples podem montar `Resultado` diretamente.

Capabilities maiores podem chamar `[CDXMS] Registrar Resultado` para padronizar, validar ou propagar retornos.

## Relação com Logger

O Logger, que virá depois, poderá consumir `Resultado` já normalizado. O Result Manager não grava log por conta própria.
