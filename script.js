// Valve Partners site script
// Contact forms save to the Supabase project "valve-partners" and email a copy through Web3Forms.
const SB_URL = "https://mefvxxoytleyfjbwtxix.supabase.co";
const SB_KEY = "sb_publishable_Ex6vMImvvkTdQsFYprve7g_awiuqxEs";   // public key: can only add form entries and count visits

// Where each form's email goes.  Each Web3Forms access key is tied to one inbox; the key below sends to Eric's inbox.
// To route a form somewhere else, create a Web3Forms key for that address and put it here.
const ERIC_KEY = "b88fef65-1434-4f2b-8b2d-9b9cb760e7f0";   // Eric's inbox (public by design; it can only send to that address)
const MAIL_KEY = {
  valve: ERIC_KEY,    // fallback (the home page no longer has a form)
  vicki: ERIC_KEY,    // Vicki's staffing page
  ayden: ERIC_KEY,    // Ayden's tutoring page
  lauren: ERIC_KEY,   // Lauren's page
};

// Links like "Talk to Vicki" jump to the form with that person picked.
document.addEventListener("click", (e) => {
  const link = e.target.closest("[data-topic]");
  if (!link) return;
  const topic = document.getElementById("topic");
  if (topic) topic.value = link.dataset.topic;
});

// The logo: choose a figure (or a name) and that partner's story appears.
// The figures sway gently, a name you point at stands up, and the one you pick does a little groove
// while a wave runs through the rest of the family.  Works for every logo on the page (the button options page has several).
document.querySelectorAll("[data-stage]").forEach((stage) => {
  const mark = stage.querySelector(".mark");
  const panel = stage.querySelector(".panel");
  if (!mark || !panel) return;
  const figs = [...mark.querySelectorAll(".fig")];
  const names = [...stage.querySelectorAll(".who button")];
  const figFor = (person) => figs.find((f) => f.dataset.person === person);
  let waveTimer;

  const restart = (el, cls) => { el.classList.remove(cls); void el.getBoundingClientRect(); el.classList.add(cls); };

  const choose = (person) => {
    mark.classList.add("choosing");
    const picked = figFor(person);
    const at = picked ? Number(picked.dataset.index) : 0;
    figs.forEach((f) => {
      const on = f.dataset.person === person;
      f.classList.toggle("active", on);
      f.setAttribute("aria-pressed", on ? "true" : "false");
      f.style.setProperty("--d", Math.abs(Number(f.dataset.index) - at));
    });
    names.forEach((b) => {
      const on = b.dataset.person === person;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (on) restart(b, "bump");
    });
    restart(mark, "wave");
    clearTimeout(waveTimer);
    waveTimer = setTimeout(() => mark.classList.remove("wave"), 1500);

    const tpl = document.getElementById(`t-${person}`);
    if (tpl) {
      panel.innerHTML = "";
      panel.appendChild(tpl.content.cloneNode(true));
    }
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
    const peek = (on) => { const f = figFor(b.dataset.person); if (f) f.classList.toggle("peek", on); };
    b.addEventListener("mouseenter", () => peek(true));
    b.addEventListener("mouseleave", () => peek(false));
    b.addEventListener("focus", () => peek(true));
    b.addEventListener("blur", () => peek(false));
  });
});

const form = document.getElementById("contact-form");
if (form) {
  const status = document.getElementById("form-status");
  const site = form.dataset.site || "valve";
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const name = (data.get("name") || "").trim();
    const email = (data.get("email") || "").trim();
    const message = (data.get("message") || "").trim();
    const topic = data.get("topic") || "Anyone";

    if (data.get("_honey")) { form.reset(); status.textContent = "Thanks.  Your message was sent."; return; }   // bots fill hidden fields
    if (!name || !email || !message) {
      status.textContent = "Fill in your name, email and message, then send again.";
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      status.textContent = "Check your email address.  It should look like name@example.com.";
      return;
    }

    const send = form.querySelector("button[type=submit]");
    send.disabled = true; send.textContent = "Sending...";
    status.textContent = "";

    const row = { site, name, email, topic, message, page: location.pathname };
    const db = fetch(`${SB_URL}/rest/v1/contact_requests`, {
      method: "POST",
      headers: { apikey: SB_KEY, "Content-Type": "application/json", Prefer: "return=minimal" },
      body: JSON.stringify(row),
    }).then((r) => r.ok).catch(() => false);
    const mail = fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ access_key: MAIL_KEY[site] || MAIL_KEY.valve, subject: `Valve Partners website: message for ${topic}`, from_name: "Valve Partners website",
        replyto: email, Name: name, Email: email, For: topic, Message: message, Page: location.pathname }),
    }).then((r) => r.ok).catch(() => false);

    const [a, b] = await Promise.all([db, mail]);
    send.disabled = false; send.textContent = "Send message";
    if (a || b) {
      form.reset();
      status.textContent = "Thanks.  Your message was sent, and we'll get back to you soon.";
    } else {
      status.textContent = "Sorry, the message didn't go through.  Please try again in a minute.";
    }
  });
}

// Visit counter: one count per page per browser session.  No cookies, no personal data.
if (!/^(localhost|127\.)/.test(location.hostname) && location.protocol.startsWith("http")) {
  const path = location.pathname.replace(/index\.html$/, "") || "/";
  let seen = false;
  try { const k = "valve-hit:" + path; seen = !!sessionStorage.getItem(k); sessionStorage.setItem(k, "1"); } catch (e) {}
  if (!seen) fetch(`${SB_URL}/rest/v1/rpc/count_hit`, {
    method: "POST", keepalive: true,
    headers: { apikey: SB_KEY, "Content-Type": "application/json" },
    body: JSON.stringify({ p_site: "valve", p_path: path }),
  }).catch(() => {});
}
