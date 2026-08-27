# [CDXMS] Test Solution v1.0.0

Solution genérica de homologação do fluxo inicial do ecossistema CDXMS Solutions.

## Objetivo

- executar o `[CDXMS] Bootstrap` em dispositivo já preparado pela macro inicial;
- construir um contrato visual pelo `[CDXMS] JUIF UI Builder`;
- renderizar a interface pelo `[CDXMS] Java UI Framework`;
- comprovar que o export distribuído pelo Solutions Manager pode ser importado e executado;
- não executar operações destrutivas nem alterar configurações do usuário.

## Distribuição

O Solutions Manager baixa o arquivo:

```text
solutions/test_solution/macrodroid/[CDXMS]_Test_Solution.macro
```

para a área de staging validada dentro de `Documents/CDXMS_Solutions`. A importação no MacroDroid permanece manual e orientada nesta etapa.

## Resultado esperado

Ao executar a macro importada, o usuário deve visualizar uma interface JUIF com estado do Bootstrap, componentes de identidade visual, informações da solution e navegação interna.

## Reconstrução e validação

```bash
python src/solutions/solutions_manager/scripts/build_solutions_manager_export.py
python src/solutions/test_solution/scripts/build_test_solution_export.py
python src/solutions/test_solution/validate_test_solution.py
```
