from Consts import Consts
from Error import Error
from SemanticVisitor import *  # mantive a importação para compatibilidade


class Grammar:
    def __init__(self, parser):
        self.parser = parser

    def Rule(self):
        return self.GetParserManager().fail(
            f"{Error.parserError}: Implementar suas regras de producao (Heranca de Grammar)!"
        )

    def CurrentToken(self):
        return self.parser.CurrentTok()

    def NextToken(self):
        return self.parser.NextTok()

    def GetParserManager(self):
        return self.parser.Manager()

    @staticmethod
    def StartSymbol(parser):  # Start Symbol S from Grammar G(V, T, S, P)
        resultado = Historia(parser).Rule()
        if parser.CurrentTok().type != Consts.EOF:
            return resultado.fail(
                f"{Error.parserError}: Erro sintatico - tokens remanescentes"
            )
        return resultado


# <Historia> ::= "o" <Personagem> <Acao> "o" <Objeto> "."
class Historia(Grammar):
    def Rule(self):
        pr = self.GetParserManager()
        tok = self.CurrentToken()

        # Expect article "o" (ID with value 'o')
        if tok.type != Consts.ID or tok.value != "o":
            return pr.fail(
                f"{Error.parserError}: Esperado o artigo 'O' no inicio da historia"
            )
        self.NextToken()

        # Personagem
        personagem_node = pr.registry(Personagem(self.parser).Rule())
        if pr.error:
            return pr

        # Acao
        acao_node = pr.registry(Acao(self.parser).Rule())
        if pr.error:
            return pr

        # Expect article "o" before objeto
        tok = self.CurrentToken()
        if tok.type != Consts.ID or tok.value != "o":
            return pr.fail(
                f"{Error.parserError}: Esperado o artigo 'o' antes do objeto"
            )
        self.NextToken()

        # Objeto
        objeto_node = pr.registry(Objeto(self.parser).Rule())
        if pr.error:
            return pr

        # Expect dot
        tok = self.CurrentToken()
        if tok.type != Consts.DOT:
            return pr.fail(f"{Error.parserError}: Esperado '.' ao final da historia")
        self.NextToken()

        # Build AST-like node (dictionary)
        node = {
            "type": "Historia",
            "personagem": personagem_node,
            "acao": acao_node,
            "objeto": objeto_node,
        }
        return pr.success(node)


class Personagem(Grammar):
    def Rule(self):
        personagens = ("gato", "menino", "dragao")

        pr = self.GetParserManager()
        tok = self.CurrentToken()
        if tok.type == Consts.ID and tok.value in personagens:
            # return the value as node
            val = tok.value
            self.NextToken()
            return pr.success({"type": "Personagem", "value": val})
        return pr.fail(
            f"{Error.parserError}: Esperado um Personagem ({', '.join(personagens[:-1])} ou {personagens[-1]})"
        )


class Acao(Grammar):
    def Rule(self):
        acoes = ("comeu", "achou", "derrubou")

        pr = self.GetParserManager()
        tok = self.CurrentToken()
        if tok.type == Consts.ID and tok.value in acoes:
            val = tok.value
            self.NextToken()
            return pr.success({"type": "Acao", "value": val})
        return pr.fail(
            f"{Error.parserError}: Esperado uma Acao ({', '.join(acoes[:-1])} ou {acoes[-1]})"
        )


class Objeto(Grammar):
    def Rule(self):
        objetos = ("pao", "livro", "castelo")

        pr = self.GetParserManager()
        tok = self.CurrentToken()
        if tok.type == Consts.ID and tok.value in objetos:
            val = tok.value
            self.NextToken()
            return pr.success({"type": "Objeto", "value": val})
        return pr.fail(
            f"{Error.parserError}: Esperado um Objeto ({', '.join(objetos[:-1])} ou {objetos[-1]})"
        )
