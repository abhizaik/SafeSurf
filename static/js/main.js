function showLoadingSpinner() {
    var button = document.querySelector('button');
    button.style.display = 'none';
    var spinner = document.createElement('div');
    spinner.className = 'spinner';
    button.parentNode.appendChild(spinner);
}