document.addEventListener('DOMContentLoaded', function() {    

    // Only attach fetch for API links
    document.querySelectorAll('.api-link').forEach(link => {
        link.addEventListener('click', async function(event) {
            event.preventDefault(); 
            const url = this.href;
            const method = this.dataset.method || 'GET';
            const bodyData = this.dataset.body ? JSON.parse(this.dataset.body) : null;

            try {
                let response = await fetch(url, {
                    method: method,
                    credentials: "include", 
                    headers: { "Content-Type": "application/json" },
                    body: bodyData ? JSON.stringify(bodyData) : null
                });

                // Handle token expiry
                if (response.status === 401) {
                    alert("Your session has expired. Logging you out…");
                    await fetch("/logout", { method: "GET", credentials: "include" });
                    window.location.href = "/";  // redirect to home
                    return;
                }

                const contentType = response.headers.get("content-type");
                if (contentType && contentType.includes("application/json")) {
                    const data = await response.json();
                    console.log("Response:", data);
                } else {
                    console.error("Received HTML instead of JSON");
                }
            } catch (err) {
                console.error("Fetch error:", err);
            }
        });
    });

});
