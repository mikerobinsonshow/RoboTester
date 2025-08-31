document.addEventListener('DOMContentLoaded', () => {
  fetch('/schema')
    .then((res) => res.json())
    .then((fields) => renderForm(fields));
});

function renderForm(fields) {
  const form = document.getElementById('dynamic-form');
  form.innerHTML = '';
  fields.forEach((field) => {
    const wrapper = document.createElement('div');

    const label = document.createElement('label');
    label.textContent = field.label;
    label.setAttribute('for', field.name);

    let input;
    if (field.type === 'checkbox') {
      input = document.createElement('input');
      input.type = 'checkbox';
    } else {
      input = document.createElement('input');
      input.type = field.type || 'text';
    }
    input.name = field.name;
    input.id = field.name;

    if (field.validation) {
      if (field.validation.required) input.required = true;
      if (field.validation.minLength) input.minLength = field.validation.minLength;
      if (field.validation.min !== undefined) input.min = field.validation.min;
      if (field.validation.max !== undefined) input.max = field.validation.max;
    }

    wrapper.appendChild(label);
    wrapper.appendChild(input);
    form.appendChild(wrapper);

    if (typeof attachValidation === 'function') {
      attachValidation(input, field.validation || {});
    }
  });
  const submit = document.createElement('button');
  submit.type = 'submit';
  submit.textContent = 'Submit';
  form.appendChild(submit);
}
