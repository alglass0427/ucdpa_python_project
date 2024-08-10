document.addEventListener('DOMContentLoaded', function () {
    console.log("Inside the Function")
    // Ensure that the form and checkbox exist before adding the event listener
    const addStockForm = document.getElementById('addStockForm');
    const yahooFinanceToggle = document.getElementById('yahooFinance');
    console.log(addStockForm)
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


// const jsonFilePath  = "static/json/tickers.json"
// Populate Dropdown for Demo Purpose
        document.addEventListener('DOMContentLoaded', function () {
            // Path to your JSON file
            const jsonFilePath  = "static/json/tickers";
        //    \static\json\tickers
            // Fetch the JSON file
            fetch(jsonFilePath)
                .then(response => response.json())
                .then(data => populateDropdown(data))
                .catch(error => console.error('Error loading JSON:', error));
            
            function populateDropdown(stocks) {
                console.log(stocks)
                const dropdown = document.getElementById('stockDropdown');
        
                // Iterate over the stocks and create an option element for each
                stocks.forEach(stock => {
                    console.log(stock)
                    const option = document.createElement('option');
                    option.value = stock.ticker; // Ticker as value
                    option.text = `${stock.ticker}`; // Display name with ticker
        
                    dropdown.appendChild(option); // Add option to dropdown
                });
            }
        });
        