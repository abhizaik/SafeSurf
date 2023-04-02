function showLoadingSpinner() {
    var input = document.querySelector('input[name="url"]');
    var button = document.querySelector('button');
    if (input.value.trim() !== '') {
        button.style.display = 'none';
        var spinner = document.createElement('div');
        spinner.className = 'spinner';
        button.parentNode.appendChild(spinner);
    }
}