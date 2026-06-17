# CDXMS Artifact Manager — Arquitetura v1.0.0

O Artifact Manager é a capability responsável pela camada local de lifecycle de artifacts. Ele não resolve dependências complexas e não baixa conteúdo remoto nesta versão. Essas responsabilidades pertencem às próximas capabilities/camadas: Dependency Resolver e GitHub Distribution Layer.

## Responsabilidades

- Validar manifest de artifact.
- Calcular paths locais.
- Construir entrada de registry.
- Gerar plano de instalação/registro/desregistro.
- Preservar config do usuário por padrão.

## Fora do escopo

- Download remoto.
- Resolução completa de dependências.
- Importação automática de `.macro`/`.ablock` no MacroDroid.
- Interface visual.
