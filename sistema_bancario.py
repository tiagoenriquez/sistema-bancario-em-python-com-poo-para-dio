from abc import ABC, abstractmethod
from datetime import datetime


class Transacao(ABC):

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):

    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        conta.historico.adicionar_transacao(self)


class Saque(Transacao):

    def registrar(self, conta):
        conta.historico.adicionar_transacao(self)

    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor


class Historico:

    def __init__(self):
        self._transacoes: list[Transacao] = []
    
    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

    def __str__(self):
        retorno = "\n *** Histórico de Transações ***\n\n"
        for transacao in self._transacoes:
            retorno += f"{transacao.__class__.__name__} --> Valor: {transacao.valor}\n"
        retorno += "\n"
        return retorno


class Conta:

    def __init__(self, numero, agencia, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def clientes(self):
        return self._clientes
    
    @property
    def historico(self):
        return self._historico
    
    @property
    def saldo(self):
        return self._saldo
    
    @staticmethod
    def nova_conta(numero, agencia, cliente):
        conta = Conta(numero, agencia, cliente)
        cliente.adicionar_conta(conta)
        return conta
    
    def sacar(self, valor):
        if self._saldo < valor:
            print("Saldo insuficiente")
            return False
        if valor <= 0:
            print("Valor inválido")
            return 0
        self._saldo -= valor
        saque = Saque(valor)
        self._cliente.realizar_transacao(self, saque)
        return True
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            deposito = Deposito(valor)
            self._cliente.realizar_transacao(self, deposito)
            return True
        else:
            print("Valor inválido")
            return False


class ContaCorrente(Conta):

    def __init__(self, numero, agencia, cliente, limite, limite_saques):
        super().__init__(numero, agencia, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques = 0
    
    @staticmethod
    def nova_conta(numero, agencia, cliente, limite, limite_saques):
        conta_corrente = ContaCorrente(numero, agencia, cliente, limite, limite_saques)
        cliente.adicionar_conta(conta_corrente)
        return conta_corrente
    
    def sacar(self, valor):
        if self._saldo < valor:
            print("Saldo insuficiente")
            return False
        if valor <= 0:
            print("Valor inválido")
            return False
        if valor > self._limite:
            print("Valor acima do limite para saque")
            return False
        if self._limite_saques <= self._saques:
            print("Limite de saques diário estourado")
            return False
        self._saldo -= valor
        saque = Saque(valor)
        self._cliente.realizar_transacao(self, saque)
        self._saques += 1
        return True


class Cliente:

    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []
    
    @property
    def endereco(self):
        return self._endereco
    
    @property
    def contas(self):
        return self._contas
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):

    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nascimento(self):
        return self._data_nascimento
