from django.contrib import admin
from .models import Categoria, Produto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'imagem']
    readonly_fields = ['imagem_preview']

    def imagem_preview(self, obj):
        if obj.imagem:
            return f'<img src="{obj.imagem.url}" style="max-height: 100px;" />'
        return "Sem imagem"
    imagem_preview.allow_tags = True
    imagem_preview.short_description = 'Pré-visualização'

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'categoria', 'disponivel']
    list_filter = ['categoria', 'disponivel']
    search_fields = ['nome', 'descricao']



