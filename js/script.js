(function () {
    const minPrice = document.getElementById('rangeMin');
    const maxPrice = document.getElementById('rangeMax');

    const labelMin = document.querySelector('.price-field.min span');
    const labelMax = document.querySelector('.price-field.max span');
    const minGap = 100;

    const rangeFill = document.querySelector('.range-fill');

    if (!minPrice || !maxPrice) return

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
        labelMax.textContent = maxValue;
        labelMin.textContent = minValue;
    }

    function updateSizes() {
        rangeFill.style.setProperty('--min', `${(minPrice.valueAsNumber - 990) / (5000 - 990) * 100}%`);
        rangeFill.style.setProperty('--max', `${(maxPrice.valueAsNumber - minPrice.valueAsNumber) / (5000 - 990) * 100}%`);
    }

    minPrice.addEventListener('input', (event) => {
        console.log(minPrice.value)
        console.log(maxPrice.value)
        onMinChange(event.target.valueAsNumber);
    });

    maxPrice.addEventListener('input', (event) => {
        console.log(minPrice.value)
        console.log(maxPrice.value)
        onMaxChange(event.target.valueAsNumber);
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