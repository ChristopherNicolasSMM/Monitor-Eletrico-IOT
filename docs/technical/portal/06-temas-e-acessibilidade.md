# Temas e padrão visual do Portal Técnico — v0.1.2

**Estado:** IMPLEMENTADO no código da branch `feature/portal-tecnico-mvp`; validação visual manual em navegadores ainda pendente.  
**Público:** equipe de desenvolvimento e avaliadores de usabilidade.  
**Escopo:** somente interface técnica. PDF cliente e PDF técnico continuam sendo perfis de saída, sem segundo portal.

## Diretriz de design

A marca aprovada permanece: grafite, azul técnico, verde-água e âmbar. A aplicação passa a oferecer três preferências: **Claro**, **Escuro** e **Sistema**. O tema escuro não utiliza preto puro: utiliza azul-grafite intermediário, superfícies elevadas diferenciadas, bordas suaves e textos claros. O tema claro mantém cartões brancos em fundo cinza-azulado.

## Tokens canônicos

Todos os componentes de interface devem receber cores de variáveis semânticas em `portal/static/style.css`. Evitar valores hexadecimais diretamente em novos painéis.

| Token | Claro | Escuro | Papel |
|---|---|---|---|
| `--page` | `#F2F5F7` | `#263846` | Fundo geral |
| `--surface` | `#FFFFFF` | `#324654` | Cartões e painéis |
| `--surface-alt` | `#F7FAFB` | `#2C4050` | Tabelas e detalhes |
| `--sidebar` | `#1C3445` | `#253B4C` | Navegação |
| `--text` | `#203443` | `#E0EAF0` | Texto de leitura |
| `--muted` | `#526876` | `#C4D5DE` | Texto secundário |
| `--teal` | `#087A74` | `#75E0D0` | Ações e destaques |
| `--warning-bg` | `#FFF4DC` | `#594E39` | Avisos, dados simulados |
| `--plot-bg` | `#FFFFFF` | `#324654` | Plotly |
| `--plot-grid` | `#E4ECEF` | `#4B6270` | Linhas auxiliares |

As cores da marca aprovadas não mudaram; as cores de superfície derivam delas para leitura confortável em ambos os modos.

## Funcionamento

1. Sem preferência salva, a aparência segue a configuração `prefers-color-scheme` do sistema operacional.
2. Quando o usuário escolhe Claro ou Escuro, o tema é aplicado sem recarregar a página e a escolha fica salva em `localStorage` sob `monitor-theme`.
3. Ao escolher Sistema, o site passa a acompanhar mudanças futuras do sistema; a opção também é persistida.
4. Se o navegador bloquear armazenamento, a alternância ainda funciona durante a sessão.
5. Pequeno script no `<head>` aplica o tema antes do CSS para evitar flash inicial de modo incorreto.
6. Os botões usam `aria-pressed` e navegação por teclado; `color-scheme` adapta controles nativos.
7. O gráfico Plotly usa os mesmos tokens da página. Ao alternar, mudam grade, fundo, fontes e cores das curvas, preservando o zoom já selecionado.
8. Em telas pequenas, o seletor aparece abaixo da navegação horizontal. O layout respeita `prefers-reduced-motion`.

## Acessibilidade e verificação

Contrastes calculados a partir dos valores publicados: texto padrão no cartão escuro ≈ 8,0:1; texto secundário no cartão escuro ≈ 6,5:1; texto do menu escuro ≈ 10,6:1; aviso escuro ≈ 6,7:1. Esses cálculos não substituem auditoria visual real em navegador, incluindo foco, elementos nativos e zoom.

## Casos de teste UX

| ID | Cenário | Esperado |
|---|---|---|
| UX-THEME-01 | Selecionar Escuro | Todos os painéis, tabelas, botões e gráfico ficam legíveis |
| UX-THEME-02 | Selecionar Claro | Cores claras reaparecem, sem refresh |
| UX-THEME-03 | Recarregar com Escuro | Preferência anterior permanece |
| UX-THEME-04 | Selecionar Sistema, alterar aparência do SO | UI acompanha o SO |
| UX-THEME-05 | Alterar tema com gráfico ampliado | Cores do gráfico mudam sem perder zoom |
| UX-THEME-06 | Navegar usando Tab/Enter/Espaço | Seletor operável e botão ativo anunciado |
| UX-THEME-07 | Testar em viewport estreito | Conteúdo e seletor sem recorte prejudicial |
| UX-THEME-08 | Gerar PDF técnico/cliente | Os PDFs não mudam de conteúdo ou métricas pela seleção visual |

**Evidências ainda pendentes:** screenshots reais em Windows/Chrome/Edge, teste com dados fictícios, leitura sob baixa luminosidade, avaliação de cores dos controles nativos e relatório de contraste completo.

## Manutenção

- Mudanças de cor devem alterar `--tokens` em ambos os temas e `--plot-*` correspondentes.
- Evitar CSS `filter:invert()` ou aplicar inversão geral ao canvas.
- Não fixar texto branco em cartão claro nem texto escuro em cartão escuro.
- O tema altera somente apresentação, nunca análise elétrica, registros originais ou cálculos.
