// Cookies

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Add to favorites

let csrftoken = getCookie('csrftoken');

function addToFavorites() {
    $('.add-to-favorites').each((index, el) => {
        $(el).on('click', function (e) {
            e.preventDefault();
            const type = $(el).data('type');
            const id = $(el).data('id');
            if ($(this).hasClass('added')) {
                $.ajax({
                    url: '/favorites/remove/',
                    type: 'POST',
                    dataType: 'json',
                    headers: {
                        'X-CSRFToken': csrftoken,
                    },
                    data: {
                        type: type,
                        id: id
                    },
                    success: (data) => {
                        $(el).removeClass('added');
                        $(el).html('<i class="bx bx-heart"></i>')
                    }
                })
            } else {
                $.ajax({
                    url: '/favorites/add/',
                    type: 'POST',
                    dataType: 'json',
                    headers: {
                        'X-CSRFToken': csrftoken,
                    },
                    data: {
                        type: type,
                        id: id
                    },
                    success: (data) => {
                        $(el).addClass('added');
                        $(el).html('<i class="bx bxs-heart"></i>');
                    }
                })
            }
        })
    })
}

function get_session_favorites() {
    $.getJSON('/favorites/api/', (json) => {
        if (json !== null) {
            for (let key in json) {
                $('.add-to-favorites').each((index, el) => {
                    const type = $(el).data('type');
                    const id = $(el).data('id');
                    if (type === key && json[key].includes(String(id))) {
                        $(el).addClass('added');
                        $(el).html('<i class="bx bxs-heart"></i>');
                    }
                })
            }
        }
    })
}

function remove_favorites_from_session() {
    $('.remove-from-favorites').each((index, el) => {
        $(el).on('click', function (e) {
            e.preventDefault();
            const type = $(el).data('type');
            const id = $(el).data('id');
            $.ajax({
                url: '/favorites/remove/',
                type: 'POST',
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                data: {
                    type: type,
                    id: id
                },
                success: (data) => {
                    $(el).closest('.col').remove();
                }
            })
        })
    })
}

$(document).ready(function () {
    addToFavorites();
    get_session_favorites();
    remove_favorites_from_session();
})

// Modal product

// get buttons for modal
const modalbtns = document.querySelectorAll('.modal-btn');
const modalContent = document.querySelector(".modal-content");

modalbtns.forEach(a => a.addEventListener('click', () => {
    // get product item modal info
    const modalinfo = a.parentNode.parentNode.childNodes[1];
    const imgLinks = modalinfo.childNodes[3].childNodes;
    const cartForm = document.forms.modal_cart_form;

    createCarousel(imgLinks)
    modalContent.querySelector(".modal-title").textContent = modalinfo.children[1].textContent;
    modalContent.querySelector(".modal-desc").textContent = modalinfo.children[2].textContent;
    modalContent.querySelector(".modal-price").textContent = modalinfo.children[3].textContent;
    modalContent.querySelector(".modal-sku").textContent = modalinfo.children[4].textContent;
    cartForm.action = modalinfo.children[5].textContent;
}));


// Rating

const ratings = document.querySelectorAll('.rating')
if (ratings.length > 0) {
    initRatings();
}

function initRatings() {
    let ratingActive, ratingValue, usersCount;
    for (let i = 0; i < ratings.length; i++) {
        const rating = ratings[i];
        initRating(rating);
    }

    function initRating(rating) {
        initRatingVars(rating);

        setRatingActiveWidth();

        if (rating.classList.contains('rating__set')) {
            setRating(rating);

        }
    }

    function initRatingVars(rating) {
        ratingActive = rating.querySelector('.rating__active');
        ratingValue = rating.querySelector('.rating__value');
    }

    function setRatingActiveWidth(index = ratingValue.innerHTML) {
        const ratingActiveWidth = index / 0.05;
        ratingActive.style.width = `${ratingActiveWidth}%`;
    }

    function setRating(rating) {
        const ratingItems = rating.querySelectorAll('.rating__item');
        for (let i = 0; i < ratingItems.length; i++) {
            const ratingItem = ratingItems[i];
            ratingItem.addEventListener("mouseenter", function (e) {
                initRatingVars(rating);
                setRatingActiveWidth(ratingItem.value);
            });
            ratingItem.addEventListener("mouseleave", function (e) {
                setRatingActiveWidth();
            })
            ratingItem.addEventListener("click", function (e) {
                initRatingVars(rating);

                if (rating.dataset.ajax) {
                    setRatingValue(ratingItem.value, rating);
                } else {
                    ratingValue.innerHTML = i + 1;
                    setRatingActiveWidth();
                }
            })
        }

        async function setRatingValue(value, rating) {
            if (!rating.classList.contains('rating_sending')) {
                rating.classList.add('rating_sending');
                let csrftoken = getCookie('csrftoken')
                let response = await fetch("/ratings/set_rating/", {
                    method: 'POST',
                    mode: 'same-origin',
                    body: JSON.stringify({
                        user_rating: value,
                        product_model: rating.dataset.model,
                        product_id: rating.dataset.id
                    }),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    }
                });
                if (response.ok) {
                    const result = await response.json();

                    ratingValue.innerHTML = result.new_rating;

                    setRatingActiveWidth();
                    rating.classList.remove('rating_sending');
                } else {
                    alert("Error. Rating not sent.")

                    rating.classList.remove('rating_sending');
                }
            }
        }
    }
}

// Highlighting customer's menu items

let a = document.querySelectorAll('.list-group-item')
a.forEach((el) => {
    if (el.getAttribute('href') === window.location.pathname)
        el.classList.add('active')
    el.classList.remove('bg-transparent')
})

// Carousel for modal
function createCarousel(links) {
    $('.image-zoom-section').html('<div id="modal_carousel" class="product-gallery owl-carousel owl-theme border mb-3 p-3" data-slider-id="1"></div><div id="modal_thumbs" class="owl-thumbs d-flex justify-content-center" data-slider-id="1"></div>');
    let owl = $("#modal_carousel");
    let thumbs = $("#modal_thumbs");
    for (let i = 0; i < links.length; i++) {
        owl.append('<div class="item"><img src="' + links[i].textContent + '" alt="" /></div>');
        thumbs.append('<button class="owl-thumb-item"><img src="' + links[i].textContent + '" alt="" /></button>');
    }
    owl.owlCarousel({
        loop: true,
        margin: 10,
        responsiveClass: true,
        nav: false,
        dots: false,
        thumbs: true,
        thumbsPrerendered: true,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 1
            },
            1000: {
                items: 1
            }
        }
    });

    $(function () {
        "use strict";


        new PerfectScrollbar('.cart-list');

        // jquery ready start
        $(document).ready(function () {
            // jQuery code
            $("[data-trigger]").on("click", function (e) {
                e.preventDefault();
                e.stopPropagation();
                var offcanvas_id = $(this).attr('data-trigger');
                $(offcanvas_id).toggleClass("show");
                $('body').toggleClass("offcanvas-active");
                $(".screen-overlay").toggleClass("show");
            });

            // Close menu when pressing ESC
            $(document).on('keydown', function (event) {
                if (event.keyCode === 27) {
                    $(".mobile-offcanvas").removeClass("show");
                    $("body").removeClass("overlay-active");
                }
            });

            $(".btn-close, .screen-overlay").click(function (e) {
                $(".screen-overlay").removeClass("show");
                $(".mobile-offcanvas").removeClass("show");
                $("body").removeClass("offcanvas-active");
            });
        });
        // jquery end

        $('.dropdown-menu a.dropdown-toggle').on('click', function (e) {
            if (!$(this).next().hasClass('show')) {
                $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
            }
            var $subMenu = $(this).next(".dropdown-menu");
            $subMenu.toggleClass('show');


            $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function (e) {
                $('.submenu .show').removeClass("show");
            });


            return false;
        });


        $(document).ready(function () {
            $(window).on("scroll", function () {
                $(this).scrollTop() > 300 ? $(".back-to-top").fadeIn() : $(".back-to-top").fadeOut()
            }), $(".back-to-top").on("click", function () {
                return $("html, body").animate({
                    scrollTop: 0
                }, 600), !1
            })
        }),


            $(".btn-mobile-filter").on("click", function () {
                $(".filter-sidebar").removeClass("d-none")
            }),

            $(".btn-mobile-filter-close").on("click", function () {
                $(".filter-sidebar").addClass("d-none")
            }),


            $(".switcher-btn").on("click", function () {
                $(".switcher-wrapper").toggleClass("switcher-toggled")
            }),

            $(".close-switcher").on("click", function () {
                $(".switcher-wrapper").removeClass("switcher-toggled")
            }),


            $('#theme1').click(theme1);
        $('#theme2').click(theme2);
        $('#theme3').click(theme3);
        $('#theme4').click(theme4);
        $('#theme5').click(theme5);
        $('#theme6').click(theme6);
        $('#theme7').click(theme7);
        $('#theme8').click(theme8);
        $('#theme9').click(theme9);
        $('#theme10').click(theme10);
        $('#theme11').click(theme11);
        $('#theme12').click(theme12);
        $('#theme13').click(theme13);
        $('#theme14').click(theme14);
        $('#theme15').click(theme15);

        function theme1() {
            $('body').attr('class', 'bg-theme bg-theme1');
        }

        function theme2() {
            $('body').attr('class', 'bg-theme bg-theme2');
        }

        function theme3() {
            $('body').attr('class', 'bg-theme bg-theme3');
        }

        function theme4() {
            $('body').attr('class', 'bg-theme bg-theme4');
        }

        function theme5() {
            $('body').attr('class', 'bg-theme bg-theme5');
        }

        function theme6() {
            $('body').attr('class', 'bg-theme bg-theme6');
        }

        function theme7() {
            $('body').attr('class', 'bg-theme bg-theme7');
        }

        function theme8() {
            $('body').attr('class', 'bg-theme bg-theme8');
        }

        function theme9() {
            $('body').attr('class', 'bg-theme bg-theme9');
        }

        function theme10() {
            $('body').attr('class', 'bg-theme bg-theme10');
        }

        function theme11() {
            $('body').attr('class', 'bg-theme bg-theme11');
        }

        function theme12() {
            $('body').attr('class', 'bg-theme bg-theme12');
        }

        function theme13() {
            $('body').attr('class', 'bg-theme bg-theme13');
        }

        function theme14() {
            $('body').attr('class', 'bg-theme bg-theme14');
        }

        function theme15() {
            $('body').attr('class', 'bg-theme bg-theme15');
        }
    })
}
