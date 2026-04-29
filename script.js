// ✅ YOUR REAL API LINK ADDED
window.VISITOR_COUNTER_CONFIG = {
  endpoint: "https://k1b2zd2dlf.execute-api.ap-south-1.amazonaws.com/count",
  method: "GET"
};

const menuBtn = document.getElementById("menu-btn");
const navMenu = document.getElementById("nav-menu");
const navLinks = document.querySelectorAll(".nav-menu a");
const revealItems = document.querySelectorAll(".reveal");
const counterElement = document.getElementById("visitor-counter");
const currentPage = document.body.dataset.page;

if (menuBtn && navMenu) {
  menuBtn.addEventListener("click", () => {
    navMenu.classList.toggle("open");
  });
}

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    if (navMenu) navMenu.classList.remove("open");
  });
});

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add("visible");
      });
    },
    { threshold: 0.14 }
  );
  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("visible"));
}

if (currentPage) {
  navLinks.forEach((link) => {
    link.classList.toggle("active", link.dataset.page === currentPage);
  });
}

// 🔢 Counter Animation
const animateCounter = (start, end, duration = 900) => {
  if (!counterElement) return;
  let value = start;
  counterElement.textContent = String(start).padStart(6, "0");

  const stepTime = Math.max(Math.floor(duration / (end - start || 1)), 20);

  const timer = setInterval(() => {
    value++;
    counterElement.textContent = String(value).padStart(6, "0");
    if (value >= end) clearInterval(timer);
  }, stepTime);
};

// 🌐 Fetch from AWS
const loadVisitorCount = async () => {
  if (!counterElement) return;

  try {
    const response = await fetch(window.VISITOR_COUNTER_CONFIG.endpoint);

    if (!response.ok) throw new Error("API error");

    const data = await response.json();

    const parsed = typeof data.body === "string" ? JSON.parse(data.body) : data;
    const count = Number(parsed.count);

    if (!Number.isFinite(count)) throw new Error("Invalid data");

    animateCounter(Math.max(count - 20, 0), count, 1000);

  } catch (error) {
    console.error("Error:", error);
    counterElement.textContent = "ERROR";
  }
};

loadVisitorCount();

// 📅 Year
const year = document.getElementById("year");
if (year) year.textContent = new Date().getFullYear();