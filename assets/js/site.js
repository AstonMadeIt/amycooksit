const toggle = document.querySelector(".nav-toggle");
const nav = document.querySelector("#nav");

toggle?.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  toggle.setAttribute("aria-expanded", String(open));
});

const offer = document.querySelector("#offer");
const when = document.querySelector("#when");
const headcount = document.querySelector("#headcount");
const place = document.querySelector("#place");
const diet = document.querySelector("#diet");
const budget = document.querySelector("#budget");
const note = document.querySelector("#note");
const msg = document.querySelector("#msg");
const status = document.querySelector("#status");

function field(node) {
  return node?.value.trim() || "";
}

function draft() {
  const lines = [
    `Hi Amy — I'd like ${field(offer)}.`,
    field(when) ? `Date: ${field(when)}.` : "Date: not set.",
    field(headcount) ? `Headcount: ${field(headcount)}.` : "Headcount: not set.",
    field(place) ? `Place: ${field(place)}.` : "",
    field(diet) ? `Dietary: ${field(diet)}.` : "",
    field(budget) ? `Budget: ${field(budget)}.` : "",
    field(note) ? `${field(note)}.` : "",
    "Please reply with the total before you cook. For a room, send a price per guest.",
  ].filter(Boolean);
  msg.value = lines.join(" ");
  const missing = [];
  if (!field(when)) missing.push("a date");
  if (!field(headcount)) missing.push("a headcount");
  status.textContent = missing.length
    ? `Add ${missing.join(" and ")}. She cannot price it without them.`
    : "Ready to text. This note does not charge a card.";
  const href = `sms:+13474208728?body=${encodeURIComponent(msg.value)}`;
  document.querySelectorAll("a.sms").forEach((link) => {
    link.href = href;
  });
}

[offer, when, headcount, place, diet, budget, note].forEach((node) => {
  node?.addEventListener("input", draft);
  node?.addEventListener("change", draft);
});
draft();

document.querySelector("#copy")?.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(msg.value);
    status.textContent = "Copied. Paste it into a text or an Instagram DM.";
  } catch {
    msg.focus();
    msg.select();
    status.textContent = "Message selected. Copy it, then paste into a text or DM.";
  }
});
