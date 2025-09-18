const apiUrl = 'http://localhost:8000';


async function fetchCustomers() {
  const type_name = document.getElementById("filterTypename")?.value;
  const type_contact_information = document.getElementById("filterTypecontactinformation")?.value;
  const type_address = document.getElementById("filterTypeaddress")?.value;

  const params = new URLSearchParams();
  if (type_name) params.append("type_name", type_name);
  if (type_contact_information) params.append("type_contact_information", type_contact_information);
  if (type_address) params.append("type_address", type_address);

  let customers = await fetch(`${apiUrl}/customers?${params}`).then(res => res.json());

  const tbody = document.querySelector("#customersTable tbody");
  if (tbody) {
    tbody.innerHTML = "";
    customers.forEach(d => {
      tbody.innerHTML += `
        <tr>
          <td>${d.login}</td>
          <td>${d.password}</td>
          <td>${d.name}</td>
          <td>${d.contact_information}</td>
          <td>${d.address}</td>
          
          <td>${d.comments || ''}</td>
          <td>
            <button onclick="editCustomer('${d.name}')">Edit</button>
            <button onclick="deleteCustomer('${d.name}')">Delete</button>
          </td>
        </tr>
      `;
    });
  }
}

function editCustomer(name) {
  window.location.href = `customer_form.html?edit=${encodeURIComponent(name)}`;
}

async function deleteCustomer(name) {
  await fetch(`${apiUrl}/customers/${encodeURIComponent(name)}`, { method: 'DELETE' });
  fetchCustomers();
}

async function submitCustomer(event) {
  event.preventDefault();

  const urlParams = new URLSearchParams(window.location.search);
  const editName = urlParams.get('edit');

  const customer = {
    login: document.getElementById("login").value,
    password: document.getElementById("password").value,
    name: document.getElementById("name").value,
    contact_information: document.getElementById("contact_information").value,
    address: document.getElementById("contact_information").value,
    is_available: document.getElementById("available").value === 'true',
    comments: document.getElementById("comments").value
  };

  const method = editName ? 'PUT' : 'POST';
  const endpoint = editName ? `${apiUrl}/customers/${encodeURIComponent(editName)}` : `${apiUrl}/customers`;

  await fetch(endpoint, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(customer)
  });

  window.location.href = 'index.html';
}

async function exportCustomers() {
  const data = await fetch(`${apiUrl}/customers/export`).then(res => res.json());
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'customers.json';
  a.click();
}

async function importCustomers() {
  const file = document.getElementById("importFile").files[0];
  const text = await file.text();
  const data = JSON.parse(text);
  await fetch(`${apiUrl}/customers/import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  alert("Customers imported");
}





async function fetchTCs() {
  const type_registration_number = document.getElementById("filterTyperegistrationnumber")?.value;
  const type_tcs = document.getElementById("filterTypetc")?.value;
  const available = document.getElementById("filterAvailable")?.value;

  const params = new URLSearchParams();
  if (type_registration_number) params.append("type_registration_number", type_registration_number);
  if (type_tcs) params.append("type_tc", type_tcs);
  if (available !== '') params.append("is_available", available);

  let tcs = await fetch(`${apiUrl}/tcs?${params}`).then(res => res.json());

  const tbody = document.querySelector("#tcsTable tbody");
  if (tbody) {
    tbody.innerHTML = "";
    tcs.forEach(d => {
      tbody.innerHTML += `
        <tr>
          <td>${d.type_tc}</td>
          <td>${d.registration_number}</td>
          <td>${d.is_available}</td>
          <td>${d.comments || ''}</td>
          <td>
            <button onclick="editTC('${d.registration_number}')">Edit</button>
            <button onclick="deleteTC('${d.registration_number}')">Delete</button>
          </td>
        </tr>
      `;
    });
  }
}

function editTC(registration_number) {
  window.location.href = `tc_form.html?edit=${encodeURIComponent(registration_number)}`;
}

async function deleteTC(registration_number) {
  await fetch(`${apiUrl}/tcs/${encodeURIComponent(registration_number)}`, { method: 'DELETE' });
  fetchTCs();
}

async function submitTC(event) {
  event.preventDefault();

  const urlParams = new URLSearchParams(window.location.search);
  const editName = urlParams.get('edit');

  const tc = {
    type_tc: document.getElementById("type_tc").value,
    registration_number: document.getElementById("registration_number").value,
    is_available: document.getElementById("available").value === 'true',
    comments: document.getElementById("comments").value
  };

  const method = editName ? 'PUT' : 'POST';
  const endpoint = editName ? `${apiUrl}/tcs/${encodeURIComponent(editName)}` : `${apiUrl}/tcs`;

  await fetch(endpoint, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(tc)
  });

  window.location.href = 'tc.html';
}

async function exportTCs() {
  const data = await fetch(`${apiUrl}/tcs/export`).then(res => res.json());
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'tcs.json';
  a.click();
}

async function importTCs() {
  const file = document.getElementById("importFile").files[0];
  const text = await file.text();
  const data = JSON.parse(text);
  await fetch(`${apiUrl}/tcs/import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  alert("TCs imported");
}



async function fetchRents() {
  const type_order_name = document.getElementById("filterTypeordername")?.value;
  const type_registration_number = document.getElementById("filterTyperegistrationnumber")?.value;
  const type_rent_id = document.getElementById("filterTyperentid")?.value;
  const type_date_of_begining = document.getElementById("filterTypedateofbegining")?.value;
  const type_date_of_ending = document.getElementById("filterTypedateofending")?.value;
  const params = new URLSearchParams();
  if (type_order_name) params.append("type_order_name", type_order_name);
  if (type_registration_number) params.append("type_registration_number", type_registration_number);
  if (type_rent_id) params.append("type_rent_id", type_rent_id);
  if (type_date_of_begining) params.append("type_date_of_begining", type_date_of_begining);
  if (type_date_of_ending) params.append("type_date_of_ending", type_date_of_ending);
 
  let rents = await fetch(`${apiUrl}/rents?${params}`).then(res => res.json());

  const tbody = document.querySelector("#rentsTable tbody");
  if (tbody) {
    tbody.innerHTML = "";
    rents.forEach(d => {
      tbody.innerHTML += `
        <tr>
          <td>${d.rent_id}</td>
          <td>${d.date_of_begining}</td>
          <td>${d.date_of_ending}</td>
          <td>${d.order_name}</td>
          <td>${d.tc_registration_number}</td>
          <td>
            <button onclick="editRent('${d.rent_id}')">Edit</button>
            <button onclick="deleteRent('${d.rent_id}')">Delete</button>
          </td>
        </tr>
      `;
    });
  }
}

function editRent(rent_id) {
  window.location.href = `rent_form.html?edit=${encodeURIComponent(rent_id)}`;
}

async function deleteRent(rent_id) {
  await fetch(`${apiUrl}/rents/${encodeURIComponent(rent_id)}`, { method: 'DELETE' });
  fetchRents();
}

async function submitRent(event) {
  event.preventDefault();

  const urlParams = new URLSearchParams(window.location.search);
  const editName = urlParams.get('edit');

  const rent = {
    rent_id: document.getElementById("rent_id").value,
    date_of_begining: document.getElementById("date_of_begining").value,
    date_of_ending: document.getElementById("date_of_ending").value,
    order_name: document.getElementById("order_name").value,
    tc_registration_number: document.getElementById("tc_registration_number").value,
  };

  const method = editName ? 'PUT' : 'POST';
  const endpoint = editName ? `${apiUrl}/rents/${encodeURIComponent(editName)}` : `${apiUrl}/rents`;

  await fetch(endpoint, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(rent)
  });

  window.location.href = 'rent.html';
}

async function exportRents() {
  const data = await fetch(`${apiUrl}/rents/export`).then(res => res.json());
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'rents.json';
  a.click();
}

async function importRents() {
  const file = document.getElementById("importFile").files[0];
  const text = await file.text();
  const data = JSON.parse(text);
  await fetch(`${apiUrl}/rents/import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  alert("Transactions imported");
}
