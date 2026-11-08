// Valve Partners site script
// Contact forms save to the Supabase project "valve-partners" and email a copy through Web3Forms.
const SB_URL = "https://mefvxxoytleyfjbwtxix.supabase.co";
const SB_KEY = "sb_publishable_Ex6vMImvvkTdQsFYprve7g_awiuqxEs";   // public key: can only add form entries and count visits

// Where each person's messages are emailed.  Each Web3Forms access key is tied to one inbox; right now every key is Eric's.
// To send someone's messages to their own inbox, create a Web3Forms key for their address and put it on their line.
const ERIC_KEY = "b88fef65-1434-4f2b-8b2d-9b9cb760e7f0";   // Eric's inbox (public by design; it can only send to that address)
const MAIL_KEY = {
  valve: ERIC_KEY,     // "Not sure, anyone"
  vincent: ERIC_KEY,
  ayden: ERIC_KEY,
  lauren: ERIC_KEY,
  vicki: ERIC_KEY,
  eric: ERIC_KEY,
};

// The one contact form (contact.html).  Every "Contact Vicki" style link opens it as contact.html?to=vicki,
// so the person is already picked and the visitor never touches the drop-down.  Lauren's links can add &about=sourdough, &about=soccer or &about=solar.
const PEOPLE = {
  anyone:  { name: "",        site: "valve",   title: "Get in touch",   intro: "Tell us what you need and who you'd like to reach.  We'll get your message to the right person." },
  vincent: { name: "Vincent", site: "vincent", title: "Contact Vincent", intro: "Tell Vincent what you need and he'll put together a quote." },
  ayden:   { name: "Ayden",   site: "ayden",   title: "Contact Ayden",   intro: "Send Ayden a note with the student's grade and what they need help with, and he'll get back to you.", hint: "Student's grade, subject and what they need help with" },
  lauren:  { name: "Lauren",  site: "lauren",  title: "Contact Lauren",  intro: "Tell Lauren whether it's about solar, sourdough or soccer, and she'll get back to you." },
  vicki:   { name: "Vicki",   site: "vicki",   title: "Contact Vicki",   intro: "Tell Vicki who you're looking for, or what kind of help you need, and she'll get back to you." },
  eric:    { name: "Eric",    site: "eric",    title: "Contact Eric",    intro: "Tell Eric what you need help with, and he'll get back to you." },
};
const LAUREN_HINT = { sourdough: "How many loaves you'd like and when you need them", soccer: "Your player's age and what they want to work on", solar: "Your city, and roughly what your monthly electric bill runs" };
const LAUREN_TOPIC = { sourdough: "sourdough", soccer: "soccer training", solar: "solar" };

const smart = document.querySelector("form[data-smart]");
if (smart) {
  const q = new URLSearchParams(location.search);
  const to = smart.querySelector("#to");
  const about = smart.querySelector("#about");
  const aboutLabel = smart.querySelector("#about-label");
  const whoLabel = smart.querySelector("#who-label");
  const sendingTo = smart.querySelector("#sending-to");
  const topic = smart.querySelector("input[name=topic]");
  const message = smart.querySelector("#message");

  const update = () => {
    const key = PEOPLE[to.value] ? to.value : "anyone";
    const p = PEOPLE[key];
    const isLauren = key === "lauren";
    aboutLabel.hidden = !isLauren;
    smart.dataset.site = p.site;
    topic.value = isLauren ? `Lauren (${LAUREN_TOPIC[about.value] || "sourdough"})` : (p.name || "Anyone");
    document.getElementById("c-title").textContent = p.title;
    document.getElementById("c-intro").textContent = p.intro;
    document.getElementById("sending-name").textContent = p.name;
    message.placeholder = isLauren ? LAUREN_HINT[about.value] : (p.hint || "");
    document.title = `${p.title} | Valve Partners`;
    const url = new URL(location.href);
    if (key === "anyone") url.searchParams.delete("to"); else url.searchParams.set("to", key);
    if (isLauren) url.searchParams.set("about", about.value); else url.searchParams.delete("about");
    history.replaceState(null, "", url);
  };

  const picked = (q.get("to") || "").toLowerCase();
  if (PEOPLE[picked] && picked !== "anyone") {
    to.value = picked;
    whoLabel.hidden = true;          // already picked from their link: show "Sending to Vicki" instead of the drop-down
    sendingTo.hidden = false;
  }
  if (LAUREN_TOPIC[q.get("about")]) about.value = q.get("about");
  smart.querySelector("#change-person").addEventListener("click", () => {
    sendingTo.hidden = true; whoLabel.hidden = false; to.focus();
  });
  to.addEventListener("change", update);
  about.addEventListener("change", update);
  update();

  // Someone who has sent a message before gets their name and email filled in (kept in their own browser only).
  try {
    const saved = JSON.parse(localStorage.getItem("valve-contact") || "{}");
    if (saved.name) smart.querySelector("input[name=name]").value = saved.name;
    if (saved.email) smart.querySelector("input[name=email]").value = saved.email;
  } catch (e) {}
}

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
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const site = form.dataset.site || "valve";
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

    const dbSite = ["ayden", "lauren"].includes(site) ? site : "valve";   // the database keeps its original labels; the topic says who it's for
    const row = { site: dbSite, name, email, topic, message, page: location.pathname };
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
      try { localStorage.setItem("valve-contact", JSON.stringify({ name, email })); } catch (e) {}
      const keep = form.querySelector("#to") ? [form.querySelector("#to").value, form.querySelector("#about").value] : null;
      form.reset();
      if (keep) { form.querySelector("#to").value = keep[0]; form.querySelector("#about").value = keep[1]; form.querySelector("input[name=name]").value = name; form.querySelector("input[name=email]").value = email; }
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
