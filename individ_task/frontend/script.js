const apiUrl = 'http://localhost:8000';


async function fetchCars() {
  const type_registration_number = document.getElementById("filterTyperegistrationnumber")?.value;
  const type_category = document.getElementById("filterTypecategory")?.value;
  const type_model = document.getElementById("filterTypemodel")?.value;
  const type_year = document.getElementById("filterTypeyear")?.value;

  const params = new URLSearchParams();
  if (type_registration_number) params.append("type_registration_number", type_registration_number);
  if (type_category) params.append("type_category", type_category);
  if (type_model) params.append("type_model", type_model);
  if (type_year) params.append("type_year", type_year);

  let cars = await fetch(`${apiUrl}/cars?${params}`).then(res => res.json());

  const tbody = document.querySelector("#carsTable tbody");
  if (tbody) {
    tbody.innerHTML = "";
    cars.forEach(d => {
      tbody.innerHTML += `
        <tr>
          <td>${d.registration_number}</td>
          <td>${d.category}</td>
          <td>${d.model}</td>
          <td>${d.year}</td>
         
          <td>
            <button onclick="editCar('${d.registration_number}')">Edit</button>
            <button onclick="deleteCar('${d.registration_number}')">Delete</button>
          </td>
        </tr>
      `;
    });
  }
}

function editCar(registration_number) {
  window.location.href = `car_form.html?edit=${encodeURIComponent(registration_number)}`;
}

async function deleteCar(registration_number) {
  await fetch(`${apiUrl}/cars/${encodeURIComponent(registration_number)}`, { method: 'DELETE' });
  fetchCars();
}

async function submitCar(event) {
  event.preventDefault();

  const urlParams = new URLSearchParams(window.location.search);
  const editName = urlParams.get('edit');

  const car = {
    registration_number: document.getElementById("registration_number").value,
    category: document.getElementById("category").value,
    model: document.getElementById("model").value,
    year: document.getElementById("year").value,
    
  };

  const method = editName ? 'PUT' : 'POST';
  const endpoint = editName ? `${apiUrl}/cars/${encodeURIComponent(editName)}` : `${apiUrl}/cars`;

  await fetch(endpoint, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(car)
  });

  window.location.href = 'index.html';
}

async function exportCars() {
  const data = await fetch(`${apiUrl}/cars/export`).then(res => res.json());
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'cars.json';
  a.click();
}

async function importCars() {
  const file = document.getElementById("importFile").files[0];
  const text = await file.text();
  const data = JSON.parse(text);
  await fetch(`${apiUrl}/cars/import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  alert("Customers imported");
}





async function fetchMasters() {
  const type_name = document.getElementById("filterName")?.value;
  const type_qualification = document.getElementById("filterQualification")?.value;
  const minExp = document.getElementById("filterExpMin")?.value;
  const maxExp = document.getElementById("filterExpMax")?.value;
  const available = document.getElementById("filterAvailable")?.value;
  const type_comments = document.getElementById("filterTypecomments")?.value;

  const params = new URLSearchParams();
  if (type_name) params.append("name", type_name);
  if (type_qualification) params.append("type_qualification", type_qualification);
  if (minExp) params.append("min_experience", minExp);
  if (available !== '') params.append("is_available", available);
  if (type_comments) params.append("type_comments", type_comments);

  let masters = await fetch(`${apiUrl}/masters?${params}`).then(res => res.json());

  if (maxExp) {
    masters = masters.filter(d => d.experience_years <= parseInt(maxExp));
  }

  const tbody = document.querySelector("#mastersTable tbody");
  if (tbody) {
    tbody.innerHTML = "";
    drivers.forEach(d => {
      tbody.innerHTML += `
        <tr>
          <td>${d.name}</td>
          <td>${d.qualification}</td>
          <td>${d.experience_years}</td>
          <td>${d.is_available}</td>
          <td>${d.comments || ''}</td>
          <td>
            <button onclick="editMaster('${d.name}')">Edit</button>
            <button onclick="deleteMaster('${d.name}')">Delete</button>
          </td>
        </tr>
      `;
    });
  }
}

function editMaster(name) {
  window.location.href = `master_form.html?edit=${encodeURIComponent(name)}`;
}

async function deleteMaster(name) {
  await fetch(`${apiUrl}/masters/${encodeURIComponent(name)}`, { method: 'DELETE' });
  fetchMasters();
}

async function submitMaster(event) {
  event.preventDefault();

  const urlParams = new URLSearchParams(window.location.search);
  const editName = urlParams.get('edit');

  const master = {
    name: document.getElementById("name").value,
    qualification: document.getElementById("type_qualification").value,
    experience_years: parseInt(document.getElementById("experience").value),
    is_available: document.getElementById("available").value === 'true',
    comments: document.getElementById("comments").value
  };

const method = editName ? 'PUT' : 'POST';
  const endpoint = editName ? `${apiUrl}/masters/${encodeURIComponent(editName)}` : `${apiUrl}/masters`;

  await fetch(endpoint, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(master)
  });

  window.location.href = 'master.html';
}

async function exportMasters() {
  const data = await fetch(`${apiUrl}/masters/export`).then(res => res.json());
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'masters.json';
  a.click();
}

async function importMasters() {
  const file = document.getElementById("importFile").files[0];
  const text = await file.text();
  const data = JSON.parse(text);
  await fetch(`${apiUrl}/masters/import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  alert("TCs imported");
}



async function fetchGarages() {
  const type_garage_id = document.getElementById("filterTypegarageid")?.value;
  const type_address = document.getElementById("filterTypeaddress")?.value;
  const available = document.getElementById("filterAvailable")?.value;
  const type_comments = document.getElementById("filterTypecomments")?.value;

  const params = new URLSearchParams();
  if (type_garage_id) params.append("type_garage_id", type_garage_id);
  if (type_address) params.append("type_address", type_address);
  if (available !== '') params.append("is_available", available);
  if (type_comments) params.append("type_comments", type_comments);
 
  let garages = await fetch(`${apiUrl}/garages?${params}`).then(res => res.json());

  const tbody = document.querySelector("#garagesTable tbody");
  if (tbody) {
    tbody.innerHTML = "";
    garages.forEach(d => {
      tbody.innerHTML += `
        <tr>
          <td>${d.garage_id}</td>
          <td>${d.address}</td>
          <td>${d.is_available}</td>
          <td>${d.comments}</td>
          <td>
            <button onclick="editGarage('${d.garage_id}')">Edit</button>
            <button onclick="deleteGarage('${d.garage_id}')">Delete</button>
          </td>
        </tr>
      `;
    });
  }
}

function editGarage(garage_id) {
  window.location.href = `garage_form.html?edit=${encodeURIComponent(garage_id)}`;
}

async function deleteGarage(garage_id) {
  await fetch(`${apiUrl}/garages/${encodeURIComponent(garage_id)}`, { method: 'DELETE' });
  fetchGarages();
}

async function submitGarage(event) {
  event.preventDefault();

  const urlParams = new URLSearchParams(window.location.search);
  const editName = urlParams.get('edit');

  const garage = {
    garage_id: document.getElementById("garage_id").value,
    address: document.getElementById("address").value,
    is_available: document.getElementById("is_available").value,
    comments: document.getElementById("comments").value
  };

  const method = editName ? 'PUT' : 'POST';
  const endpoint = editName ? `${apiUrl}/garages/${encodeURIComponent(editName)}` : `${apiUrl}/garages`;

  await fetch(endpoint, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(garage)
  });

  window.location.href = 'garage.html';
}

async function exportGarages() {
  const data = await fetch(`${apiUrl}/garages/export`).then(res => res.json());
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'garages.json';
  a.click();
}

async function importGarages() {
  const file = document.getElementById("importFile").files[0];
  const text = await file.text();
  const data = JSON.parse(text);
  await fetch(`${apiUrl}/garages/import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  alert("Transactions imported");
}




async function fetchFlights() {
  const type_flight_id = document.getElementById("filterTypegarageid")?.value;
  const type_master_name = document.getElementById("filterTypegarageid")?.value;
  const type_registration_number = document.getElementById("filterTypegarageid")?.value;
  const type_garage_id = document.getElementById("filterTypegarageid")?.value;
  const type_date_of_begining_from = document.getElementById("filterTypeaddress")?.value;
  const type_date_of_begining_to = document.getElementById("filterTypeaddress")?.value;
  const type_date_of_ending_from = document.getElementById("filterTypeaddress")?.value;
  const type_date_of_ending_to = document.getElementById("filterTypeaddress")?.value;
  const type_comments = document.getElementById("filterTypecomments")?.value;

  const params = new URLSearchParams();
  if (type_flight_id) params.append("type_flight_id", type_flight_id);
  if (type_master_name) params.append("type_master_name", type_master_name);
  if (type_registration_number) params.append("type_registration_number", type_registration_number);
  if (type_garage_id) params.append("type_garage_id", type_garage_id);
  if (type_date_of_begining_from) params.append("type_date_of_begining_from", type_date_of_begining_from);
  if (type_date_of_begining_to) params.append("type_date_of_begining_to", type_date_of_begining_to);
  if (type_date_of_ending_from) params.append("type_date_of_ending_from", type_date_of_ending_from);
  if (type_date_of_ending_to) params.append("type_date_of_ending_to", type_date_of_ending_to);
  if (type_comments) params.append("type_comments", type_comments);
 
  let rents = await fetch(`${apiUrl}/garages?${params}`).then(res => res.json());

  const tbody = document.querySelector("#garagesTable tbody");
  if (tbody) {
    tbody.innerHTML = "";
    rents.forEach(d => {
      tbody.innerHTML += `
        <tr>
          <td>${d.flight_id}</td>
          <td>${d.master_name}</td>
          <td>${d.registration_number}</td>
          <td>${d.garage_id}</td>
          <td>${d.date_of_begining}</td>
          <td>${d.date_of_ending}</td>
          <td>${d.comments}</td>
          <td>
            <button onclick="editFlight('${d.flight_id}')">Edit</button>
            <button onclick="deleteFlight('${d.flight_id}')">Delete</button>
          </td>
        </tr>
      `;
    });
  }
}

function editFlight(flight_id) {
  window.location.href = `flight_form.html?edit=${encodeURIComponent(flight_id)}`;
}

async function deleteFlight(flight_id) {
  await fetch(`${apiUrl}/flights/${encodeURIComponent(flight_id)}`, { method: 'DELETE' });
  fetchFlights();
}

async function submitFlight(event) {
  event.preventDefault();

  const urlParams = new URLSearchParams(window.location.search);
  const editName = urlParams.get('edit');

  const garage = {
    flight_id: document.getElementById("flight_id").value,
    master_name: document.getElementById("master_name").value,
    registration_number: document.getElementById("registration_number").value,
    garage_id: document.getElementById("garage_id").value,
    date_of_begining: document.getElementById("date_of_begining").value,
    date_of_ending: document.getElementById("date_of_ending").value,
    comments: document.getElementById("comments").value
  };

  const method = editName ? 'PUT' : 'POST';
  const endpoint = editName ? `${apiUrl}/flights/${encodeURIComponent(editName)}` : `${apiUrl}/flights`;

  await fetch(endpoint, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(flight)
  });

  window.location.href = 'flight.html';
}

async function exportFlights() {
  const data = await fetch(`${apiUrl}/flights/export`).then(res => res.json());
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'flights.json';
  a.click();
}

async function importFlights() {
  const file = document.getElementById("importFile").files[0];
  const text = await file.text();
  const data = JSON.parse(text);
  await fetch(`${apiUrl}/flights/import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  alert("Transactions imported");
}
