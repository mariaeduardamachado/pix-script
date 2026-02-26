import sys
import re
import csv

# ===============================
# DEFINIÇÕES DA LINGUAGEM
# ===============================

RESERVED_WORDS = {
    "LEDGER", "CLOSE", "LET", "IF", "TRUE", "FALSE"
}

TYPES = {"$", "#", "@", "?", "!", "~"}

ARITHMETIC_OPS = {"++", "--", "**", "//", "%%"}
RELATIONAL_OPS = {"==", "!=", ">>", "<<", ">=", "<="}
LOGICAL_OPS = {"&&", "||", "!!"}
ASSIGNMENT_OPS = {"<-", "="}
DELIMITERS = {"(", ")", "{", "}"}

TOKEN_REGEX = [
    ("STRING", r"'[^']*'|\"[^\"]*\""),
    ("NUMBER", r"\d+\.\d+|\d+"),
    ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),
]

# ===============================
# ANALISADOR LÉXICO
# ===============================

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.symbol_table = {}
        self.errors = []

    def tokenize(self):
        lines = self.code.split("\n")
        line_number = 0

        for line in lines:
            line_number += 1
            i = 0

            while i < len(line):

                if line[i].isspace():
                    i += 1
                    continue

                # Operadores compostos
                two_char = line[i:i+2]

                if two_char in ARITHMETIC_OPS | RELATIONAL_OPS | LOGICAL_OPS | ASSIGNMENT_OPS:
                    self.tokens.append((two_char, "OPERATOR"))
                    i += 2
                    continue

                # Comando de saída
                if line[i:i+2] == "$>":
                    self.tokens.append(("$>", "OUTPUT"))
                    i += 2
                    continue

                # Tipos
                if line[i] in TYPES:
                    self.tokens.append((line[i], "TYPE"))
                    i += 1
                    continue

                # Delimitadores
                if line[i] in DELIMITERS:
                    self.tokens.append((line[i], "DELIMITER"))
                    i += 1
                    continue

                # Strings
                string_match = re.match(r"'[^']*'|\"[^\"]*\"", line[i:])
                if string_match:
                    value = string_match.group()
                    self.tokens.append((value, "STRING"))
                    i += len(value)
                    continue

                # Números
                number_match = re.match(r"\d+\.\d+|\d+", line[i:])
                if number_match:
                    value = number_match.group()
                    self.tokens.append((value, "NUMBER"))
                    i += len(value)
                    continue

                # Identificadores / Palavras reservadas
                id_match = re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", line[i:])
                if id_match:
                    value = id_match.group()
                    if value in RESERVED_WORDS:
                        self.tokens.append((value, "RESERVED"))
                    else:
                        self.tokens.append((value, "IDENTIFIER"))
                        if value not in self.symbol_table:
                            self.symbol_table[value] = "IDENTIFIER"
                    i += len(value)
                    continue

                # Se nada reconhecido → erro
                self.errors.append(
                    f"Erro léxico na linha {line_number}: símbolo inválido '{line[i]}'"
                )
                i += 1

        return self.tokens

# ===============================
# FUNÇÃO PRINCIPAL
# ===============================

def main():

    if len(sys.argv) < 2:
        print("Uso: python pix_lexer.py arquivo.pix")
        return

    input_file = sys.argv[1]

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            code = f.read()
    except:
        print("Erro ao abrir arquivo.")
        return

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    base_name = input_file.split(".")[0]

    # ===============================
    # GERAÇÃO DO .pixobj
    # ===============================
    with open(base_name + ".pixobj", "w", encoding="utf-8") as f:
        for token in tokens:
            f.write(f"{token[0]} -> {token[1]}\n")

    # ===============================
    # GERAÇÃO DO CSV
    # ===============================
    with open(base_name + ".csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Identificador", "Tipo"])
        for symbol in lexer.symbol_table:
            writer.writerow([symbol, lexer.symbol_table[symbol]])

    # ===============================
    # GERAÇÃO DO LOG
    # ===============================
    if lexer.errors:
        with open(base_name + ".log", "w", encoding="utf-8") as f:
            for error in lexer.errors:
                f.write(error + "\n")

    print("Análise léxica concluída!")

if __name__ == "__main__":
    main()