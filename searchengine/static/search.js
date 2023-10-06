$(document).ready(function() {
    $('#query').autoComplete({
        minLength: 2,
        bootstrapVersion: '4',
        noResultsText: "",
        resolverSettings: {
            fail: function() {},
            requestThrottling: 100
        }
    });

    $('#form-search').on('click', '.bootstrap-autocomplete a', function() {
        $('#form-search').submit();
    });

    $('#query').on('click', function() {
        $('#query').autoComplete('show');
    });

    $(window).resize(function(){
        pos = document.getElementById('query').getBoundingClientRect();
        autoCmpElem = document.getElementsByClassName('bootstrap-autocomplete')[0];
        if (autoCmpElem) {
            autoCmpElem.style.top = `${pos.bottom}px`;
            autoCmpElem.style.left = `${pos.left}px`;
            autoCmpElem.style.width = `${pos.width}`;
        }
    });
});

const toTop = document.querySelector(".to-top");
window.addEventListener("scroll", () =>{
    if (window.pageYOffset > 100) {
        toTop.classList.add("active");
    } else {
        toTop.classList.remove("active");
    }
})