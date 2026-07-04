PYTHON  := python3
SCRIPTS := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ROOT    := $(SCRIPTS)../

# variáveis com defaults sobrescrevíveis
SRC       ?= $(ROOT)concepts/classes
OUT       ?= $(ROOT)concepts/classes/treated
THRESHOLD ?= 160
ITEMS_SRC ?= $(ROOT)site/concepts/items/

.DEFAULT_GOAL := help
.PHONY: help cut cut-classes cut-items remove-bg

# quando OUT vem da linha de comando, repassa como -o; senão o script
# salva os PNGs na mesma pasta do arquivo de entrada
ifeq ($(origin OUT),command line)
CUT_OUT = -o "$(OUT)"
endif

help:
	@echo ""
	@echo "  make cut          FILE=<imagem> [OUT=<pasta>] [THRESHOLD=160]"
	@echo "      recorta silhueta de UM arquivo só"
	@echo "      gera <nome>_black.png e <nome>_white.png ao lado do original (ou em OUT)"
	@echo ""
	@echo "  make cut-classes  [SRC=<pasta|arquivo>] [OUT=<pasta>] [THRESHOLD=160]"
	@echo "      recorta silhueta preta de imagens GPT Image 2"
	@echo "      gera <nome>_black.png e <nome>_white.png em OUT"
	@echo "      padrão: SRC=$(ROOT)concepts/classes  OUT=$(ROOT)concepts/classes/treated"
	@echo ""
	@echo "  make cut-items    [ITEMS_SRC=<pasta>]"
	@echo "      recorta fundo cinza dos ícones do compêndio"
	@echo "      padrão: ITEMS_SRC=$(ROOT)site/concepts/items/"
	@echo ""
	@echo "  make remove-bg    SRC=<arquivo|pasta>"
	@echo "      remove fundo por chroma key (cantos como referência)"
	@echo "      salva PNG no mesmo diretório da entrada"
	@echo ""

cut:
ifndef FILE
	$(error uso: make cut FILE=<imagem> [OUT=<pasta>] [THRESHOLD=160])
endif
	$(PYTHON) $(SCRIPTS)cut_class_symbols.py "$(FILE)" $(CUT_OUT) -t $(THRESHOLD)

cut-classes:
	$(PYTHON) $(SCRIPTS)cut_class_symbols.py $(SRC) -o $(OUT) -t $(THRESHOLD)

cut-items:
	find $(ITEMS_SRC) -name "*.jpg" | xargs $(PYTHON) $(SCRIPTS)cut_item_bg.py

remove-bg:
	$(PYTHON) $(SCRIPTS)remove-bg.py $(SRC)
