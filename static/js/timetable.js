const method = document.getElementById('method');
const manual = document.getElementById('manualFields');

if (method) {
  const toggle = () => {
    manual.classList.toggle('hidden', method.value !== 'manual');
  };
  method.addEventListener('change', toggle);
  toggle();
}
