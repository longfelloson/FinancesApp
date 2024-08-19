async function registerUser() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail.msg || 'Registration failed');
        }

        const result = await response.json();
        const access_token = result.access_token;

        document.cookie = `access_token=${access_token}; path=/; SameSite=Lax`;
        window.location.href = '/';
    } catch (error) {
        alert(error.message);  // Используем свойство message вместо msg
    }
}
