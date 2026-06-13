/**
 * Utility: Copy Short Links to Clipboard
 */
async function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).innerText;
    try {
        await navigator.clipboard.writeText(text);
        alert("Link copied to clipboard!");
    } catch (err) {
        console.error('Failed to copy: ', err);
    }
}
