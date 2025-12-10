
document.addEventListener('keydown', function(event) {
    if (event.altKey && event.shiftKey && (event.key === 'c' || event.key === 'C' || event.code === 'KeyC')) {
        window.location.href = window.bdayUrl || '/bday.html';
    }
});
