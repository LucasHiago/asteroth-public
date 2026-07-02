# Changelog: asteroth-public

Marcos públicos do projeto Asteroth. Detalhes técnicos do desenvolvimento ficam no repositório de código (privado).

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

---

## [Unreleased]

### Added
- **Seta de rolagem no pergaminho**: chevron pulsante pousado acima do rolo de baixo do papiro — clicar rola uma "página" do texto com animação suave; a seta some ao chegar no fim (e não aparece quando o texto cabe inteiro).

### Changed
- **Modal unificado: um papiro só**: todos os modais (Governante, conto, vinheta, item) agora são um único pergaminho grande (`papyrus_frame`, até 760px) com a arte no topo — boss/item fundidos no papiro, pinturas de mundo como prancha emoldurada — e o texto rolando abaixo, entre os rolos. O corpo do papiro virou camada própria (irmã do scroller) com tile espelhado que repete sem esticar em qualquer altura; isso também elimina de vez o texto/scroll vazando pra fora do pergaminho.

### Fixed
- **Papiro "vazado" no modal**: o corpo do papiro sumia (fundo escuro translúcido com borda aparente) em certos tamanhos de janela — bug de composição do Chromium com `border-image fill` quando há scroll no elemento ou num filho. O corpo agora é `background` clipado no padding-box (`papyrus_body.jpg`), com o 9-slice só na moldura; scroll movido pra um wrapper interno.

### Changed
- **Papiro maior, papel menor**: colunas do modal-livro em 2fr/3fr (antes ~metade/metade) — o pergaminho de texto domina.
- **Mobile: só o papiro**: em telas pequenas a folha da arte some e o boss aparece no topo do próprio pergaminho (blend multiply; pinturas de mundo como prancha emoldurada).
- **Modal: papel na arte, papiro no texto**: em todos os modais, a arte agora senta na folha antiga de bordas rasgadas (`paper_frame`) e o texto sempre no papiro com rolos (`papyrus_frame`) — antes o boss tinha o texto no papel e a arte num cartão branco.

### Added
- **Modais em pergaminho + Compêndio de Itens**: texto dos modais de conto/vinheta agora vive num papiro com rolos ([`concepts/assets/papyrus_blank.png`](concepts/assets/papyrus_blank.png)) e o do Governante numa folha antiga de bordas rasgadas ([`concepts/assets/paper_blank.png`](concepts/assets/paper_blank.png)) — o conteúdo rola entre os rolos, com sensação de desenrolar o pergaminho. Tipografia de texto antigo (IM Fell English no corpo, Uncial Antiqua nos títulos). Capítulos do Lore reorganizados em blocos de 2 colunas (arte | texto) com borda de cantos cortados ecoando os botões. Nova seção **O Compêndio de Itens**: primeiros 10 registros (Ferramentas) de 517 catalogados, cada item abre num papiro único com a arte e a descrição rolando juntas; revelação em levas de 10.
- **Modal-livro e artes do Lore sem corte**: modais de Governante/conto/vinheta viram livro aberto (arte impressa na página esquerda via blend com o papel, texto com capitular na direita; o modal do Governante inclui o conto do despertar). Concept arts do Lore agora aparecem inteiras — arte emoldurada sobre backdrop borrado dela mesma, em vez de crop widescreen.
- **Redesign do site com cara de jogo** ([asteroth.com.br](https://asteroth.com.br)): hero cinematográfico (zoom lento na cover + badge de status), contos como cards com medalhão do Governante correspondente (antes lista de texto), concept arts full-bleed entre os capítulos do Lore, galeria de O Mundo com card em destaque e títulos sobre a arte, reveal animations no scroll, botões estilo game UI e Contos promovido na navegação (antes de Gameplay).
- **Banner no README** ([`concepts/white_red_bg.png`](concepts/white_red_bg.png)), banner principal (3260×2048, ~8.9 MB) no topo do [`README.md`](README.md). Pasta `concepts/` criada pra arts públicas.
- **Coleção "Contos dos Governantes"** em [`stories/`](stories/), vinte e seis vinhetas, uma por governante do panteão (Cthulhu → Chronus). Cada conto mostra a entidade interagindo com humanos no momento do despertar, ou em ação. Cada arquivo linka de volta pro verbete em [`GOVERNANTES.md`](GOVERNANTES.md). Tom narrativo curto (~250–300 palavras por conto), em prosa. Material vivo, sementes pra expansão futura. Índice em [`stories/README.md`](stories/README.md).

### Initial
- **Repo público criado.** Espaço externo do projeto Asteroth: pitch, lore, panteão dos governantes, mecânicas-em-tom-narrativo, e canal de sponsor. O código-fonte continua num repo privado separado.
- **[`LORE.md`](LORE.md)**, canon do mundo: a origem cosmogônica (a Hora das Partículas), Asteroth como entidade-salvadora-do-planeta, e o mundo físico (planeta esférico, sol, órbita anual, duas luas, civilização player-driven).
- **[`GOVERNANTES.md`](GOVERNANTES.md)**, panteão das 26 entidades que dividem o domínio do planeta. Descrições completas dos 10 maiores (Cthulhu, Azazel, Beelzebub, Metatron, Hastur, Abaron, Abaddon, Mammon, Baphomet, Asratheet) + 16 regentes menores em forma compacta. Cada um com sua condição de despertar.
- **[`GAMEPLAY.md`](GAMEPLAY.md)**, mecânicas em tom narrativo: vínculo de classe primária (habilidade única que persiste após troca de classe) e o sistema de fama (status aleatórios, bônus em 1.000 pts, redistribuição em PvP por contribuição).
- **[`stories/`](stories/)**, pasta pronta pra receber contos curtos do mundo.
- **[`README.md`](README.md)** + **[`.github/FUNDING.yml`](.github/FUNDING.yml)**, pitch + sponsor button (GitHub Sponsors, Patreon `Asteroth`, asteroth.com.br).
