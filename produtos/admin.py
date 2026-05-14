from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Produto, Tamanho


# ============================================================
# CATEGORIA
# ============================================================

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display  = ['nome', 'imagem_preview']
    search_fields = ['nome']

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="height:50px; border-radius:50%; object-fit:cover;" />',
                obj.imagem.url
            )
        return '—'
    imagem_preview.short_description = 'Imagem'


# ============================================================
# TAMANHO
# ============================================================

@admin.register(Tamanho)
class TamanhoAdmin(admin.ModelAdmin):
    list_display  = ['valor', 'tipo', 'total_produtos']
    list_filter   = ['tipo']
    search_fields = ['valor']
    ordering      = ['tipo', 'valor']

    def total_produtos(self, obj):
        return obj.produtos.count()
    total_produtos.short_description = 'Produtos com este tamanho'


# ============================================================
# PRODUTO
# ============================================================

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display   = ['nome', 'categoria', 'preco', 'disponivel', 'lista_tamanhos', 'imagem_preview']
    list_filter    = ['categoria', 'disponivel', 'tamanhos__tipo']
    search_fields  = ['nome', 'descricao']
    list_editable  = ['disponivel']
    filter_horizontal = ['tamanhos']   # widget de dupla caixa de seleção para M2M

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'categoria', 'preco', 'disponivel')
        }),
        ('Imagem', {
            'fields': ('imagem',)
        }),
        ('Tamanhos Disponíveis', {
            'fields': ('tamanhos',),
            'description': (
                'Selecione os tamanhos disponíveis para este produto. '
                'Cadastre novos tamanhos em Produtos → Tamanhos antes de vinculá-los aqui.'
            )
        }),
    )

    def lista_tamanhos(self, obj):
        tamanhos = obj.tamanhos.all()
        if not tamanhos:
            return '—'
        return ', '.join(t.valor for t in tamanhos)
    lista_tamanhos.short_description = 'Tamanhos'

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="height:50px; object-fit:cover; border-radius:4px;" />',
                obj.imagem.url
            )
        return '—'
    imagem_preview.short_description = 'Imagem'