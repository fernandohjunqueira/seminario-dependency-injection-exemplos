# Exemplo com Injeção de Dependência no Construtor

# Serviço
class PagamentoComCartao():
    def __init__(self, taxa):
        self._taxa = taxa # Valor da taxa cobrada a cada pagamento em porcentagem

    def transferencia_valida(self, saldo, valor):
        saldo_final = self.calcula_saldo_final(saldo, valor)
        if (saldo_final >= 0):
            return True
        else:
            return False

    def calcula_saldo_final(self, saldo, valor):
        return saldo - valor - (valor * self._taxa)
        
# Cliente
class Cliente():
    def __init__(self, nome, saldo_inicial, pagamento: PagamentoComCartao):
        self.nome = nome
        self._saldo = saldo_inicial
        self._pagamento = pagamento

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


# Exemplo de funcionamento
def main():
    pagamento_bradesco = PagamentoComCartao(0.2)
    pagamento_nubank = PagamentoComCartao(0)

    fernando = Cliente("Fernando", 300, pagamento_nubank)
    david = Cliente("David", 200, pagamento_nubank)
    andre = Cliente("André", 100, pagamento_nubank)
    fabio = Cliente("Fabio Kon", 400, pagamento_bradesco)
   
    clientes = [fernando, david, andre, fabio]

    print("SALDO INICIAL")
    total_inicial = 0
    for cliente in clientes: 
        print(" ", cliente._saldo, ":", cliente.nome)
        total_inicial += cliente._saldo
    print("Dinheiro total:", total_inicial)
    print()

    fernando.paga(50, david)
    david.paga(50, fernando)
    fabio.paga(380, andre)
    fabio.paga(50, andre)
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
