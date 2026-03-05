# IDE Prompt: Fix Mobile PDF Display in Gallery Modal

## PROBLEM
PDFs displayed in the portfolio gallery modal are cut off on mobile devices, requiring horizontal scrolling and not showing the full document properly.

## SOLUTION REQUIREMENTS

Fix the PDF display in the gallery modal (`#galleryPdf`) to work seamlessly on mobile devices with these requirements:

1. **Full viewport width on mobile** - PDFs should scale to fit mobile screen width
2. **No horizontal scrolling required** - Users should see the full page width
3. **Vertical scrolling only** - Allow natural scrolling through PDF pages
4. **Pinch-to-zoom support** - Enable users to zoom in/out on PDF content
5. **Fallback for unsupported browsers** - Provide download link if PDF can't render
6. **Touch-friendly navigation** - Gallery arrows should work with PDF open

---

## IMPLEMENTATION INSTRUCTIONS

### Step 1: Update Gallery Modal HTML
Locate the `#galleryModal` div and ensure it has this structure:

```html
<div class="gallery-modal" id="galleryModal">
    <div class="gallery-close" id="galleryClose">&times;</div>
    <div class="gallery-nav gallery-prev" id="galleryPrev">&#10094;</div>

    <div class="gallery-content">
        <!-- Image display -->
        <img src="" alt="Gallery Image" class="gallery-img" id="galleryImg">

        <!-- PDF display wrapper -->
        <div class="gallery-pdf-wrapper" id="galleryPdfWrapper" style="display: none;">
            <embed
                id="galleryPdf"
                type="application/pdf"
                class="gallery-pdf"
            />

            <!-- Fallback download link for unsupported browsers -->
            <div class="pdf-fallback" id="pdfFallback">
                <p>Unable to display PDF in your browser.</p>
                <a href="" download class="btn btn-filled-light" id="pdfDownloadLink">
                    Download PDF
                </a>
            </div>
        </div>
    </div>

    <div class="gallery-nav gallery-next" id="galleryNext">&#10095;</div>
    <div class="gallery-counter" id="galleryCounter"></div>
</div>
```

### Step 2: Update CSS for PDF Display

Add these styles to the existing stylesheet (inside `<style>` tags):

```css
/* =========================================================================
   MOBILE PDF FIXES
   ========================================================================= */

/* PDF Wrapper Container */
.gallery-pdf-wrapper {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    background: #000;
}

/* PDF Embed - Desktop */
.gallery-pdf {
    width: 90vw;
    height: 85vh;
    max-width: 1200px;
    border: none;
    border-radius: var(--radius-md);
    background: white;
}

/* PDF Fallback Download */
.pdf-fallback {
    display: none;
    text-align: center;
    color: white;
    padding: var(--space-xl);
}

.pdf-fallback.active {
    display: block;
}

.pdf-fallback p {
    margin-bottom: var(--space-md);
    font-size: var(--text-body-lg);
}

/* Mobile PDF Optimizations */
@media (max-width: 768px) {
    /* Make PDF wrapper full screen on mobile */
    .gallery-pdf-wrapper {
        width: 100vw;
        height: 100vh;
        padding: 0;
    }

    /* PDF takes full viewport on mobile */
    .gallery-pdf {
        width: 100vw;
        height: calc(100vh - 60px); /* Account for counter */
        max-width: 100vw;
        border-radius: 0;
        /* Enable touch gestures */
        touch-action: pan-y pinch-zoom;
        -webkit-overflow-scrolling: touch;
    }

    /* Adjust gallery controls for PDF viewing */
    .gallery-modal.viewing-pdf .gallery-nav {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(8px);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
    }

    .gallery-modal.viewing-pdf .gallery-prev {
        left: 10px;
        top: 50%;
        transform: translateY(-50%);
    }

    .gallery-modal.viewing-pdf .gallery-next {
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
    }

    .gallery-modal.viewing-pdf .gallery-close {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(8px);
        border-radius: 50%;
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        line-height: 1;
        top: 10px;
        right: 10px;
    }

    .gallery-modal.viewing-pdf .gallery-counter {
        bottom: 10px;
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(8px);
        padding: 8px 16px;
        border-radius: 20px;
    }

    /* Adjust image gallery when NOT viewing PDF */
    .gallery-content {
        max-width: 100vw;
        max-height: 100vh;
        overflow: hidden;
    }
}

/* Small phones - even more compact */
@media (max-width: 480px) {
    .gallery-pdf {
        width: 100vw;
        height: calc(100vh - 50px);
    }

    .gallery-modal.viewing-pdf .gallery-nav {
        width: 44px;
        height: 44px;
        font-size: 20px;
    }
}

/* Landscape mode on mobile */
@media (max-width: 768px) and (orientation: landscape) {
    .gallery-pdf {
        height: 100vh;
    }

    .gallery-modal.viewing-pdf .gallery-counter {
        bottom: 5px;
        font-size: 11px;
        padding: 6px 12px;
    }
}
```

### Step 3: Update JavaScript for PDF Handling

Locate the `updateGalleryImage()` function and replace it with this enhanced version:

```javascript
function updateGalleryImage() {
    const imgEl = document.getElementById('galleryImg');
    const pdfWrapper = document.getElementById('galleryPdfWrapper');
    const pdfEl = document.getElementById('galleryPdf');
    const pdfFallback = document.getElementById('pdfFallback');
    const pdfDownloadLink = document.getElementById('pdfDownloadLink');
    const counter = document.getElementById('galleryCounter');
    const modal = document.getElementById('galleryModal');

    const src = currentGallery[currentIndex];
    const isPdf = src.toLowerCase().endsWith('.pdf');

    if (isPdf) {
        // Hide image, show PDF
        imgEl.style.display = 'none';
        pdfWrapper.style.display = 'flex';

        // Set PDF source with fallback detection
        pdfEl.src = src;
        pdfDownloadLink.href = src;

        // Add class for PDF-specific styling
        modal.classList.add('viewing-pdf');

        // Detect if PDF loaded successfully (timeout method)
        setTimeout(() => {
            // Check if PDF embed is working
            // If height is 0 or very small, likely failed
            if (pdfEl.offsetHeight < 100) {
                pdfEl.style.display = 'none';
                pdfFallback.classList.add('active');
            } else {
                pdfEl.style.display = 'block';
                pdfFallback.classList.remove('active');
            }
        }, 1000);

        // Mobile-specific: Add instructions for first-time viewers
        if (window.innerWidth <= 768 && !localStorage.getItem('pdfInstructionsShown')) {
            showPdfInstructions();
            localStorage.setItem('pdfInstructionsShown', 'true');
        }

    } else {
        // Show image, hide PDF
        imgEl.style.display = 'block';
        pdfWrapper.style.display = 'none';
        imgEl.src = src;
        modal.classList.remove('viewing-pdf');
    }

    // Update counter
    counter.innerText = `${currentIndex + 1} / ${currentGallery.length}`;
}

// Optional: Show brief instructions for mobile PDF viewing
function showPdfInstructions() {
    const instructionDiv = document.createElement('div');
    instructionDiv.className = 'pdf-instructions';
    instructionDiv.innerHTML = `
        <div class="pdf-instructions-content">
            <p>📄 Use pinch to zoom • Swipe to scroll</p>
        </div>
    `;
    document.body.appendChild(instructionDiv);

    // Add styles for instructions
    const style = document.createElement('style');
    style.textContent = `
        .pdf-instructions {
            position: fixed;
            top: 80px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 10001;
            animation: fadeInOut 3s ease forwards;
        }
        .pdf-instructions-content {
            background: rgba(0, 0, 0, 0.85);
            color: white;
            padding: 12px 24px;
            border-radius: 24px;
            font-size: 14px;
            backdrop-filter: blur(8px);
        }
        @keyframes fadeInOut {
            0%, 100% { opacity: 0; }
            10%, 90% { opacity: 1; }
        }
    `;
    document.head.appendChild(style);

    // Remove after animation
    setTimeout(() => {
        instructionDiv.remove();
    }, 3000);
}
```

### Step 4: Add iOS Safari Specific Fixes

iOS Safari has known issues with PDF embeds. Add this additional JavaScript:

```javascript
// Add to the DOMContentLoaded event listener

// iOS PDF Fix - Use iframe instead of embed on iOS
function isIOS() {
    return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
}

if (isIOS()) {
    // Replace embed with iframe on iOS for better compatibility
    const pdfWrapper = document.getElementById('galleryPdfWrapper');
    const oldEmbed = document.getElementById('galleryPdf');

    // Create iframe instead
    const iframe = document.createElement('iframe');
    iframe.id = 'galleryPdf';
    iframe.className = 'gallery-pdf';
    iframe.setAttribute('frameborder', '0');
    iframe.setAttribute('scrolling', 'auto');

    // Replace embed with iframe
    oldEmbed.parentNode.replaceChild(iframe, oldEmbed);
}
```

---

## ALTERNATIVE SOLUTION: PDF.js Integration (Better Mobile Support)

If native PDF embedding still has issues, use Mozilla's PDF.js library for better mobile control:

### Step 1: Add PDF.js Library
Add this to the `<head>` section:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
```

### Step 2: Replace Embed with Canvas
Replace the `#galleryPdf` embed with:

```html
<div class="pdf-viewer" id="pdfViewer" style="display: none;">
    <canvas id="pdfCanvas"></canvas>
    <div class="pdf-controls">
        <button class="pdf-nav-btn" id="pdfPrevPage">← Previous</button>
        <span id="pdfPageInfo">Page 1 of 1</span>
        <button class="pdf-nav-btn" id="pdfNextPage">Next →</button>
    </div>
</div>
```

### Step 3: Add PDF.js Rendering Logic

```javascript
let pdfDoc = null;
let pdfPageNum = 1;
let pdfPageRendering = false;

async function renderPdf(url) {
    const canvas = document.getElementById('pdfCanvas');
    const ctx = canvas.getContext('2d');

    // Load PDF
    const loadingTask = pdfjsLib.getDocument(url);
    pdfDoc = await loadingTask.promise;

    document.getElementById('pdfPageInfo').textContent =
        `Page ${pdfPageNum} of ${pdfDoc.numPages}`;

    // Render first page
    renderPdfPage(pdfPageNum);
}

function renderPdfPage(num) {
    pdfPageRendering = true;
    const canvas = document.getElementById('pdfCanvas');
    const ctx = canvas.getContext('2d');

    pdfDoc.getPage(num).then((page) => {
        const viewport = page.getViewport({ scale: 1.5 });

        // Mobile scaling
        if (window.innerWidth <= 768) {
            const scale = window.innerWidth / viewport.width;
            canvas.width = window.innerWidth * 0.95;
            canvas.height = viewport.height * scale;
        } else {
            canvas.width = viewport.width;
            canvas.height = viewport.height;
        }

        const renderContext = {
            canvasContext: ctx,
            viewport: viewport
        };

        page.render(renderContext).promise.then(() => {
            pdfPageRendering = false;
        });
    });
}

// PDF navigation
document.getElementById('pdfPrevPage').addEventListener('click', () => {
    if (pdfPageNum <= 1) return;
    pdfPageNum--;
    renderPdfPage(pdfPageNum);
    document.getElementById('pdfPageInfo').textContent =
        `Page ${pdfPageNum} of ${pdfDoc.numPages}`;
});

document.getElementById('pdfNextPage').addEventListener('click', () => {
    if (pdfPageNum >= pdfDoc.numPages) return;
    pdfPageNum++;
    renderPdfPage(pdfPageNum);
    document.getElementById('pdfPageInfo').textContent =
        `Page ${pdfPageNum} of ${pdfDoc.numPages}`;
});
```

---

## RECOMMENDED APPROACH

**Try Solution 1 (Native Embed with Fixes) first** - It's simpler and works for most cases.

**If mobile issues persist, use Solution 2 (PDF.js)** - Provides better control but requires more code.

---

## TESTING CHECKLIST

After implementation, test:

- [ ] PDF displays full-width on mobile (no horizontal scroll)
- [ ] Pinch-to-zoom works on touch devices
- [ ] Gallery navigation arrows work with PDF open
- [ ] Close button works when viewing PDF
- [ ] Falls back to download link if PDF can't render
- [ ] Multi-page PDFs scroll naturally
- [ ] Works on iOS Safari
- [ ] Works on Android Chrome
- [ ] Desktop view still looks good
- [ ] Gallery counter shows correct position

---

## QUICK WIN MINIMAL FIX

If you need the fastest fix possible, just add this single CSS rule:

```css
@media (max-width: 768px) {
    #galleryPdf {
        width: 100vw !important;
        height: calc(100vh - 60px) !important;
        max-width: 100vw !important;
    }
}
```

This won't be perfect but will immediately stop the horizontal scrolling issue.
