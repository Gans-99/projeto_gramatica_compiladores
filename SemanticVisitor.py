from TValue import *

class NoNumber:
	def __init__(self, tok):
		self.tok = tok

	def __repr__(self):
		return f'{self.tok}'

class NoOpBinaria:
	def __init__(self, leftNode, opTok, rightNode):
		self.noEsq = leftNode
		self.opTok = opTok
		self.noDir = rightNode

	def __repr__(self):
		return f'({self.noEsq}, {self.opTok}, {self.noDir})'

	@staticmethod
	def Perform(GVar1, ops, GVar2=None): # Grammar Var (GVar), Operator options (ops=+,- ou *, /)
		if GVar2==None: GVar2 = GVar1
		ast = GVar1.GetParserManager()
		op_bin_ou_esq = ast.registry(GVar1.Rule())
		if ast.error: return ast
		while GVar1.CurrentToken().type in ops:
			token_operador = GVar1.CurrentToken()
			GVar1.NextToken()
			lado_direito = ast.registry(GVar2.Rule())
			if ast.error: return ast
			op_bin_ou_esq = NoOpBinaria(op_bin_ou_esq, token_operador, lado_direito)
		return ast.success(op_bin_ou_esq)

class NoOpUnaria:
	def __init__(self, opTok, node):
		self.opTok = opTok
		self.node = node
	def __repr__(self):
		return f'({self.opTok}, {self.node})'
