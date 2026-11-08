const gallery = [...document.querySelectorAll("[data-photo]")];
const viewer = document.querySelector("#photo-viewer");
const viewerImage = document.querySelector("#viewer-image");
const viewerCaption = document.querySelector("#viewer-caption");
let currentPhoto = 0;
let swipeStart = null;

function showPhoto(index) {
  currentPhoto = (index + gallery.length) % gallery.length;
  const photo = gallery[currentPhoto];
  viewerImage.src = photo.href;
  viewerImage.alt = photo.querySelector("img").alt;
  const label = photo.querySelector(".photo-name").textContent;
  viewerCaption.textContent = `${currentPhoto + 1} of ${gallery.length} · ${label}`;
}

if (typeof viewer.showModal === "function") {
  for (const [index, photo] of gallery.entries()) {
    photo.addEventListener("click", (event) => {
      if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
      event.preventDefault();
      showPhoto(index);
      viewer.showModal();
    });
  }

  document.querySelector("#previous-photo").addEventListener("click", () => showPhoto(currentPhoto - 1));
  document.querySelector("#next-photo").addEventListener("click", () => showPhoto(currentPhoto + 1));
  viewer.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      event.preventDefault();
      showPhoto(currentPhoto + (event.key === "ArrowLeft" ? -1 : 1));
    }
  });

  const stage = viewer.querySelector(".viewer-stage");
  stage.addEventListener("pointerdown", (event) => {
    if (event.pointerType !== "touch" || !event.isPrimary) return;
    swipeStart = { id: event.pointerId, x: event.clientX, y: event.clientY };
  });
  stage.addEventListener("pointercancel", () => { swipeStart = null; });
  stage.addEventListener("pointerup", (event) => {
    if (swipeStart?.id !== event.pointerId) return;
    const x = event.clientX - swipeStart.x;
    const y = event.clientY - swipeStart.y;
    swipeStart = null;
    if (Math.abs(x) > 45 && Math.abs(x) > Math.abs(y) * 1.3) {
      showPhoto(currentPhoto + (x < 0 ? 1 : -1));
    }
  });
  viewer.addEventListener("close", () => { swipeStart = null; });
}

const share = document.querySelector("[data-share-url]");
const shareStatus = document.querySelector("#share-status");
if (navigator.share || navigator.clipboard?.writeText) {
  share.hidden = false;
  share.addEventListener("click", async () => {
    const url = share.dataset.shareUrl;
    try {
      if (navigator.share) {
        await navigator.share({ title: "VEGAS! The Show", url });
      } else {
        await navigator.clipboard.writeText(url);
        shareStatus.textContent = "Show link copied.";
        share.textContent = "Link copied";
      }
    } catch (error) {
      if (error.name !== "AbortError") shareStatus.textContent = "The show link could not be shared.";
    }
  });
}

if ("IntersectionObserver" in window) {
  const mobileTicket = document.querySelector("#mobile-ticket");
  const mobileLink = mobileTicket.querySelector("a");
  const ticketStrip = document.querySelector("#showtimes");
  const closeout = document.querySelector(".closeout");
  const footer = document.querySelector(".footer");
  const targets = [ticketStrip, closeout, footer];
  const narrow = matchMedia("(max-width: 760px)");

  function updateTicketBar() {
    const pastOpeningTicket = ticketStrip.getBoundingClientRect().bottom <= 0;
    const atClosingTicket = targets.slice(1).some((target) => {
      const rect = target.getBoundingClientRect();
      return rect.top < innerHeight && rect.bottom > 0;
    });
    const focusInBar = document.activeElement === mobileLink;
    mobileTicket.hidden = !narrow.matches || (!focusInBar && (!pastOpeningTicket || atClosingTicket));
  }

  const observer = new IntersectionObserver(updateTicketBar);
  targets.forEach((target) => observer.observe(target));
  narrow.addEventListener("change", updateTicketBar);
  mobileLink.addEventListener("blur", () => requestAnimationFrame(updateTicketBar));
}
