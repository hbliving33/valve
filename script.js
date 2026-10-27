// Valve Partners site script
// Change this one line to set where contact messages go.
const CONTACT_EMAIL = "hello@valvepartners.com";

// Links like "Talk to Vicky" jump to the form with that person picked.
document.querySelectorAll("[data-topic]").forEach((link) => {
  link.addEventListener("click", () => {
    const topic = document.getElementById("topic");
    if (topic) topic.value = link.dataset.topic;
  });
});

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
