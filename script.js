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

// The wheel: choose a letter and the wheel turns that partner to the top.
const wheel = document.getElementById("wheel");
const panel = document.getElementById("panel");
if (wheel && panel) {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let rot = 0;
  const setRot = (deg) => wheel.style.setProperty("--rot", `${deg}deg`);

  // Opening turn on load, like opening a valve.
  if (!reduce) {
    setRot(-72);
    wheel.getBoundingClientRect();
    requestAnimationFrame(() => { wheel.classList.add("ready"); setRot(0); });
  } else {
    wheel.classList.add("ready");
  }

  const choose = (med) => {
    const i = Number(med.dataset.index);
    let delta = (-i * 72 - rot) % 360;
    if (delta > 180) delta -= 360;
    if (delta < -180) delta += 360;
    rot += delta;
    setRot(rot);
    wheel.querySelectorAll(".med").forEach((m) => {
      m.classList.toggle("active", m === med);
      m.setAttribute("aria-pressed", m === med ? "true" : "false");
    });
    const tpl = document.getElementById(`t-${med.dataset.person}`);
    panel.innerHTML = "";
    panel.appendChild(tpl.content.cloneNode(true));
    panel.removeAttribute("data-show");
    void panel.offsetWidth;
    panel.setAttribute("data-show", "");
  };

  wheel.querySelectorAll(".med").forEach((med) => {
    med.setAttribute("aria-pressed", "false");
    med.addEventListener("click", () => choose(med));
    med.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); choose(med); }
    });
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
