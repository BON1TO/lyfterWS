async function scrape() {
    const url = document.getElementById("urlInput").value;
    const output = document.getElementById("output");

    if (!url) {
        output.textContent = "Please enter a URL.";
        return;
    }

    output.textContent = "Scraping…";

    try {
        const res = await fetch("/scrape", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        const data = await res.json();
        window.lastResult = data;
        output.textContent = JSON.stringify(data, null, 2);

    } catch (err) {
        output.textContent = "Error: " + err.message;
    }
}

function downloadJSON() {
    if (!window.lastResult) {
        alert("Nothing to download yet.");
        return;
    }

    const blob = new Blob(
        [JSON.stringify(window.lastResult, null, 2)],
        { type: "application/json" }
    );

    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "scrape-result.json";
    a.click();
}
