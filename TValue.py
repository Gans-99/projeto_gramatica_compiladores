####################################### Inclui tudo que tem valor (pode conter @abc.abstractmethod para metodos abstratos) #######################################
class TValue():
	def __init__(self) -> None:
		self.value = None

class TNumber(TValue):
	def __init__(self, value):
		self.value = value
	def __repr__(self):
		return str(self.value)
