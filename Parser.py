from Grammar import Grammar
from Error import Error


class AstInfo:
    singleton = None

    @staticmethod
    def resetSingletonErrorForNewParsing():
        AstInfo.singleton.error = None

    @staticmethod
    def singletonInstance():
        if AstInfo.singleton == None:
            AstInfo.singleton = AstInfo()
        return AstInfo.singleton

    def __init__(self):
        if AstInfo.singleton != None:
            raise Exception(f"{Error.singletonMsg(self)}.singletonInstance()'!")
        self.error = None
        self.node = None
        AstInfo.singleton = self

    def registry(self, ast_info):
        if ast_info.error:
            self.error = ast_info.error
        return ast_info.node

    def success(self, node):
        self.node = node
        return self

    def fail(self, errorMsg):
        if not self.error:
            self.error = Error(errorMsg)
        return self


class Parser:
    singleton = None

    @staticmethod
    def instance():
        if Parser.singleton == None:
            Parser.singleton = Parser()
        return Parser.singleton

    def __init__(self):
        if Parser.singleton != None:
            raise Exception(f"{Error.singletonMsg(self)}.instance()'!")

        self.__start([])
        Parser.singleton = self

    def NextTok(self):
        self.tokIdx += 1
        if self.tokIdx < len(self.tokens):
            self.currentToken = self.tokens[self.tokIdx]
        return self.currentToken

    def __start(self, _tokens):
        self.tokens = _tokens
        self.tokIdx = -1
        self.currentToken = None
        self.manager = AstInfo.singletonInstance()
        self.manager.resetSingletonErrorForNewParsing()

    def Manager(self):
        return self.manager

    def CurrentTok(self):
        return self.currentToken

    def Parsing(self, _tokens):
        self.__reset(_tokens)
        return Grammar.StartSymbol(self)

    def __reset(self, _tokens):
        self.__start(_tokens)
        self.NextTok()
