# Runbook — leva do Bestiário (executar UMA leva por vez)

Executa uma leva de até 10 criaturas do Bestiário no site. As criaturas já publicadas servem de referência de padrão — **sempre imitar o que já está no arquivo** (e NUNCA editar este runbook).

## Repos

- **Site**: `~/PROJETOS_PM2/STEPLY/asteroth-public` (este repo). Fluxo: branch + PR + merge (`--merge`, nunca squash, nunca deletar branch).
- **Catálogo**: `~/PROJETOS_PM2/STEPLY/Asteroth/game_rules/world/bestiary/mobs.json` — **somente leitura**: é GERADO de `mob_hierarchy.md` (não editar nem o .json nem o .md por causa do site). Contexto de cada criatura: `~/PROJETOS_PM2/STEPLY/Asteroth/game_rules/world/mob_hierarchy.md`.
- **NUNCA** `git add .`/`-A` — sempre paths explícitos. Não tocar arquivos não relacionados no working tree.

## 1. Selecionar a leva

**Pendente = mob que ainda não está no site** (sem `id="mob-<slug>"` no `site/index.html`, slug = `id` do mobs.json com `_`→`-`).

```python
import json, re
d = json.load(open('.../Asteroth/game_rules/world/bestiary/mobs.json'))
html = open('site/index.html').read()
no_site = set(re.findall(r'article id="mob-([a-z0-9-]+)"', html))
pend = [m for m in d['mobs'] if m['id'].replace('_','-') not in no_site]
```

- Leva = os **próximos até 10 pendentes na ordem do arquivo** (a ordem do mobs.json já agrupa por domínio e desce a hierarquia). Não misturar domínios na mesma leva: se o domínio atual tem <10 pendentes, a leva é menor e fecha o capítulo.
- Capítulo atual = domínio da leva (rótulos: vulcanico=Domínio Vulcânico · pantano=Domínio do Pântano · necropole=Domínio da Necrópole · tundra=Domínio da Tundra · deserto=Domínio do Deserto · picos=Domínio dos Picos · floresta=Domínio da Floresta · fauna=Fauna Livre · slimes=Slimes).
- Nº da leva = (mobs no site ÷ 10) + 1.

## 2. Imagens

Copiar de `Asteroth/<image>` (campo `image` do mob) pra `asteroth-public/concepts/mobs/<domain>/` (`mkdir -p` se preciso). **Sem processamento nenhum** — jpg original.

## 3. Site (`site/index.html`)

Tudo dentro de `<section id="bestiario">`:

1. **Contador**: `<div class="itens-count"><span>N</span> de <span>326</span> criaturas reveladas · capítulo atual: <strong>RÓTULO</strong></div>` — somar a leva ao N.
2. **Card** no fim de `.mobs-grid` (copiar o formato exato dos existentes):
   `<a class="item-card" href="#mob-<slug>" data-domain="<domain>" data-rank="<rank>"><img src="concepts/mobs/<domain>/<arquivo>" alt="<name_pt>" loading="lazy" /><span class="item-name"><name_pt></span><span class="item-cat"><Domínio> · <Patente></span></a>`
   - `data-domain`/`data-rank` = valores crus do mobs.json (os filtros dependem deles; os rótulos PT já estão nos maps `DOMAIN_LABEL`/`RANK_LABEL` do script da seção).
3. **Article** no fim de `.item-list` da seção (formato exato dos existentes):
   - `<p class="epitaph">Domínio X · <Patente> · <Raridade></p>` (raridade PT capitalizada: Único/Lendário/Raro/Incomum/Comum).
   - **2 parágrafos** de descrição. Tom: bestiário antigo de um mundo medieval-fantástico, denso, concreto, sem clichê de RPG genérico; 1º parágrafo descreve a criatura e como ela caça/age como quem a viu; 2º traz costume, superstição ou relato dos caçadores/vilas, idealmente fechando com um gancho de lore sutil. Ler 3–4 entries existentes antes de escrever. O `description_short` do mobs.json e a tabela do `mob_hierarchy.md` são a semente (perfil/comportamento) — mas **nunca citar mecânicas de jogo** ("HP", "AoE", "glass cannon", "tank", "buff"), sempre traduzir em comportamento narrado.

## 4. CHANGELOG do site

Adicionar em `[Unreleased] > Added`: uma linha "**Bestiário: leva N (TOTAL/326)**: ..." listando as criaturas com patente.

## 5. Verificação mínima (antes do merge)

```bash
# nº de cards do bestiário == contador
grep -o 'data-domain=' site/index.html | wc -l
# âncoras novas existem (pra cada slug)
grep -c 'id="mob-<slug>"' site/index.html
```
Se `playwright` disponível, abrir `site/index.html` via http.server local, clicar num card novo e screenshotar o modal + testar os dois filtros (padrão dos PRs anteriores).

## 6. Entrega

1. asteroth-public: branch `feat/site-mobs-batch-N` a partir de main atualizado → commit (`feat(site): bestiário leva N — ...`, paths explícitos: `site/index.html`, `concepts/mobs/...`, `CHANGELOG.md`) → push → `gh pr create` (body com criaturas, test plan) → `gh pr review <n> --comment` (self-review) → `gh pr merge <n> --merge` → `git checkout main && git pull`.
2. Reportar: nº da leva, domínio, criaturas, link da PR, total revelado (N/326) e quantos pendentes restam.
