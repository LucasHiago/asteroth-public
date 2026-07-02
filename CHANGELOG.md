# Changelog: asteroth-public

Marcos públicos do projeto Asteroth. Detalhes técnicos do desenvolvimento ficam no repositório de código (privado).

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

---

## [Unreleased]

### Changed
- **Item no slot de inventário**: no modal do Compêndio, o ícone agora flutua dentro do slot dourado do jogo ([`item_border.png`](concepts/assets/item_border.png)); os 10 ícones foram recortados do fundo cinza (PNG com alpha, [`scripts/cut_item_bg.py`](scripts/cut_item_bg.py)) — no grid também ficam limpos, sem tile cinza.
- **Cards dos Governantes em folha antiga**: o card inteiro agora É a folha rasgada (`paper_frame` como background) — retrato em blend multiply, nome em tinta escura e epíteto em sépia impressos no papel; sem card escuro nem borda. O grid vira uma parede de gravuras.
- **Pinturas fundidas no pergaminho**: nos modais de O Mundo, a concept art derrete no papiro (multiply + máscara radial esfumando as bordas + tom sépia) em vez da prancha retangular que cortava a textura; a arte vira um banner de iluminura de altura fixa (corte cover 16:10) — retratos altos não engolem mais o pergaminho, título e texto aparecem já na primeira dobra.
- **Texto do pergaminho com respiro**: margens do conteúdo recuadas pra dentro das colunas de ornamento da folha (24% laterais, 20%/18% vertical) — o texto não atropela mais os desenhos nem as bordas rasgadas.
- **Papiro de imagem única**: o pergaminho do modal deixou de ser montado em 9 fatias + tile central (que criava uma emenda retangular visível cortando a textura) e virou o `papyrus_frame` inteiro esticado numa única camada; o conteúdo é ancorado em percentuais, então rolos e bordas escalam juntos em qualquer tamanho — visual fluido, sem costura.

### Added
- **Compêndio: leva 14 (116/517)**: fecha o capítulo Material refinado — 2 itens revelados: Argamassa e Tijolo — descrições inéditas em tom de compêndio antigo; tooltips curtos gravados no catálogo do jogo (ambos estavam vazios). Próximo capítulo: Construção.
- **Compêndio: leva 13 (114/517)**: continua o capítulo Material refinado — 10 itens revelados: Viga, Vidro, Papel, Tinta, Cera, Óleo Refinado, Farinha, Corante, Cola e Piche — descrições inéditas em tom de compêndio antigo; tooltips curtos gravados no catálogo do jogo (todos estavam vazios).

- **Compêndio: leva 12 (104/517)**: continua o capítulo Material refinado — 10 itens revelados: Barra de Bronze, Barra de Estanho, Barra de Prata, Barra de Ouro, Barra de Aço, Barra de Chumbo, Couro Endurecido, Linho Tecido, Tecido de Lã e Tecido de Seda — descrições inéditas em tom de compêndio antigo; tooltips curtos gravados no catálogo do jogo (todos estavam vazios).

- **Compêndio: leva 11 (94/517)**: abre o capítulo Material refinado — 10 itens revelados: Barra de Ferro, Barra de Cobre, Couro, Couro Esticado, Tecido, Linha, Tábua, Carvão, Pólvora e Corda — descrições inéditas em tom de compêndio antigo; todos tinham tooltip legado no catálogo (não sobrescritos, usados como semente das descrições longas).

- **Compêndio: leva 10 (84/517)**: fecha o capítulo Matéria-prima — 3 itens revelados: Pó Rúnico, Cristal Rúnico e Fragmento de Glifo — descrições inéditas em tom de compêndio antigo; tooltips curtos gravados no catálogo do jogo (todos estavam vazios).

- **Compêndio: leva 9 (81/517)**: continua o capítulo Matéria-prima — 10 itens revelados: Cristal Carregado, Pedra de Faísca, Mana Bruta, Diamante Bruto, Rubi Bruto, Safira Bruta, Esmeralda Bruta, Gema Bruta, Pedra Rúnica e Minério Rúnico — descrições inéditas em tom de compêndio antigo; tooltips curtos gravados no catálogo do jogo (todos estavam vazios).

- **Compêndio: leva 8 (71/517)**: continua o capítulo Matéria-prima — 10 itens revelados: Chifre, Pena, Escama, Gordura Animal, Tendão, Sangue, Água, Óleo Bruto, Energia Engarrafada e Fragmento de Energia — descrições inéditas em tom de compêndio antigo; tooltips curtos gravados no catálogo do jogo (todos estavam vazios).

- **Compêndio: leva 7 (61/517)**: continua o capítulo Matéria-prima — 10 itens revelados: Areia, Pederneira, Sal-gema, Turfa, Cinza, Pele Grossa, Linho Cru, Lã Crua, Seda Crua e Osso — descrições inéditas em tom de compêndio antigo; tooltips curtos gravados no catálogo do jogo (todos estavam vazios).

- **Compêndio: leva 6 (51/517)**: continua o capítulo Matéria-prima — 10 itens revelados: Minério de Estanho, Minério de Prata, Minério de Ouro, Minério de Chumbo, Minério de Zinco, Carvão Mineral, Granito, Mármore, Calcário e Argila — descrições inéditas em tom de compêndio antigo; tooltips curtos gravados no catálogo do jogo (todos estavam vazios).

- **Compêndio: leva 5 (41/517)**: abre o capítulo Matéria-prima — 10 itens revelados: Minério de Ferro, Minério de Cobre, Pedra Bruta, Pele Bruta, Fibra de Algodão, Tora de Carvalho, Erva Medicinal, Cristal de Mana, Enxofre e Salitre — descrições inéditas em tom de compêndio antigo; todos já tinham tooltip legado no catálogo (não sobrescritos).

- **Compêndio: leva 4 (31/517)**: ferramenta final do capítulo revelada — Balança — com descrição inédita em tom de compêndio e tooltip curto gravado no catálogo do jogo. Fecha o capítulo Ferramentas.

- **Compêndio: leva 3 (30/517)**: mais 10 ferramentas reveladas — Faca, Faca de Esfolar, Cutelo, Agulha, Fuso, Pilão, Almofariz, Armadilha de Caça, Laço e Bússola de Agrimensor — com descrições inéditas em tom de compêndio; tooltips curtos gravados no catálogo do jogo.

- **Compêndio: leva 2 (20/517)**: mais 10 ferramentas reveladas — Rede de Arrasto, Enxada, Pá, Foice, Gadanha, Regador, Martelo de Forja, Marreta, Tenaz e Cinzel — com descrições inéditas em tom de compêndio; tooltips curtos gravados no catálogo do jogo. Os ícones voltam ao original com fundo cinza (o recorte de fundo distorcia itens): o JPG fica reduzido dentro do miolo do slot dourado, com cantos arredondados e um anel do interior escuro em volta, e filtro sépia aproximando o cinza do tom do slot.

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
