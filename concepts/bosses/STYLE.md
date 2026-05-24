# Estilo: Low Poly Asteroth

Bloco de estilo compartilhado pelos prompts dos bosses, calibrado para **Leonardo.ai**. Cada `<boss>/<boss>.md` traz só a descrição objetiva do personagem. Combine com o bloco abaixo na hora de gerar.

## Style block (cole no início do prompt)

```
chunky low poly 3D character, stylized fantasy game art, sharp geometric facets, flat shading, vivid limited palette, transparent background, full body character sheet, frontal pose, isolated subject, soft rim light, clean silhouette
```

## Negative prompt (universal)

```
realistic, photoreal, smooth shading, blurry, low detail, extra limbs, deformed, cluttered background, watermark, text, signature, low quality, motion blur, noise
```

## Como compor o prompt final

```
<style block>. <descricao do boss do MD correspondente>.
```

Exemplo (Azazel):

```
chunky low poly 3D character, stylized fantasy game art, sharp geometric facets, flat shading, vivid limited palette, transparent background, full body character sheet, frontal pose, isolated subject, soft rim light, clean silhouette. Tall lean demon, 5m, black ram horns, glowing green flame eyes, muscular green skin, dark membranous bat wings spread, green fire on both hands, black flowing loincloth, barbed tail.
```

## Referencias visuais

- Concept arts ja prontas: [azazel](azazel/), [hastur](hastur/), [metatron](metatron/).
- Pasta privada com mais seeds de estilo: `concepts/seeds/` (gitignored).

## Configuracao sugerida no Leonardo.ai

- Model: **Phoenix** ou **Lightning XL**.
- Preset Style: **3D Render** ou **Stylized**.
- Aspect ratio: **1:1** (sheet) ou **2:3** (corpo inteiro vertical).
- Guidance scale: **7**.
- Sem transparencia nativa? Use fundo branco e remova depois com PNG mask, ou troque `transparent background` por `clean white background` no style block.

## Convencoes da descricao do boss

Cada MD descreve em ingles, em um paragrafo unico, na ordem:

1. Tipo + porte (ex: "Tall demon, 5m").
2. Cabeca e olhos (chifres, mascara, expressao).
3. Pele/escamas/material com paleta de 2 a 4 cores.
4. Membros e adendos (asas, cauda, garras).
5. Roupa/armadura.
6. Arma e props principais.
7. Aura/efeito visual.

Mantenha cada descricao entre **400 e 700 caracteres** para nao saturar o Leonardo.
