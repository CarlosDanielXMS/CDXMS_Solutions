# Arquitetura — CDXMS String Utils v1.0.0

A String Utils é uma capability pura do ecossistema CDXMS.

## Papel

Centralizar transformações textuais reutilizáveis para impedir duplicação em Artifact Manager, Dependency Resolver, GitHub Distribution Layer, JUIF UI Builder, MDF e demais solutions.

## Fora de escopo

- filesystem;
- GitHub/CDN;
- registry;
- instalação/update de artifacts;
- logging persistente;
- UI;
- leitura de tela/OCR.

## Dependência

A capability depende apenas de `result_manager >= 1.0.0` para finalizar a saída `Resultado`.

## Decisão de design

O processamento textual ocorre em uma etapa local e o contrato final é construído pelo Result Manager. Isso mantém o contrato uniforme e evita que a String Utils replique a lógica oficial de `Resultado`.
