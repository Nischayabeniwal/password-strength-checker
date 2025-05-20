const passwordInput = document.getElementById("password");
const strengthBar = document.getElementById("strength-bar");
const strengthText = document.getElementById("strength-text");
const suggestionsBox = document.getElementById("suggestions");
const generatedPasswordInput = document.getElementById("generated-password");

passwordInput.addEventListener("input", checkStrength);

function checkStrength() {
  const password = passwordInput.value;
  const score = calculateStrength(password);

  strengthBar.style.backgroundColor = score.color;
  strengthText.textContent = score.label;
  strengthText.style.color = score.color;

  const suggestions = generateSuggestions(password);
  if (suggestions.length > 0) {
    suggestionsBox.innerHTML = `<ul>${suggestions.map(s => `<li>${s}</li>`).join('')}</ul>`;
  } else {
    suggestionsBox.innerHTML = "";
  }
}

function calculateStrength(password) {
  let score = 0;
  if (password.length >= 8) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[a-z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;

  if (score <= 2) return { label: "Very Weak", color: "#dc2626" };
  if (score === 3) return { label: "Weak", color: "#f97316" };
  if (score === 4) return { label: "Moderate", color: "#facc15" };
  return { label: "Strong", color: "#16a34a" };
}

function generateSuggestions(password) {
  const tips = [];
  if (password.length < 8) tips.push("Use at least 8 characters.");
  if (!/[A-Z]/.test(password)) tips.push("Add uppercase letters.");
  if (!/[a-z]/.test(password)) tips.push("Include lowercase letters.");
  if (!/[0-9]/.test(password)) tips.push("Include numbers.");
  if (!/[^A-Za-z0-9]/.test(password)) tips.push("Use special characters.");
  return tips;
}

function toggleVisibility() {
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    document.getElementById("eye-icon").textContent = "🙈";
  } else {
    passwordInput.type = "password";
    document.getElementById("eye-icon").textContent = "👁️";
  }
}

function generatePassword() {
  const length = 12;
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+~";
  let password = "";
  for (let i = 0; i < length; i++) {
    password += chars[Math.floor(Math.random() * chars.length)];
  }
  generatedPasswordInput.value = password;
}

function copyPassword() {
  generatedPasswordInput.select();
  document.execCommand("copy");
  alert("Password copied to clipboard!");
}
