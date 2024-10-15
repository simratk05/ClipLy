document.getElementById("login").addEventListener("click", () => {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (username && password) {
    fetch("http://127.0.0.1:8000/my-login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: username, password: password }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.token) {
          // Store the JWT token using chrome.storage.local
          chrome.storage.local.set({ jwt_token: data.token }, function () {
            alert("Login successful!");
            // Optionally, you can redirect the user to another page or popup
          });
        } else {
          alert("Login failed: " + data.error);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred during login.");
      });
  } else {
    alert("Please enter both username and password.");
  }
});
