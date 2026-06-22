# Arquitetura — Java UI Framework v1.0.0

## Papel

Renderer declarativo da camada de apresentação. Recebe JUIF JSON e produz overlay, state e eventos. Não persiste dados e não conhece lifecycle de artifacts.

## Fluxo

```text
JUIF UI Json
→ escape seguro no Action Block
→ Java Action
→ parse de state/pages/shell
→ renderização
→ eventos estruturados
→ Resultado
```

## Shell compatível

`ui.shell` é opcional. Sem ele, o renderer preserva o layout legado. Com ele:

- `top_app_bar` e `tab_bar` ficam acima da área rolável;
- `navigation_rail` fica ao lado da área rolável;
- `bottom_navigation` fica abaixo da área rolável;
- `navigation_drawer` é exibido em camada sobreposta.

## Limites

- depende da permissão Android para overlays;
- não garante importação automática;
- não substitui UI nativa do MacroDroid em fluxos de recuperação crítica;
- precisa de homologação real após qualquer alteração no Java Action.
