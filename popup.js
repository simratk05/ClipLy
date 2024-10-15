document.getElementById("save").addEventListener("click", () => {
  const title = document.getElementById("title").value;

  if (title) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const url = tabs[0].url;

      fetch("http://127.0.0.1:8000/save_bookmark", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url, title: title }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          if (data.status === "success") {
            alert("Bookmark saved successfully!");
          } else {
            alert("Failed to save bookmark: " + JSON.stringify(data.errors));
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("An error occurred while saving the bookmark.");
        });
    });
  } else {
    alert("Please enter a title for the bookmark.");
  }
});
