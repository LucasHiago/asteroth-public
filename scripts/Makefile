PYTHON  := python3
SCRIPTS := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ROOT    := $(SCRIPTS)../

# variáveis com defaults sobrescrevíveis
SRC       ?= .
OUT       ?= $(ROOT)site/concepts/classes/
THRESHOLD ?= 160
ITEMS_SRC ?= $(ROOT)site/concepts/items/

.DEFAULT_GOAL := help
.PHONY: help cut-classes cut-items remove-bg

help:
	@echo ""
	@echo "  make cut-classes  [SRC=<pasta|arquivo>] [OUT=<pasta>] [THRESHOLD=160]"
	@echo "      recorta silhueta preta de imagens GPT Image 2"
	@echo "      gera <nome>_black.png e <nome>_white.png em OUT"
	@echo "      padrão: SRC=.  OUT=$(ROOT)site/concepts/classes/"
	@echo ""
	@echo "  make cut-items    [ITEMS_SRC=<pasta>]"
	@echo "      recorta fundo cinza dos ícones do compêndio"
	@echo "      padrão: ITEMS_SRC=$(ROOT)site/concepts/items/"
	@echo ""
	@echo "  make remove-bg    SRC=<arquivo|pasta>"
	@echo "      remove fundo por chroma key (cantos como referência)"
	@echo "      salva PNG no mesmo diretório da entrada"
	@echo ""

cut-classes:
	$(PYTHON) $(SCRIPTS)cut_class_symbols.py $(SRC) -o $(OUT) -t $(THRESHOLD)

cut-items:
	find $(ITEMS_SRC) -name "*.jpg" | xargs $(PYTHON) $(SCRIPTS)cut_item_bg.py

remove-bg:
	$(PYTHON) $(SCRIPTS)remove-bg.py $(SRC)
