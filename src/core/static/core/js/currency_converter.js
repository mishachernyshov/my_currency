const updateInputs = (formContainer) => {
    const inputs = formContainer.querySelectorAll('input:not([type="button"]), select');
    inputs.forEach(input => {
        const updatingAttributes = ['name', 'id'];
        updatingAttributes.forEach(attribute => {
            const attributeValue = input.getAttribute(attribute);
            if (attributeValue) {
                const match = attributeValue.match(/-(\d+)-/);
                const updatedValue = attributeValue.replace(match[0], `-${parseInt(match[1]) + 1}-`);
                if (match) {
                    input.setAttribute(attribute, updatedValue);
                }
            }
        });
        input.value = '';
    });
};

const updateLabels = (formContainer) => {
    const labels = formContainer.querySelectorAll('label');
    labels.forEach(input => {
        const forValue = input.getAttribute('for');
        if (forValue) {
            const match = forValue.match(/-(\d+)-/);
            const updatedForValue = forValue.replace(match[0], `-${parseInt(match[1]) + 1}-`);
            if (match) {
                input.setAttribute('for', updatedForValue);
            }
        }
    });
};

const rotateConversionImage = (conversionImage, currentAngle = 0, rotationAngle = 0.8) => {
    const updatedAngle = (currentAngle + rotationAngle) % 360;
    conversionImage.style.transform = `rotate(${updatedAngle}deg)`;
    requestAnimationFrame(() => rotateConversionImage(conversionImage, updatedAngle));
};

const handleDeleteExchangedCurrencyBtnClick = (event) => {
    event.preventDefault();
    event.target.closest('.exchanged-currency-form').remove();
    const maxNumFormsInput = document.querySelector('input[name="form-TOTAL_FORMS"]');
    maxNumFormsInput.value = parseInt(maxNumFormsInput.value) - 1;
};

const handleAddExchangedCurrencyBtnClick = (event) => {
    const exchangedCurrencyForms = document.querySelectorAll('.exchanged-currency-form');
    const lastExchangedCurrencyForm = exchangedCurrencyForms[exchangedCurrencyForms.length - 1];

    const newExchangedCurrencyForm = lastExchangedCurrencyForm.cloneNode(true);
    const newFormDeleteButton = newExchangedCurrencyForm.querySelector('.delete-exchanged-currency-btn');
    newFormDeleteButton?.classList.remove('hidden');

    updateInputs(newExchangedCurrencyForm);
    updateLabels(newExchangedCurrencyForm);

    lastExchangedCurrencyForm.after(newExchangedCurrencyForm);

    const maxNumFormsInput = document.querySelector('input[name="form-TOTAL_FORMS"]');
    maxNumFormsInput.value = parseInt(maxNumFormsInput.value) + 1;
};

const handleConvertBtnClick = () => {
    const conversionImage = document.getElementById('convert-img');
    rotateConversionImage(conversionImage);
};

document.addEventListener('click', function (event) {
    if (event.target.classList.contains('delete-exchanged-currency-btn')) {
        handleDeleteExchangedCurrencyBtnClick(event);
    } else if (event.target.id === 'add-exchanged-currency') {
        handleAddExchangedCurrencyBtnClick(event);
    } else if (event.target.id === 'convert-btn') {
        handleConvertBtnClick();
    }
});
