const form = document.getElementById("churn-form");
const submitBtn = form.querySelector(".submit-btn");
const btnText = form.querySelector(".btn-text");
const btnSpinner = form.querySelector(".btn-spinner");

const gaugeFill = document.getElementById("gauge-fill");
const gaugeNumber = document.getElementById("gauge-number");
const verdict = document.getElementById("verdict");

const CIRCUMFERENCE = 377; // 2 * PI * r(60), matches stroke-dasharray in CSS

function setGauge(pct, isRisk) {
  const offset = CIRCUMFERENCE - (CIRCUMFERENCE * pct) / 100;
  gaugeFill.style.strokeDashoffset = offset;
  gaugeFill.style.stroke = isRisk ? "#e11d48" : "#059669";
  gaugeNumber.textContent = `${pct}%`;
}

function setVerdict(prediction, pct) {
  verdict.classList.remove("safe", "risk");
  if (prediction === "Yes") {
    verdict.classList.add("risk");
    verdict.textContent = `High risk — ${pct}% likely to churn`;
  } else {
    verdict.classList.add("safe");
    verdict.textContent = `Low risk — ${pct}% likely to churn`;
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  submitBtn.disabled = true;
  btnText.textContent = "Checking...";
  btnSpinner.hidden = false;

  const payload = Object.fromEntries(new FormData(form).entries());

  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error("Request failed");

    const data = await res.json();
    setGauge(data.probability, data.prediction === "Yes");
    setVerdict(data.prediction, data.probability);
  } catch (err) {
    verdict.classList.remove("safe", "risk");
    verdict.textContent = "Something went wrong — please try again.";
  } finally {
    submitBtn.disabled = false;
    btnText.textContent = "Check risk";
    btnSpinner.hidden = true;
  }
});
