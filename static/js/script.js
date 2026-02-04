document.addEventListener('DOMContentLoaded', function() {
    const categoryList = document.querySelector('.category-list');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    
    // Largura aproximada de cada item (110px + margens)
    const itemWidth = 112;
    
    prevBtn.addEventListener('click', function() {
        categoryList.scrollBy({
            left: -itemWidth * 3, // Move 3 itens por clique
            behavior: 'smooth'
        });
    });
    
    nextBtn.addEventListener('click', function() {
        categoryList.scrollBy({
            left: itemWidth * 3, // Move 3 itens por clique
            behavior: 'smooth'
        });
    });
    
    // Desabilita o scroll com a roda do mouse (opcional)
    categoryList.addEventListener('wheel', function(e) {
        e.preventDefault();
    }, { passive: false });
});
