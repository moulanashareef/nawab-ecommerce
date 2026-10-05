document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector("[data-nav]");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  document.querySelectorAll(".message-close").forEach((button) => {
    button.addEventListener("click", () => button.parentElement.remove());
  });

  document.querySelectorAll("input[type=number]").forEach((input) => {
    input.addEventListener("input", () => {
      const min = Number(input.min);
      const max = Number(input.max);
      const value = Number(input.value);
      if (input.value !== "" && Number.isFinite(min) && value < min) input.value = min;
      if (input.value !== "" && Number.isFinite(max) && value > max) input.value = max;
    });
  });
});
