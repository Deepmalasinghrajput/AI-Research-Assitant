const chat = document.getElementById("chat");
const input = document.getElementById("input");

input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

function addMessage(text, type) {
    const div = document.createElement("div");
    div.className = "msg " + type;
    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    // 🔥 HIDE EMPTY MESSAGE
    const empty = document.getElementById("empty");
    if (empty) empty.style.display = "none";

    // USER MESSAGE
    addMessage(text, "user");
    input.value = "";

    // LOADING MESSAGE (better text)
    const loading = document.createElement("div");
    loading.className = "msg bot";
    loading.innerText = "🔎 Searching and generating report...";
    chat.appendChild(loading);
    chat.scrollTop = chat.scrollHeight;

    try {
        // API CALL
        const res = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ topic: text })
        });

        const data = await res.json();

        // REMOVE LOADING
        loading.remove();

        // BOT RESPONSE (clean formatting)
        addMessage("📄 REPORT:\n\n" + data.report, "bot");
        addMessage("🧪 FEEDBACK:\n\n" + data.feedback, "bot");

    } catch (error) {
        loading.innerText = "❌ Error: Something went wrong!";
    }
}