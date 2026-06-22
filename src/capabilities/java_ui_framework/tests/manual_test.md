# Teste manual — Java UI Framework v1.0.0

## Pré-condições

- permissão de exibição sobre outros apps concedida;
- Action Block importado no MacroDroid.

## Regressão dos componentes existentes

1. Renderizar todos os 26 componentes do protótipo.
2. Confirmar inputs, state, eventos, navegação e fechamento.
3. Confirmar fallback quando `JUIF UI Json` estiver vazio.
4. Confirmar erro estruturado para JSON inválido.

## Novos componentes

5. `top_app_bar`: back, drawer e ação customizada.
6. `bottom_navigation`: seleção e troca de página.
7. `navigation_rail`: seleção lateral e troca de página.
8. `navigation_drawer`: abrir, fechar pelo scrim e selecionar item.
9. `tab_bar`: seleção e evento.
10. `search_bar`: `search_changed` e `search_submitted`.
11. `chip`: alternância booleana.
12. `chip_group`: single e multiple.
13. `empty_state`: renderização e botão opcional.
14. `loading_indicator`: renderização indeterminada.

## Shell

15. Shell vazio mantém layout legado.
16. Top bar e bottom navigation ficam fora do scroll.
17. Rail permanece ao lado da área rolável.
18. Drawer fica acima do conteúdo e fecha sem remover o overlay principal.
19. Navegação atualiza `Tmp_JuifCurrentPage` e state.
20. Apenas `Resultado` aparece como saída pública.

## Aceite

A homologação deve registrar modelo Android, versão do MacroDroid e resultado por caso.
