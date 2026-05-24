from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Motorista(models.Model):
    """ 
        Modelo de Motorista para o sistema de gestão de frotas.
        - nome: Nome completo do motorista.
        - cnh: Número da Carteira Nacional de Habilitação (CNH) do motorista (único).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='motorista_profile')
    nome = models.CharField(max_length=100)
    cnh = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    """ 
        Modelo de Funcionário para o sistema de gestão de frotas.
        - nome: Nome do funcionário.
        - endereco: Endereço do funcionário.
        - telefone: Número de telefone do funcionário.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='funcionario_profile')
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome
