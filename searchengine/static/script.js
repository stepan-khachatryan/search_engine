function truncateTextOnMobile() {
    const windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    const elementsToTruncate = document.querySelectorAll('.body');

    elementsToTruncate.forEach(element => {
        if (windowWidth < 767) {
            let truncatedText = element.textContent;
            if (truncatedText.length > 100) {
                truncatedText = truncatedText.substring(0, 240) + '...';
                element.textContent = truncatedText;
            }
        } else {
            const fullText = element.getAttribute('data-full-text');
            if (fullText) {
                element.textContent = fullText;
            }
        }
    });
}

document.querySelectorAll('.body').forEach(element => {
    element.setAttribute('data-full-text', element.textContent);
});
window.addEventListener('load', truncateTextOnMobile);
window.addEventListener('resize', truncateTextOnMobile);