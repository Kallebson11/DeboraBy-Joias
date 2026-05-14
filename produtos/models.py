from django.db import models
from django.urls import reverse


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(
        upload_to='categorias/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']


class Tamanho(models.Model):

    TIPO_CHOICES = [
        ('anel',     'Anel (número)'),
        ('colar',    'Colar (cm)'),
        ('pulseira', 'Pulseira (cm)'),
        ('brinco',   'Brinco (tamanho)'),
        ('geral',    'Geral (P/M/G)'),
    ]

    valor = models.CharField(
        max_length=20,
        verbose_name='Valor',
        help_text='Ex: 15, 17, 19 (para colares/pulseiras) ou P, M, G'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='geral',
        verbose_name='Tipo'
    )

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.valor}'

    class Meta:
        verbose_name = 'Tamanho'
        verbose_name_plural = 'Tamanhos'
        ordering = ['tipo', 'valor']
        unique_together = ('valor', 'tipo')


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='produtos'
    )
    disponivel = models.BooleanField(default=True)

    # ⬇️ TAMANHOS disponíveis para este produto
    tamanhos = models.ManyToManyField(
        Tamanho,
        blank=True,
        related_name='produtos',
        verbose_name='Tamanhos disponíveis',
        help_text='Selecione os tamanhos disponíveis para este produto'
    )

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('produto_detalhe', args=[str(self.id)])

    def tem_tamanhos(self):
        """Retorna True se o produto tiver pelo menos um tamanho cadastrado"""
        return self.tamanhos.exists()

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']