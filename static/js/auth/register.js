async function registerUser() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    await fetch('/user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
    });
    try {
        const response = await fetch('/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail[0].msg || 'Login failed');
        }

        const result = await response.json();
        const access_token = result.access_token;

        if (!access_token) {
            throw new Error('Token not found in response');
        }

        document.cookie = `access_token=${access_token}; path=/; SameSite=Lax`;
        window.location.href = '/';
    } catch (error) {
        alert(error.message);
    }
}
