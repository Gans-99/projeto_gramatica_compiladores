from Consts import Consts
from Token import Token
from Error import Error


class Lexer:
    def __init__(self, source_code):
        self.code = source_code
        self.current = None
        self.indice, self.coluna, self.linha = -1, -1, 0
        self.__advance()

    def __advance(self):
        self.__advanceCalc(self.current)
        self.current = self.code[self.indice] if self.indice < len(self.code) else None

    def __advanceCalc(self, _char=None):
        self.indice += 1
        self.coluna += 1
        if _char == "\n":
            self.linha += 1
            self.coluna = 0
        return self

    def makeTokens(self):
        tokens = []
        while self.current != None:
            # whitespace
            if self.current in " \t\n\r":
                self.__advance()
                continue

            # strings (keep original behavior)
            if self.current == '"':
                tokens.append(self.__MakeString())
                continue

            # punctuation: dot (.)
            if self.current == ".":
                tokens.append(Token(Consts.DOT, "."))
                self.__advance()
                continue

            # letters => identifier / keyword
            if self.current in Consts.LETRAS or self.current == Consts.UNDER:
                tokens.append(self.__makeIdentifier())
                continue

            # unknown symbol -> produce lexer error
            bad = self.current
            self.__advance()
            return [], Error(f"{Error.lexerError}: lex-symbol '{bad}' fail!")

        tokens.append(Token(Consts.EOF))
        return tokens, None

    def __MakeString(self):
        stri = ""
        bypass = False
        self.__advance()
        specialChars = {"n": "\n", "t": "\t"}
        while self.current != None and (self.current != '"' or bypass):
            if bypass:
                c = specialChars.get(self.current, self.current)
                stri += c
                bypass = False
            else:
                if self.current == "\\":
                    bypass = True
                else:
                    stri += self.current
            self.__advance()

        # close quote
        self.__advance()
        return Token(Consts.STRING, stri)

    def __makeIdentifier(self):
        id_str = ""
        while self.current != None and (
            self.current in Consts.LETRAS_DIGITOS + Consts.UNDER
        ):
            id_str += self.current
            self.__advance()
        # normalize to lowercase for comparisons in grammar
        id_lower = id_str.lower()
        # If you have a KEY list of reserved words in Consts, you could map them to KEY token type.
        # For simplicity we return ID with lowercase value
        return Token(Consts.ID, id_lower)
