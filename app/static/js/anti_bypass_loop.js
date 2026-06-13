/**
 * Anti-Bypass Security Layer
 * Prevents Click-jacking and Iframe-based ad hijacking.
 */
(function() {
    if (window.self !== window.top) {
        // If site is loaded in an iframe, redirect to top-level window
        window.top.location.href = window.self.location.href;
    }

    // Detect if user has adblocker actively interfering with our Monetization Logic
    const adBlockDetector = setInterval(() => {
        const ad = document.querySelector('.ad-container');
        if (ad && ad.offsetHeight === 0) {
            console.warn("MonetLink Security: Adblock detected. Please disable to support the publisher.");
            // Optional: Redirect to a 'Please disable adblock' page here
            clearInterval(adBlockDetector);
        }
    }, 2000);
})();
