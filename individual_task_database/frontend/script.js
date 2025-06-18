const apiUrl = 'http://localhost:8000';

async function fetchDrivers() {
  const category = document.getElementById("filterCategory")?.value;
  const minExp = document.getElementById("filterExpMin")?.value;
  const maxExp = document.getElementById("filterExpMax")?.value;
  const available = document.getElementById("filterAvailable")?.value;

  const params = new URLSearchParams();
  if (category) params.append("category", category);
  if (minExp) params.append("min_experience", minExp);
  if (available !== '') params.append("is_available", available);

  let drivers = await fetch(`${apiUrl}/drivers?${params}`).then(res => res.json());

  if (maxExp) {
    drivers = drivers.filter(d => d.experience_years <= parseInt(maxExp));
  }

  const tbody = document.querySelector("#driversTable tbody");
  if (tbody) {
    tbody.innerHTML = "";
    drivers.forEach(d => {
      tbody.innerHTML += `
        <tr>
          <td>${d.name}</td>
          <td>${d.license_categories.join(', ')}</td>
          <td>${d.experience_years}</td>
          <td>${d.is_available}</td>
          <td>${d.comments || ''}</td>
          <td>
            <button onclick="editDriver('${d.name}')">Edit</button>
            <button onclick="deleteDriver('${d.name}')">Delete</button>
          </td>
        </tr>
      `;
    });
  }
}

function editDriver(name) {
  window.location.href = `form.html?edit=${encodeURIComponent(name)}`;
}

async function deleteDriver(name) {
  await fetch(`${apiUrl}/drivers/${encodeURIComponent(name)}`, { method: 'DELETE' });
  fetchDrivers();
}

async function submitDriver(event) {
  event.preventDefault();

  const urlParams = new URLSearchParams(window.location.search);
  const editName = urlParams.get('edit');

  const driver = {
    name: document.getElementById("name").value,
    license_categories: document.getElementById("categories").value.split(',').map(c => c.trim()),
    experience_years: parseInt(document.getElementById("experience").value),
    is_available: document.getElementById("available").value === 'true',
    comments: document.getElementById("comments").value
  };

  const method = editName ? 'PUT' : 'POST';
  const endpoint = editName ? `${apiUrl}/drivers/${encodeURIComponent(editName)}` : `${apiUrl}/drivers`;

  await fetch(endpoint, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(driver)
  });

  window.location.href = 'table.html';
}

async function exportDrivers() {
  const data = await fetch(`${apiUrl}/drivers/export`).then(res => res.json());
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'drivers.json';
  a.click();
}

async function importDrivers() {
  const file = document.getElementById("importFile").files[0];
  const text = await file.text();
  const data = JSON.parse(text);
  await fetch(`${apiUrl}/drivers/import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  alert("Drivers imported");
}
