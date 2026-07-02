# Runbook — leva do Compêndio de Itens (executar UMA leva por vez)

Executa uma leva de até 10 itens do compêndio: descrições longas no site + tooltips no catálogo do jogo. Já existem 20 itens feitos servindo de referência de padrão — **sempre imitar o que já está no arquivo**.

## Repos

- **Site**: `~/PROJETOS_PM2/STEPLY/asteroth-public` (este repo). Fluxo: branch + PR + merge (`--merge`, nunca squash, nunca deletar branch).
- **Catálogo**: `~/PROJETOS_PM2/STEPLY/Asteroth/game_rules/items/catalog/items.json`. Commit direto na main (exceção `game_rules/`); o push exige `ASTEROTH_ALLOW_MAIN_PUSH=1 git push`.
- **NUNCA** `git add .`/`-A` — sempre paths explícitos. Não tocar arquivos não relacionados (ex.: README.md modificado no working tree é WIP do usuário).

## 1. Selecionar a leva

```python
import json
d = json.load(open('.../Asteroth/game_rules/items/catalog/items.json'))
pend = [i for i in d['items'] if not i['description_short']]
```

- Categoria da leva: a **categoria em andamento** (que já tem itens descritos e ainda tem pendentes); se nenhuma, a primeira categoria na ordem do arquivo com pendentes.
- Leva = os **próximos até 10 pendentes dessa categoria, na ordem do arquivo**. Se a categoria tem <10 pendentes, a leva é menor (fecha o capítulo; não misturar categorias na mesma leva).
- Nº da leva = (itens já descritos ÷ 10) + 1.

## 2. Imagens

Copiar de `Asteroth/<image>` (campo `image` do item) pra `asteroth-public/concepts/items/<categoria>/` (`mkdir -p` se preciso). **Sem processamento nenhum** — jpg original. Se a imagem não existir no repo Asteroth, incluir o item mesmo assim com `<img>` apontando pro caminho esperado e anotar na PR.

## 3. Site (`site/index.html`)

Tudo dentro de `<section id="itens">`:

1. **Contador**: `<div class="itens-count"><span>N</span> de <span>517</span> ... capítulo atual: <strong>RÓTULO</strong></div>` — somar a leva ao N; rótulo = capítulo da leva (tabela abaixo).
2. **Card** no fim de `.itens-grid` (copiar o formato exato dos existentes):
   `<a class="item-card" href="#item-<slug>"><img src="concepts/items/<cat>/<arquivo>" alt="<name_pt>" loading="lazy" /><span class="item-name"><name_pt></span><span class="item-cat">RÓTULO · Subtipo</span></a>`
   - slug = `id` com `_`→`-`. Subtipo = campo `subtype` em Title Case pt (ex.: `minerio_bruto` → "Minério Bruto"); omitir se não houver.
3. **Article** no fim de `.item-list` (formato exato dos existentes):
   - `<p class="epitaph">RÓTULO · Subtipo · <aceita tiers|sem tier> · <forjável|encontrado no mundo></p>` (tierable/craftable do JSON; `artefato` = "encontrado no mundo").
   - **2 parágrafos** de descrição. Tom: compêndio antigo de um mundo medieval-fantástico, denso, concreto, sem clichê de RPG genérico; 1º parágrafo descreve o objeto e seu uso como quem viveu aquilo; 2º traz costume, ofício ou superstição do mundo, idealmente fechando com um gancho de lore sutil (algo que insinua perigo/mistério sem explicar). Ler 3–4 entries existentes antes de escrever. Nunca citar mecânicas de jogo ("dá +5 de...", "tier 3"), nunca quebrar o tom.

### Rótulos de capítulo (categoria → rótulo)

materia_prima=Matéria-prima · material_refinado=Material refinado · material_raro=Material raro · construcao=Construção · engrenagem=Engrenagens · ferramenta=Ferramentas · ataque=Ataque · armadura=Armadura · magia=Magia · pocao=Poções · alimento=Alimento · pesca=Pesca & mar · planta=Plantas · semente=Sementes · madeira=Madeira & troncos · animal=Animais · armazenamento=Armazenamento · descanso=Descanso & mobília · artefato=Artefato · obra_prima=Obra-prima

No `.item-cat` e no epitaph usar o rótulo no singular natural ("Ferramenta", "Matéria-prima", "Poção", "Arma" pra ataque etc. — bom senso, consistente dentro da leva).

## 4. Catálogo (tooltips)

Pra cada item da leva, gravar `description_short`: **1–2 frases, ≤90 chars**, destilando a descrição longa (ver os 20 existentes). Editar via python (`json.dump(..., ensure_ascii=False, indent=2)` + newline final), com `assert it['description_short'] == ''` antes de gravar. Conferir `git diff --stat`: deve tocar exatamente N linhas.

## 5. CHANGELOG do site

Adicionar em `[Unreleased] > Added` (criar a subseção se preciso): uma linha "**Compêndio: leva N (TOTAL/517)**: ..." listando os itens.

## 6. Verificação mínima (antes do merge)

```bash
# nº de cards == contador
grep -o 'class="item-card"' site/index.html | wc -l
# âncoras novas existem
grep -c 'id="item-<slug>"' site/index.html   # pra cada slug
python3 -c "import json; json.load(open('site/index.html' if 0 else '.../items.json'))"  # json válido
```
Se `playwright` disponível, abrir `site/index.html` via http.server local, clicar num card novo e screenshotar o modal (padrão dos PRs anteriores).

## 7. Entrega

1. Asteroth: `git add game_rules/items/catalog/items.json && git commit -m "docs(game_rules): descrições da leva N do compêndio — <resumo>" && ASTEROTH_ALLOW_MAIN_PUSH=1 git push` (footer `Co-Authored-By` conforme commits anteriores).
2. asteroth-public: branch `feat/site-items-batch-N` a partir de main atualizado → commit (`feat(site): compêndio leva N — ...`) → push → `gh pr create` (body com itens, test plan) → `gh pr review <n> --comment` (self-review) → `gh pr merge <n> --merge` → `git checkout main && git pull`.
3. Reportar: nº da leva, categoria, itens, link da PR, total revelado (N/517) e quantos pendentes restam.
