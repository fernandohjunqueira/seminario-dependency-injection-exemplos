# Exemplo com Injeção e Inversão de Dependência

class PagamentoAbstrato():
	def transferencia_valida(self, saldo, valor):
		saldo_final = self.calcula_saldo_final(saldo, valor)
		if (saldo_final >= 0):
			return True
		else:
			return False

	def calcula_saldo_final(self, saldo, valor):
		pass


class PagamentoComDinheiro(PagamentoAbstrato):
	def calcula_saldo_final(self, saldo, valor):
		return saldo - valor
		
class PagamentoComCheque(PagamentoAbstrato):
	def __init__(self, taxa):
		self._taxa = taxa # Taxa fixa

	def calcula_saldo_final(self, saldo, valor):
		return saldo - valor - self._taxa

# Serviço
class PagamentoComCartao(PagamentoAbstrato):
	def __init__(self, taxa):
		self._taxa = taxa # Valor da taxa cobrada a cada pagamento em porcentagem

	def calcula_saldo_final(self, saldo, valor):
		return saldo - valor - (valor * self._taxa)


# Setter
class ConfiguradorDePagamento():
    def set_pagamento(self, novo_pagamento: PagamentoAbstrato):
        pass


# Cliente
class Cliente(ConfiguradorDePagamento):
	def __init__(self, nome, saldo_inicial):
		self.nome = nome
		self._saldo = saldo_inicial
		self._pagamento = None

	def set_pagamento(self, novo_pagamento: PagamentoAbstrato):
		self._pagamento = novo_pagamento

	def recebe(self, valor_recebido):
		self._saldo += valor_recebido

	def paga(self, valor_transferido, destinatario):
		pode_transferir = self._pagamento.transferencia_valida(self._saldo, valor_transferido)
		if (pode_transferir):
			self._saldo = self._pagamento.calcula_saldo_final(self._saldo, valor_transferido)
			destinatario.recebe(valor_transferido)
			print(self.nome, "transfere", valor_transferido, "reais para", destinatario.nome)
		else:
			print(self.nome, "não possui saldo suficiente para transferir", valor_transferido, "reais para", destinatario.nome)

# Injetor
class InjetorDePagamento():
    def __init__(self):
        self._clientes = set()

    def injeta(self, cliente: ConfiguradorDePagamento):
        self._clientes.add(cliente)
        cliente.set_pagamento(PagamentoComDinheiro())

    def muda_todos_para_cartao(self, taxa):
        print("\nTodos os clientes agora pagam com cartão com uma taxa de", f"{taxa * 100}%", )
        for cliente in self._clientes:
            cliente.set_pagamento(PagamentoComCartao(taxa))

    def muda_todos_para_cheque(self, taxa):
        print("\nTodos os clientes agora pagam com cheque com uma taxa fixa de", f"{taxa} reais", )
        for cliente in self._clientes:
            cliente.set_pagamento(PagamentoComCheque(taxa))


# Exemplo de funcionamento
def main():

    injetor = InjetorDePagamento()

    fernando = Cliente("Fernando", 300)
    david = Cliente("David", 200)
    andre = Cliente("André", 100)
    fabio = Cliente("Fabio Kon", 400)

    injetor.injeta(fernando)
    injetor.injeta(david)
    injetor.injeta(andre)
    injetor.injeta(fabio)

    clientes = [fernando, david, andre, fabio]

    print("SALDO INICIAL")
    total_inicial = 0
    for cliente in clientes: 
        print(" ", cliente._saldo, ":", cliente.nome)
        total_inicial += cliente._saldo
    print("Dinheiro total:", total_inicial)
    print()

    david.paga(100, fabio)
    injetor.muda_todos_para_cheque(10)
    andre.paga(100, fabio)
    fabio.paga(40, andre)
    injetor.muda_todos_para_cartao(0.4)
    andre.paga(100, fernando)

    print()
    
    print("SALDO FINAL")
    total_final = 0
    for cliente in clientes:
        print(" ", cliente._saldo, ":", cliente.nome)
        total_final += cliente._saldo
    print("Dinheiro total:", total_final)
    print()

    print("Perdeu-se em taxas:", total_inicial - total_final, "reais")

main()

