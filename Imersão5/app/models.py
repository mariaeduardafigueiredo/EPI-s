from datetime import datetime, timedelta
from django.db import models
from app.enums import TIPO_USUARIO, CATEGORIA_EPI, CARGOS

def devolucao_padrao():
    return datetime.now() + timedelta(days=10)


class Usuario(models.Model):
    
    # Colunas
    nome = models.CharField(max_length=255)
    login = models.CharField(max_length=255)
    senha = models.CharField(max_length=60)
    tipo = models.CharField(max_length=60, choices=TIPO_USUARIO)
    cargo = models.CharField(max_length=60, choices=CARGOS)
    data_admissao = models.DateTimeField(default=datetime.now)


    def __str__(self) -> str:
        return self.nome
    

class Equipamento(models.Model):

    # Colunas 
    nome = models.CharField(max_length=100)
    quantidade_total = models.IntegerField(default=0)  # Novo campo para a quantidade total
    quantidade_disponivel = models.IntegerField(default=0)  # Novo campo para a quantidade disponível
    validade = models.DateField()
    categoria = models.CharField(max_length=100, choices=CATEGORIA_EPI)
def save(self, *args, **kwargs):  # Corrigido: use *args, **kwargs
        # Para um novo registro, a quantidade disponível será igual à quantidade total
        if not self.pk:
            self.quantidade_disponivel = self.quantidade_total
        else:
            # Para registros existentes, calcular a quantidade disponível com base na quantidade total
            # e subtraindo a quantidade emprestada
            quantidade_emprestada = sum(
                emprestimo.quantidade
                for emprestimo in self.emprestimo_set.filter(status='pendente')
            )
            self.quantidade_disponivel = self.quantidade_total - quantidade_emprestada

        super().save(*args, **kwargs)

class Emprestimo(models.Model):

    # Colunas
    data_emprestimo = models.DateTimeField(default=datetime.now)
    data_devolucao = models.DateTimeField(default=devolucao_padrao)
    quantidade = models.PositiveIntegerField(default=1)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.data_emprestimo)
    