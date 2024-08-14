async function loginUser(){
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail[0].msg);
        }

        const data = await response.json();
        document.cookie = `access_token=${data.access_token}; path=/; SameSite=Lax`;
        window.location.href = '/';
    } catch (error) {
        alert(error.message);
    }
}
