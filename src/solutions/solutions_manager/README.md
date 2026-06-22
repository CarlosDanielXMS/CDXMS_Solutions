# [CDXMS] Solutions Manager v1.0.0

Solution permanente e entrada única do ecossistema CDXMS Solutions.

## Decisão arquitetural

O usuário importa somente `[CDXMS] Solutions Manager`.

- Na primeira execução, a própria macro atua como bootstrapper offline usando Action Blocks incorporados.
- Nas execuções seguintes, ela valida o ambiente e abre o gerenciador.
- Não existe Installer separado na v1.
- Copiar `.macro`/`.ablock` para o filesystem não equivale a importá-los no MacroDroid.

## Responsabilidade

O Solutions Manager coordena capabilities; ele não reimplementa seus domínios.

| Responsabilidade | Capability proprietária |
|---|---|
| Core, JSON e filesystem | Json Config Manager |
| Inicialização local | Bootstrap |
| Resultado universal | Result Manager |
| Logs | Logger |
| Strings | String Utils |
| Lifecycle de artifact | Artifact Manager |
| Dependências | Dependency Resolver |
| Fontes remotas e staging | Remote Source Manager |
| SHA-256 e integridade | File Integrity |
| Montagem de UI | JUIF UI Builder |
| Renderização de UI | Java UI Framework |

## Estado deste incremento

Este incremento entrega a fundação canônica:

- manifest da solution;
- contrato de operações;
- configuração default;
- máquina de estados;
- mapa de orquestração;
- schema JUIF de produção;
- corpo detalhado planejado;
- testes e validador de fundação.

O export MacroDroid ainda não está incluído. A implementação começa somente após fechar o event bridge entre a UI Java e o fluxo MacroDroid.

## Gate crítico: event bridge

A UI atual consegue navegar internamente. Entretanto, ações de negócio como instalar ou atualizar precisam retornar `action`, `payload`, `current_page` e `state` para a macro. Working variables internas do Action Block não podem ser assumidas como canal válido depois que a chamada termina.

Por isso, lifecycle mutável permanece desabilitado até que esse bridge seja implementado e homologado.
