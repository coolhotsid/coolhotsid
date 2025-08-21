let invoices = [];
let invoiceCounter = 0;

const fileInput = document.getElementById('invoiceFiles');
const addBtn = document.getElementById('addInvoicesBtn');
const invoiceList = document.getElementById('invoiceList');
const summary = document.getElementById('summary');

addBtn.addEventListener('click', () => {
  const files = Array.from(fileInput.files);
  files.forEach(file => {
    const invoice = {
      id: invoiceCounter++,
      file,
      poNumbers: [],
      status: 'pending',
      errors: []
    };
    invoices.push(invoice);
    renderInvoice(invoice);
  });
  fileInput.value = '';
  updateSummary();
});

function renderInvoice(inv) {
  const container = document.createElement('div');
  container.className = 'invoice';
  container.id = `invoice-${inv.id}`;

  const name = document.createElement('div');
  name.textContent = `File: ${inv.file.name}`;
  container.appendChild(name);

  const poLabel = document.createElement('label');
  poLabel.textContent = 'PO numbers (comma separated):';
  container.appendChild(poLabel);

  const poInput = document.createElement('input');
  poInput.type = 'text';
  poInput.className = 'po-input';
  container.appendChild(poInput);

  const validateBtn = document.createElement('button');
  validateBtn.textContent = 'Validate';
  validateBtn.addEventListener('click', () => {
    inv.poNumbers = poInput.value.split(',').map(p => p.trim()).filter(Boolean);
    validateInvoice(inv);
  });
  container.appendChild(validateBtn);

  const status = document.createElement('div');
  status.className = 'status';
  container.appendChild(status);

  const errorList = document.createElement('div');
  errorList.className = 'error';
  container.appendChild(errorList);

  const reuploadLabel = document.createElement('label');
  reuploadLabel.textContent = 'Re-upload invoice:';
  container.appendChild(reuploadLabel);

  const reuploadInput = document.createElement('input');
  reuploadInput.type = 'file';
  reuploadInput.addEventListener('change', e => {
    if (e.target.files.length > 0) {
      inv.file = e.target.files[0];
      name.textContent = `File: ${inv.file.name}`;
      inv.status = 'pending';
      status.textContent = '';
      errorList.textContent = '';
      validateInvoice(inv);
    }
  });
  container.appendChild(reuploadInput);

  invoiceList.appendChild(container);
}

function validateInvoice(inv) {
  const statusDiv = document.querySelector(`#invoice-${inv.id} .status`);
  const errorDiv = document.querySelector(`#invoice-${inv.id} .error`);

  statusDiv.textContent = 'Status: Validating...';
  statusDiv.className = 'status';
  errorDiv.textContent = '';

  setTimeout(() => {
    inv.errors = [];
    if (!inv.file.name.toLowerCase().endsWith('.pdf')) {
      inv.errors.push('Invoice must be a PDF file. Please upload a PDF.');
    }
    if (!inv.poNumbers || inv.poNumbers.length === 0) {
      inv.errors.push('At least one PO number is required. Enter PO numbers separated by commas.');
    }

    if (inv.errors.length > 0) {
      inv.status = 'rejected';
      statusDiv.textContent = 'Status: Rejected';
      statusDiv.className = 'status status-rejected';
      errorDiv.textContent = 'Validation errors: ' + inv.errors.join(' ');
    } else {
      inv.status = 'accepted';
      statusDiv.textContent = 'Status: Accepted';
      statusDiv.className = 'status status-accepted';
      errorDiv.textContent = '';
    }
    updateSummary();
  }, 500);
}

function updateSummary() {
  if (invoices.length === 0) {
    summary.textContent = 'No invoices uploaded.';
    return;
  }
  const rejected = invoices.filter(i => i.status === 'rejected').length;
  summary.textContent = `${rejected} of ${invoices.length} invoices rejected.`;
}
