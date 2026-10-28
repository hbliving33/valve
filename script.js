// Valve Partners site script
// Change this one line to set where contact messages go.
const CONTACT_EMAIL = "hello@valvepartners.com";

// Links like "Talk to Vicki" jump to the form with that person picked.
document.addEventListener("click", (e) => {
  const link = e.target.closest("[data-topic]");
  if (!link) return;
  const topic = document.getElementById("topic");
  if (topic) topic.value = link.dataset.topic;
});

// The logo: choose a figure (or a name) and that partner's story appears.
const mark = document.getElementById("mark");
const panel = document.getElementById("panel");
if (mark && panel) {
  const figs = [...mark.querySelectorAll(".fig")];
  const names = [...document.querySelectorAll(".who button")];

  const choose = (person) => {
    mark.classList.add("choosing");
    figs.forEach((f) => {
      const on = f.dataset.person === person;
      f.classList.toggle("active", on);
      f.setAttribute("aria-pressed", on ? "true" : "false");
    });
    names.forEach((b) => b.setAttribute("aria-pressed", b.dataset.person === person ? "true" : "false"));
    const tpl = document.getElementById(`t-${person}`);
    panel.innerHTML = "";
    panel.appendChild(tpl.content.cloneNode(true));
    panel.removeAttribute("data-show");
    void panel.offsetWidth;
    panel.setAttribute("data-show", "");
  };

  figs.forEach((f) => {
    f.setAttribute("aria-pressed", "false");
    f.addEventListener("click", () => choose(f.dataset.person));
    f.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); choose(f.dataset.person); }
    });
  });
  names.forEach((b) => {
    b.setAttribute("aria-pressed", "false");
    b.addEventListener("click", () => choose(b.dataset.person));
  });
}

const form = document.getElementById("contact-form");
if (form) {
  const status = document.getElementById("form-status");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const name = (data.get("name") || "").trim();
    const email = (data.get("email") || "").trim();
    const message = (data.get("message") || "").trim();
    const topic = data.get("topic") || "Anyone";

    if (!name || !email || !message) {
      status.textContent = "Fill in your name, email and message, then send again.";
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      status.textContent = "Check your email address. It should look like name@example.com.";
      return;
    }

    const subject = `Valve Partners: message for ${topic}`;
    const body = `${message}\n\nFrom: ${name}\nEmail: ${email}\nFor: ${topic}`;
    window.location.href =
      `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    status.textContent = "Your email app should open with the message ready to send.";
  });
}
