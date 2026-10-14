document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav-links");
  if (toggle && nav) toggle.addEventListener("click", () => nav.classList.toggle("open"));
  document.querySelectorAll("[data-copy]").forEach(button => {
    button.addEventListener("click", async () => {
      const text = button.getAttribute("data-copy") || "";
      try {
        await navigator.clipboard.writeText(text);
        const old = button.textContent;
        button.textContent = "تم النسخ ✓";
        setTimeout(() => button.textContent = old, 1400);
      } catch {
        button.textContent = "تعذر النسخ";
      }
    });
  });
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add("in-view"); observer.unobserve(entry.target); }
  }), {threshold: 0.08});
  document.querySelectorAll(".feature-card,.course-card,.resource-card,.snippet-card,.lesson-card").forEach(el => {
    el.classList.add("reveal"); observer.observe(el);
  });
});
