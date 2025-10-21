document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('summary-form');
    const resultContainer = document.getElementById('summary-result');
    const submitBtn = document.getElementById('submit-btn');
    const urlInput = document.getElementById('youtube-url');

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        submitBtn.textContent = isLoading ? 'Summarizing…' : 'Summarize';
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const url = urlInput.value.trim();

        if (!url) {
            resultContainer.innerHTML = '<p class="error">Please enter a YouTube URL.</p>';
            return;
        }

        resultContainer.innerHTML = 'Loading summary...';
        setLoading(true);

        try {
            const response = await fetch('/summarize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });

            const data = await response.json();

            if (data.status === 200) {
                resultContainer.innerHTML = `
                    <h2>Video Summary</h2>
                    <p>${data.summary}</p>
                `;
            } else {
                resultContainer.innerHTML = `
                    <p class="error">Error: ${data.error}</p>
                `;
            }
        } catch (error) {
            resultContainer.innerHTML = `
                <p class="error">Network Error: ${error.message}</p>
            `;
        } finally {
            setLoading(false);
        }
    });
});


