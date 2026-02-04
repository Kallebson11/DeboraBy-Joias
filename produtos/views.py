from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Produto, Categoria
from cart.models import Cart

# View temporária para testar
def index(request):
    # Verifica se há filtro de categoria na URL
    categoria_id = request.GET.get('categoria')

    # Verifica se há busca na URL
    busca = request.GET.get('busca', '').strip()

    # Inicializa variáveis
    produtos = Produto.objects.all()
    buscando = False
    busca_realizada = False  # Nova variável para controlar se busca foi feita
    
    # Aplica filtro de busca se existir
    if busca:
        busca_realizada = True  # Usuário tentou buscar
        produtos_buscados = produtos.filter(nome__icontains=busca)
        
        if produtos_buscados.exists():
            # Se encontrou produtos, usa eles
            produtos = produtos_buscados
            buscando = True
        else:
            # Se NÃO encontrou, produtos fica VAZIO
            produtos = Produto.objects.none()  # QuerySet vazio
            buscando = True
    
    # Se tiver filtro, busca produtos daquela categoria
    if categoria_id and categoria_id != 'todas' and not buscando:
        try:
            categoria = Categoria.objects.get(id=categoria_id)
            produtos = Produto.objects.filter(categoria=categoria)
            categoria_filtrada = categoria
        except (Categoria.DoesNotExist, ValueError):
            # Se categoria não existir, mostra todos produtos
            categoria_filtrada = None
    else:
        # Sem filtro ou "todas", mostra todos produtos
        categoria_filtrada = None
    
    # Busca todas categorias para o menu
    categorias = Categoria.objects.all()
    
    context = {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_filtrada': categoria_filtrada,
        'busca': busca,
        'buscando': buscando,
        'busca_realizada': busca_realizada,
    }
    
    return render(request, 'index.html', context)

def produto_detalhe(request, produto_id):


    
    # Busca o produto pelo ID ou mostra erro 404 se não existir
    produto = get_object_or_404(Produto, id=produto_id)

    # Pode buscar produtos relacionados (da mesma categoria)
    produtos_relacionados = Produto.objects.filter(
        categoria = produto.categoria
    ).exclude(id = produto.id)[:4]


    cart_obj, new_obj = Cart.objects.new_or_get(request)

    context = {
        'produto': produto,
        'produtos_relacionados': produtos_relacionados,
        'cart': cart_obj,  # ADICIONE ESTA LINHA
    }
    
    return render(request, 'produtos_detalhes.html', context)



