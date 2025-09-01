document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('dynamic-form');
  form.addEventListener('submit', handleSubmit);
  const newFormBtn = document.getElementById('new-form');
  if (newFormBtn) {
    newFormBtn.addEventListener('click', () => window.location.reload());
  }
  fetch('/schema')
    .then((res) => res.json())
    .then((fields) => renderForm(fields));
});

function handleSubmit(event) {
  event.preventDefault();
  const form = event.target;
  const data = {};
  new FormData(form).forEach((value, key) => {
    data[key] = value;
  });

  fetch('/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
    .then((res) =>
      res
        .json()
        .then((json) => ({ ok: res.ok, json }))
        .catch(() => ({ ok: res.ok, json: {} }))
    )
    .then(({ ok, json }) => {
      const result = document.getElementById('result');
      result.innerHTML = '';
      if (ok) {
        const link = document.createElement('a');
        link.href = json.pdf_url;
        link.textContent = 'Download PDF';
        result.appendChild(link);
      } else if (json.errors) {
        result.textContent = Object.values(json.errors).flat().join(', ');
      } else if (json.error) {
        result.textContent = json.error;
      } else {
        result.textContent = 'Submission failed';
      }
    })
    .catch(() => {
      const result = document.getElementById('result');
      result.textContent = 'Submission failed';
    });
}

function renderForm(fields) {
  const form = document.getElementById('dynamic-form');
  form.innerHTML = '';
  const midpoint = Math.ceil(fields.length / 2);
  const page1 = document.createElement('div');
  page1.classList.add('form-page');
  const page2 = document.createElement('div');
  page2.classList.add('form-page', 'hidden');

  fields.forEach((field, index) => {
    const wrapper = document.createElement('div');
    wrapper.classList.add('nice-form-group');

    const label = document.createElement('label');
    label.textContent = field.label;
    label.setAttribute('for', field.name);

    let input;
    if (field.type === 'checkbox') {
      input = document.createElement('input');
      input.type = 'checkbox';
      input.name = field.name;
      input.id = field.name;
      wrapper.appendChild(input);
      wrapper.appendChild(label);
    } else {
      input = document.createElement('input');
      input.type = field.type || 'text';
      input.name = field.name;
      input.id = field.name;
      wrapper.appendChild(label);
      wrapper.appendChild(input);
    }

    if (field.validation) {
      if (field.validation.required) input.required = true;
      if (field.validation.minLength) input.minLength = field.validation.minLength;
      if (field.validation.min !== undefined) input.min = field.validation.min;
      if (field.validation.max !== undefined) input.max = field.validation.max;
    }

    const targetPage = index < midpoint ? page1 : page2;
    targetPage.appendChild(wrapper);

    if (typeof attachValidation === 'function') {
      attachValidation(input, field.validation || {});
    }
  });

  const next = document.createElement('button');
  next.type = 'button';
  next.textContent = 'Next';
  next.classList.add('button');
  next.addEventListener('click', () => {
    page1.classList.add('hidden');
    page2.classList.remove('hidden');
  });
  page1.appendChild(next);

  const submit = document.createElement('button');
  submit.type = 'submit';
  submit.textContent = 'Submit';
  submit.classList.add('button');
  page2.appendChild(submit);

  form.appendChild(page1);
  form.appendChild(page2);
}
