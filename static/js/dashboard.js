document.addEventListener('DOMContentLoaded', function () {
    // Ensure that the form and checkbox exist before adding the event listener
    const addStockForm = document.getElementById('addStockForm');
    const yahooFinanceToggle = document.getElementById('yahooFinance');

    if (addStockForm && yahooFinanceToggle) {
        addStockForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent the default form submission

            // Get the value of the toggle switch
            const yahooFinanceToggleValue = yahooFinanceToggle.checked ? 'on' : 'off';

            // Create a hidden input to store the toggle value
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'yahooFinance';
            hiddenInput.value = yahooFinanceToggleValue;

            // Append the hidden input to the form
            addStockForm.appendChild(hiddenInput);
            console.log("The Add Stock Form: ${addStockForm}")

            // Submit the form
            addStockForm.submit();
        });
    }
});