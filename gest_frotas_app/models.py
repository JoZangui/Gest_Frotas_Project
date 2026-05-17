from django.db import models

class Motorista(models.Model):
    nome = models.CharField(max_length=100)
    cnh = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    motorista = models.ForeignKey('Motorista', on_delete=models.SET_NULL, null=True, blank=True)
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
    veiculo = models.ForeignKey('Veiculo', on_delete=models.CASCADE)
    data = models.DateField()
    descricao = models.TextField()
    custo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Manutenção do {self.veiculo} em {self.data}"

class Abastecimento(models.Model):
    veiculo = models.ForeignKey('Veiculo', on_delete=models.CASCADE)
    data = models.DateField()
    litros = models.DecimalField(max_digits=10, decimal_places=2)
    custo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Abastecimento do {self.veiculo} em {self.data}"

class Viagem(models.Model):
    veiculo = models.ForeignKey('Veiculo', on_delete=models.CASCADE)
    motorista = models.ForeignKey('Motorista', on_delete=models.SET_NULL, null=True, blank=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    origem = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    km_inicial = models.IntegerField()
    km_final = models.IntegerField()

    def __str__(self):
        return f"Viagem do {self.veiculo} de {self.origem} para {self.destino}"
