async function createOperation() {
    const amount = document.getElementById('amount').value;
    const name = document.getElementById('name').value;

    const balanceData = {
        amount: amount,
    };

    try {
        const balanceResponse = await fetch('/user-balance', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(balanceData)
        });

        if (!balanceResponse.ok) {
            if (balanceResponse.status === 401) {
                window.location.href = '/login';
                return;
            }
            const data = await balanceResponse.json();
            throw new Error(data.detail[0].msg);
        }

        const requestData = {
            amount: amount,
            name: name,
        };

        const response = await fetch('/operations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            const data = await response.json();
            throw new Error(data.detail[0].msg);
        }

        alert("Операция добавлена!");

    } catch (error) {
        alert(error.message);
    }
}
