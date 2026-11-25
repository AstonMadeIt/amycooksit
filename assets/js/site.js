const toggle = document.querySelector(".nav-toggle");
const nav = document.querySelector("#nav");

toggle?.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  toggle.setAttribute("aria-expanded", String(open));
});

const offer = document.querySelector("#offer");
const note = document.querySelector("#note");
const msg = document.querySelector("#msg");
const status = document.querySelector("#status");
const textAmy = document.querySelector("#text-amy");

function draft() {
  const extra = note.value.trim();
  msg.value = `Hi Amy — I'd like ${offer.value}.${extra ? ` ${extra}.` : ""} Please confirm timing and the total.`;
  status.textContent = "";
  const body = encodeURIComponent(msg.value);
  textAmy.href = `sms:+13474208728?body=${body}`;
}

offer?.addEventListener("change", draft);
note?.addEventListener("input", draft);
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
