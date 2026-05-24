from django.db import models
from users_app.models import Motorista

class Veiculo(models.Model):
    """ 
        Modelo de Veículo para o sistema de gestão de frotas.
        - motorista: Motorista responsável pelo veículo (pode ser nulo se o veículo não estiver atribuído a um motorista específico).
        - marca: Marca do veículo (ex: Ford, Toyota).
        - modelo: Modelo do veículo (ex: Fiesta, Corolla).
        - ano: Ano de fabricação do veículo.
        - placa: Placa do veículo (única).
        - tipo: Tipo do veículo (ex: carro, caminhão, moto).
        - status: Status do veículo (ex: ativo, em manutenção, desativado).
        - km_atual: Quilometragem atual do veículo.
    """
    motorista = models.ForeignKey(Motorista, on_delete=models.SET_NULL, null=True, blank=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    placa = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=50) # carro, caminhão, moto…
    status = models.CharField(max_length=20) # ativo, em manutenção, desativado
    km_atual = models.IntegerField()

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"

class Manutencao(models.Model):
    """
        Modelo de Manutenção para o sistema de gestão de frotas.
        - veiculo: Veículo associado à manutenção.
        - data: Data da manutenção.
        - descricao: Descrição detalhada da manutenção realizada.
        - custo: Custo total da manutenção.
    """
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data = models.DateField()
    descricao = models.TextField()
    custo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Manutenção do {self.veiculo} em {self.data}"

class Abastecimento(models.Model):
    """ 
        Modelo de Abastecimento para o sistema de gestão de frotas.
        - veiculo: Veículo associado ao abastecimento.
        - data: Data do abastecimento.
        - litros: Quantidade de litros abastecidos.
        - custo: Custo total do abastecimento.
    """
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data = models.DateField()
    litros = models.DecimalField(max_digits=10, decimal_places=2)
    custo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Abastecimento do {self.veiculo} em {self.data}"

class Rotas(models.Model): # rotas
    """
        Modelo de Rotas para o sistema de gestão de frotas.
        - veiculo: Veículo associado à rota.
        - motorista: Motorista responsável pela rota (pode ser nulo se o veículo não estiver atribuído a um motorista específico).
        - data_inicio: Data e hora de início da rota.
        - data_fim: Data e hora de término da rota.
        - origem: Local de origem da rota.
        - destino: Local de destino da rota.
        - km_inicial: Quilometragem do veículo no início da rota.
        - km_final: Quilometragem do veículo no final da rota.
    """
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    motorista = models.ForeignKey(Motorista, on_delete=models.SET_NULL, null=True, blank=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    origem = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    km_inicial = models.IntegerField()
    km_final = models.IntegerField()

    def __str__(self):
        return f"Viagem do {self.veiculo} de {self.origem} para {self.destino}"

class Metricas(models.Model):
    """
        Modelo de Métricas para o sistema de gestão de frotas.
        - veiculo: Veículo associado às métricas.
        - data: Data das métricas.
        - consumo_medio: Consumo médio do veículo (km/l).
        - custo_medio: Custo médio por km rodado.
    """
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data = models.DateField()
    consumo_medio = models.DecimalField(max_digits=10, decimal_places=2)
    custo_medio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Métricas do {self.veiculo} em {self.data}"

