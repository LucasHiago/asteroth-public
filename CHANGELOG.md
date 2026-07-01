# Changelog: asteroth-public

Marcos públicos do projeto Asteroth. Detalhes técnicos do desenvolvimento ficam no repositório de código (privado).

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

---

## [Unreleased]

### Added
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
