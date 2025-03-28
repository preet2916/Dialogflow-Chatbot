document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box"); // ✅ Fixed ID issue
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");

    // ✅ Capture user input when button is clicked
    sendButton.addEventListener("click", sendMessage);

    // ✅ Capture user input when 'Enter' is pressed
    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return;

        // ✅ Display user message in chat window
        appendMessage("user", message);
        
        // ✅ Send user message to FastAPI server
        fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: "12345", message: message }),
        })
        .then(response => response.json())
        .then(data => {
            // ✅ Display chatbot response
            appendMessage("bot", data.reply);
        })
        .catch(error => {
            console.error("Error:", error);
            appendMessage("bot", "⚠️ Error: Unable to connect to chatbot.");
        });

        // ✅ Clear input field after sending
        userInput.value = "";
    }

    function appendMessage(sender, text) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);
        messageDiv.innerText = text;
        chatBox.appendChild(messageDiv); // ✅ Fixed ID reference

        // ✅ Auto-scroll to the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
