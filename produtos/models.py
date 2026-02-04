from django.db import models
from django.urls import reverse

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(
        upload_to = 'categorias/',
        null = True,
        blank = True
    )

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'categorias'

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('produto_detalhe', args=[str(self.id)])

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
