// Comparison Helpers and Drag Handling
let isSliding = false;

function triggerDirectDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function downloadComparisonResult() {
  if (!currentResultBlob || !currentResultFileName) return;
  triggerDirectDownload(currentResultBlob, currentResultFileName);
}

function showImageComparison(beforeUrl, resultBlob, outName, originalFile) {
  currentResultBlob = resultBlob;
  currentResultFileName = outName;

  if (processedImageObjectUrl) {
    URL.revokeObjectURL(processedImageObjectUrl);
  }
  processedImageObjectUrl = URL.createObjectURL(resultBlob);

  // Update Slider Images
  const compImgAfter = document.getElementById('compImgAfter');
  const compImgBefore = document.getElementById('compImgBefore');
  compImgAfter.src = processedImageObjectUrl;
  compImgBefore.src = beforeUrl;

  // Update Side-by-Side Images
  const sideImgBefore = document.getElementById('sideImgBefore');
  const sideImgAfter = document.getElementById('sideImgAfter');
  sideImgBefore.src = beforeUrl;
  sideImgAfter.src = processedImageObjectUrl;

  // Metadata labels
  document.getElementById('sideBeforeMeta').textContent = `${formatBytes(originalFile.size)}`;
  document.getElementById('sideAfterMeta').textContent = `${formatBytes(resultBlob.size)}`;
  document.getElementById('compDownloadBtnText').textContent = `Download (${formatBytes(resultBlob.size)})`;

  // Reset slider to 50%
  updateSliderPosition(50);

  // Show comparison container and ensure default slider mode
  const compContainer = document.getElementById('comparisonContainer');
  compContainer.style.display = 'flex';
  setComparisonMode('slider');

  // Smooth scroll down to comparison
  compContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  // Download file automatically & notify
  triggerDirectDownload(resultBlob, outName);
  showStatus('success', `Completed: ${outName}`);
}

function updateSliderPosition(pct) {
  pct = Math.max(0, Math.min(100, pct));
  const sliderDivider = document.getElementById('sliderDivider');
  const compImgBefore = document.getElementById('compImgBefore');

  if (sliderDivider) {
    sliderDivider.style.left = `${pct}%`;
  }
  if (compImgBefore) {
    compImgBefore.style.clipPath = `polygon(0 0, ${pct}% 0, ${pct}% 100%, 0 100%)`;
    compImgBefore.style.webkitClipPath = `polygon(0 0, ${pct}% 0, ${pct}% 100%, 0 100%)`;
  }
}

function handleSliderMove(e) {
  if (!isSliding) return;
  const stage = document.getElementById('sliderStage');
  if (!stage) return;
  const rect = stage.getBoundingClientRect();
  const clientX = e.touches ? e.touches[0].clientX : e.clientX;
  const offsetX = clientX - rect.left;
  const pct = (offsetX / rect.width) * 100;
  updateSliderPosition(pct);
}

function setComparisonMode(mode) {
  const tabSlider = document.getElementById('tabSlider');
  const tabSide = document.getElementById('tabSideBySide');
  const sliderStage = document.getElementById('sliderStageWrapper');
  const sideStage = document.getElementById('sideStage');

  if (mode === 'slider') {
    tabSlider.classList.add('active');
    tabSide.classList.remove('active');
    sliderStage.style.display = 'flex';
    sideStage.style.display = 'none';
  } else {
    tabSlider.classList.remove('active');
    tabSide.classList.add('active');
    sliderStage.style.display = 'none';
    sideStage.style.display = 'grid';
  }
}

function clearComparison() {
  const compContainer = document.getElementById('comparisonContainer');
  if (compContainer) compContainer.style.display = 'none';

  if (processedImageObjectUrl) {
    URL.revokeObjectURL(processedImageObjectUrl);
    processedImageObjectUrl = null;
  }
  currentResultBlob = null;
  currentResultFileName = '';

  const compImgAfter = document.getElementById('compImgAfter');
  const compImgBefore = document.getElementById('compImgBefore');
  const sideImgBefore = document.getElementById('sideImgBefore');
  const sideImgAfter = document.getElementById('sideImgAfter');

  if (compImgAfter) compImgAfter.src = '';
  if (compImgBefore) compImgBefore.src = '';
  if (sideImgBefore) sideImgBefore.src = '';
  if (sideImgAfter) sideImgAfter.src = '';
}

// Drag listeners for slider
document.addEventListener('DOMContentLoaded', () => {
  const stageEl = document.getElementById('sliderStage');
  if (stageEl) {
    stageEl.addEventListener('mousedown', e => {
      isSliding = true;
      handleSliderMove(e);
    });
    window.addEventListener('mousemove', e => {
      if (isSliding) handleSliderMove(e);
    });
    window.addEventListener('mouseup', () => {
      isSliding = false;
    });

    stageEl.addEventListener('touchstart', e => {
      isSliding = true;
      handleSliderMove(e);
    }, { passive: true });
    window.addEventListener('touchmove', e => {
      if (isSliding) handleSliderMove(e);
    }, { passive: true });
    window.addEventListener('touchend', () => {
      isSliding = false;
    });
  }
});
