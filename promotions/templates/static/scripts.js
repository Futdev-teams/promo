document.getElementById('search').addEventListener('input', function() {
    const searchValue = this.value.toLowerCase();
    const entreprises = document.querySelectorAll('.bg-white');

    entreprises.forEach(entreprise => {
        const nom = entreprise.querySelector('h2').textContent.toLowerCase();
        if (nom.includes(searchValue)) {
            entreprise.style.display = 'block';
        } else {
            entreprise.style.display = 'none';
        }
    });
});