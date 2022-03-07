difference = document.querySelectorAll('.difference');

difference.forEach(element => {
    if (parseInt(element.textContent) > 0) {
        element.style.color = 'green';
    }
    else {
        element.style.color = 'red';
    }
});
