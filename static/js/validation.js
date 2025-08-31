const fieldErrors = {};

function isValidPhone(value) {
  const digits = value.replace(/\D/g, '');
  return /^\d{10}$/.test(digits);
}

function isValidSSN(value) {
  return /^\d{3}-\d{2}-\d{4}$/.test(value);
}

function withinLength(value, max = 15) {
  return value.length <= max;
}

function validateField(input, rules = {}) {
  const value = input.value.trim();
  const name = input.name;
  const errors = [];

  if (rules.required && !value) {
    errors.push(`${name} is required`);
  }

  if (value && !withinLength(value)) {
    errors.push(`${name} must be at most 15 characters`);
  }

  if (name.toLowerCase().includes('phone') && value && !isValidPhone(value)) {
    errors.push('Phone number must be 10 digits');
  }

  if (name.toLowerCase().includes('ssn') && value && !isValidSSN(value)) {
    errors.push('SSN must match ###-##-####');
  }

  if (rules.minLength && value.length < rules.minLength) {
    errors.push(`${name} must be at least ${rules.minLength} characters`);
  }

  if (rules.min !== undefined && value !== '' && Number(value) < rules.min) {
    errors.push(`${name} must be at least ${rules.min}`);
  }

  if (rules.max !== undefined && value !== '' && Number(value) > rules.max) {
    errors.push(`${name} must be at most ${rules.max}`);
  }

  if (errors.length) {
    fieldErrors[name] = errors;
  } else {
    delete fieldErrors[name];
  }
  renderErrors();
}

function renderErrors() {
  const container = document.getElementById('error-messages');
  if (!container) return;
  container.innerHTML = '';
  Object.values(fieldErrors).forEach((errs) => {
    errs.forEach((err) => {
      const p = document.createElement('p');
      p.textContent = err;
      container.appendChild(p);
    });
  });
}

function attachValidation(input, rules) {
  input.addEventListener('input', () => validateField(input, rules));
  input.addEventListener('blur', () => validateField(input, rules));
}

// expose to global scope
window.attachValidation = attachValidation;
