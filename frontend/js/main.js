document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            try {
                const response = await fetch(`http://127.0.0.1:8000/login?username=${username}&password=${password}`, {
                    method: "POST",
                });

                const data = await response.json();

                if (response.status === 200) {
                    // 🟢 Lưu thông tin user vào localStorage
                    localStorage.setItem("user", JSON.stringify(data));
                    window.location.href = "dashboard.html"; // Chuyển sang trang Dashboard
                } else {
                    document.getElementById("error-message").innerText = data.detail;
                }
            } catch (error) {
                console.error("Lỗi kết nối:", error);
                document.getElementById("error-message").innerText = "Không thể kết nối đến server!";
            }
        });
    }
});

