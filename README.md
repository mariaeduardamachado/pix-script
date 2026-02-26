# 🧾 Pix Script – Analisador Léxico (Lexer)

Projeto desenvolvido para a disciplina de **Compiladores** no **IF Goiano – Campus Trindade**.  
O objetivo é implementar um **analisador léxico** para a linguagem **Pix Script**, gerando:

- ✅ Código tokenizado (`.pixobj`)
- ✅ Tabela de símbolos (`.csv`)
- ✅ Log de erros léxicos (`.log`), caso existam

---

## 📌 Visão Geral

O analisador léxico (lexer) lê um arquivo de entrada no formato `.pix` e percorre o conteúdo caractere a caractere, reconhecendo lexemas e classificando-os em tokens.

### 📥 Entrada
- Arquivo texto: `programa.pix`

### 📤 Saídas geradas
- `programa.pixobj` → lista de tokens (código tokenizado)
- `programa.csv` → tabela de símbolos (identificadores encontrados)
- `programa.log` → erros léxicos (se houver)

---

## 🧠 Tokens reconhecidos

O lexer reconhece, entre outros:

### Palavras reservadas
- `LEDGER`, `CLOSE`, `LET`, `IF`, `TRUE`, `FALSE`

### Tipos
- `$` Decimal  
- `#` Inteiro  
- `@` Texto  
- `?` Booleano  
- `!` Chave PIX  
- `~` Nulo  

### Operadores
- Aritméticos: `++`, `--`, `**`, `//`, `%%`
- Relacionais: `==`, `!=`, `>>`, `<<`, `>=`, `<=`
- Lógicos: `&&`, `||`, `!!`
- Atribuição: `<-`, `=`

### Delimitadores
- `(`, `)`, `{`, `}`

### Literais
- Strings: `'texto'` ou `"texto"`
- Números: inteiros e decimais

### Identificadores
- Qualquer nome válido de variável fora da lista de palavras reservadas

---

## 🛠️ Requisitos

- Python 3.8+ (recomendado Python 3.10+)
- Sistema: Linux/Windows/Mac

---

## ▶️ Como executar

### 1) Clone o repositório
```bash
git clone https://github.com/mariaeduardamachado/pix-script.git
cd pix-script

### Execute o analisador

python3 src/pix_lexer.py exemplos/entrada.pix
ou
python src/pix_lexer.py exemplos/entrada.pix

### Exemplo de entrada

LEDGER transferencia
LET @nome <- 'Denecley'
LET $valor <- 500.00
IF ($valor >> 100.00){
$> 'Transferindo'
}
CLOSE

### Exemplo de saída

LEDGER -> RESERVED
transferencia -> IDENTIFIER
LET -> RESERVED
@ -> TYPE
nome -> IDENTIFIER
<- -> OPERATOR
'Denecley' -> STRING
...




