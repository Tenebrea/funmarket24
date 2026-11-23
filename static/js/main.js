(function () {
    const minPrice = document.getElementById('rangeMin');
    const maxPrice = document.getElementById('rangeMax');
    const form = document.getElementById('filters');

    const labelMin = document.querySelector('.price-field.min span');
    const labelMax = document.querySelector('.price-field.max span');

    const rangeFill = document.querySelector('.range-fill');

    if (!minPrice || !maxPrice) return

    const rangeEl = minPrice.closest('.range');
    const lowerBound = Number(rangeEl?.dataset.min ?? minPrice.min);
    const upperBound = Number(rangeEl?.dataset.max ?? maxPrice.max);
    const boundsSpan = upperBound - lowerBound || 1;
    const minGap = Math.min(100, Math.round(boundsSpan / 10));

    function onMinChange(minValue) {
        const maxValue = maxPrice.valueAsNumber;

        if (minValue > maxValue - minGap) {
            minValue = maxValue - minGap;
            minPrice.value = minValue;
        }
        updateSizes();
        updateLabels(maxValue, minValue);
    }
    function onMaxChange(maxValue) {
        const minValue = minPrice.valueAsNumber;

        if (minValue > maxValue - minGap) {
            maxValue = minValue + minGap;
            maxPrice.value = maxValue;
        }
        updateSizes();
        updateLabels(maxValue, minValue);
    }

    function updateLabels(maxValue, minValue) {
        if (labelMax) labelMax.textContent = maxValue;
        if (labelMin) labelMin.textContent = minValue;
    }

    function updateSizes() {
        rangeFill.style.setProperty('--min', `${(minPrice.valueAsNumber - lowerBound) / boundsSpan * 100}%`);
        rangeFill.style.setProperty('--max', `${(maxPrice.valueAsNumber - minPrice.valueAsNumber) / boundsSpan * 100}%`);
    }

    minPrice.addEventListener('input', (event) => {
        onMinChange(event.target.valueAsNumber);
    });

    maxPrice.addEventListener('input', (event) => {
        onMaxChange(event.target.valueAsNumber);
    });

    updateLabels(maxPrice.valueAsNumber, minPrice.valueAsNumber);
    updateSizes();

    if (!form) return;

    form.addEventListener('change', (event) => {
        if (!event.target.matches('input, select')) return;
        form.requestSubmit();
    });
})();

(function () {
    const items = document.querySelectorAll('.carousel-items li');
    const mainImage = document.querySelector('.img-carousel>img');

    items.forEach((element) => element.addEventListener('click', (event) => {
        const img = element.querySelector('img')
        mainImage.src = img.src;
        items.forEach((e) => e.classList.remove('selected'));
        element.classList.add('selected');
    }));
})();

(function () {
    const items = document.querySelectorAll('.product-favorite');
    items.forEach((element) => element.addEventListener('click', (event) => {
        element.toggle = !element.toggle;
        element.src = element.toggle ? element.dataset.full : element.dataset.empty;
        element.alt = element.toggle ? 'Товар в избранном' : 'Товар не в избранном';
    }));
})();

(function () {


    const items = document.querySelectorAll('.product-card-amount');
    items.forEach((element) => {
        const plus = element.querySelector('.plus');
        const minus = element.querySelector('.minus');
        const counter = element.querySelector('p');

        function updateImages() {
            const number = Number(counter.textContent);

            const minusImg = minus.querySelector('img')
            if (number === 0) {
                minusImg.src = minusImg.dataset.empty
            } else {
                minusImg.src = minusImg.dataset.full
            }
            const plusImg = plus.querySelector('img')
            if (number === Number(plus.dataset.stock)) {
                plusImg.src = plusImg.dataset.empty
            } else {
                plusImg.src = plusImg.dataset.full
            }
        }

        updateImages();

        plus.addEventListener('click', (event) => {
            const number = Number(counter.textContent);

            if (number === Number(plus.dataset.stock)) return;

            counter.textContent = number + 1;
            updateImages();
        });

        minus.addEventListener('click', (event) => {
            const number = Number(counter.textContent);
            if (number === 0) return;
            counter.textContent = number - 1;

            updateImages();
        });
    })
})();

(function () {
    const layouts = document.querySelectorAll('.layout div');
    const cards = document.querySelector('.product-cards');
    layouts.forEach((element) => {
        element.querySelector('input').addEventListener('change', function (event) {
            if (this.checked) {
                cards.classList.remove('grid');
                cards.classList.remove('list_with_images');
                cards.classList.remove('list');

                cards.classList.add(this.id);
            }
        });
    });
})();

(function () {
    const sorting = document.querySelector('.sort details');
    const topBar = document.querySelectorAll('.top-bar .dropdown');

    if (sorting) {
        sorting.addEventListener('mouseenter', () => {
            sorting.open = true;
        });

        sorting.addEventListener('mouseleave', () => {
            sorting.open = false;
        });
    }

    topBar.forEach((element) => {
        element.addEventListener('mouseenter', () => {
            topBar.forEach((other) => {
                if (other !== element) other.open = false;
            });
            element.open = true;
        });

        element.addEventListener('mouseleave', () => {
            element.open = false;
        });
    });
})();
(function () {
    const cart = document.querySelector('.cart');
    if (!cart) return;

    const overview = cart.querySelector('.cart-overview');
    const totalValue = cart.querySelector('.cart-total-value');
    const headerLink = document.querySelector('.header-inner .cart-link');
    const headerBadge = headerLink?.querySelector('.badge');
    const headerTotal = headerLink?.querySelector('span:not(.badge)');

    function plural(number) {
        const mod100 = Math.abs(number) % 100;
        if (mod100 >= 11 && mod100 <= 14) return 'товаров';

        const mod10 = mod100 % 10;
        if (mod10 === 1) return 'товар';
        if (mod10 >= 2 && mod10 <= 4) return 'товара';
        return 'товаров';
    }

    function format(number) {
        return number.toLocaleString('ru-RU');
    }

    function recount() {
        let total = 0;
        let count = 0;

        cart.querySelectorAll('.cart-item').forEach((item) => {
            const counter = item.querySelector('.product-card-amount');
            const amount = Number(counter.querySelector('p').textContent);
            const price = Number(counter.dataset.price);
            const bulkPrice = Number(counter.dataset.bulkPrice);

            item.querySelector('.cart-line-total').textContent = format(price * amount) + '₽';
            item.querySelector('.cart-line-total-bulk').textContent = format(bulkPrice * amount) + '₽';

            total += price * amount;
            count += amount;
        });

        if (overview) {
            overview.innerHTML = count + ' ' + plural(count) + ' на <span>' + format(total) + '₽</span>';
        }

        if (totalValue) {
            totalValue.textContent = format(total) + '₽';
        }

        if (headerTotal) {
            headerTotal.textContent = format(total) + ' руб.';
        }

        if (headerBadge) {
            headerBadge.textContent = count;
        }
    }

    cart.addEventListener('click', (event) => {
        if (!event.target.closest('.plus, .minus')) return;
        recount();
    });
})();
