document.addEventListener("DOMContentLoaded", function () {

    const search = document.querySelector(".form-control");

    const cards = document.querySelectorAll(".col-md-4");

    if (search) {
        search.addEventListener("keyup", function () {

            const value = search.value.toLowerCase();

            cards.forEach(card => {

                const text = card.innerText.toLowerCase();

                if(text.includes(value))
                    card.style.display="block";
                else
                    card.style.display="none";

            });

        });
    }

    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        if (window.bootstrap && bootstrap.Tooltip) {
            new bootstrap.Tooltip(tooltipTriggerEl);
        }
    });

});