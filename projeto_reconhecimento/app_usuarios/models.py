from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)  # Formato: 000.000.000-00
    foto = models.ImageField(upload_to='fotos_usuarios/')
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Presenca(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_presenca = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nome} - {self.data_presenca}"

