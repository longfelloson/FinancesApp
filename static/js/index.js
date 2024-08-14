document.addEventListener('DOMContentLoaded', async function () {
    try {
        const balanceResponse = await fetch('/user-balance');
        if (!balanceResponse.ok) {
            if (balanceResponse.status === 401) {
                window.location.href = '/login';
                return;
            }
            throw new Error('Ошибка получения баланса: ' + balanceResponse.statusText);
        }
        const userBalance = await balanceResponse.json();
        document.getElementById('balance-amount').innerText = userBalance.balance;

        const operationsResponse = await fetch('/operations');
        if (!operationsResponse.ok) {
            if (operationsResponse.status === 401) {
                window.location.href = '/login';
                return;
            }
            throw new Error('Ошибка получения операций: ' + operationsResponse.statusText);
        }
        const operationsData = await operationsResponse.json();
        const operationsList = document.getElementById('operations-list');

        operationsData.forEach(operation => {
            const operationDiv = document.createElement('div');
            operationDiv.className = 'operation';

            if (operation.type_ === 'expense') {
                operationDiv.style.border = '2px solid red';
            } else if (operation.type_ === 'income') {
                operationDiv.style.border = '2px solid green';
            }

            const operationDate = new Date(operation.created_at).toLocaleDateString();

            operationDiv.innerHTML = `<span>${operation.name}</span><span>${operation.amount}</span><span>${operationDate}</span>`;
            operationsList.appendChild(operationDiv);
        });

        document.getElementById('toggle-operations').addEventListener('click', function () {
            const operations = document.getElementById('operations');
            if (operations.style.display === 'none' || operations.style.display === '') {
                operations.style.display = 'block';
                this.innerHTML = '&#9650;';
            } else {
                operations.style.display = 'none';
                this.innerHTML = '&#9660;';
            }
        });
    } catch (error) {
        console.error(error.message);
    }
});
