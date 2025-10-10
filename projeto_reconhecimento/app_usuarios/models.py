from django.db import models

class Reu(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    foto = models.ImageField(upload_to='fotos_reus/')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    telefone = models.CharField(max_length=12, null=True)
    num_processo = models.CharField(max_length=30, null=True)
    endereco = models.CharField(max_length=200, null=True, default='SOME STRING')
    data_expiracao = models.DateField(null=True, blank=True, default=None)

    def __str__(self):
        return self.nome

class Presenca(models.Model):
    reu = models.ForeignKey(Reu, on_delete=models.CASCADE)
    data_presenca = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reu.nome} - {self.data_presenca}"

