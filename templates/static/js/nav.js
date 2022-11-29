const btnNav = document.getElementById('hamburger')

function toggleMenu(){
    const nav = document.getElementById('nav')
    const lista = document.getElementById('nav-list')
    const search = document.getElementById('form')
    nav.classList.toggle('active')
    lista.classList.toggle('active')
    form.classList.toggle('active')
}

btnNav.addEventListener('click', toggleMenu)