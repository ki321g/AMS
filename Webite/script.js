let storage, database, auditTrailRef, devicesRef, adminRef;

// Firebase configuration
// Function to fetch the config from the server
const fetchConfig = async () => {
	try {
		console.log('Fetch Firebase config...');
		const response = await fetch('/firebase/config');
		const firebaseConfig = await response.json();

		return firebaseConfig;
	} catch (error) {
		console.error('Error fetching config:', error);
	}
};

// Initialize Firebase
fetchConfig().then((firebaseConfig) => {
	console.log('Initialize Firebase App...');
	//Degbbug
	//console.log(firebaseConfig);

	firebase.initializeApp(firebaseConfig); // Initialize Firebase with the config

	storage = firebase.storage(); // Get a reference to the file storage service
	database = firebase.database(); // Get a reference to the database service
	auditTrailRef = database.ref('audittrail'); // Create camera database reference
	devicesRef = database.ref('devices'); // Create devices database reference
	adminRef = database.ref('admin'); // Create admin database reference

	updateDevices(); // Update the devices list on real-time changes
	getAuditTrail(); // Get the initial audit trail data
});

// Function to update the devices list on real-time changes
function updateDevices() {
	devicesRef.on('value', function (snapshot) {
		const devicesData = snapshot.val();

		// Filter out any null values
		if (devicesData && Array.isArray(devicesData)) {
			renderDevices(devicesData.filter((device) => device !== null));
		}
	});
}

// Function to render devices list
function renderDevices(devices) {
	const devicesList = document.getElementById('devicesList');

	devicesList.innerHTML = ''; // Clear previous list items

	devices.forEach((device, index) => {
		/* Ignore the first device added this as i had an issue as had setup the database with devices 1-5 not using 0 index. the JS script kept adding in the 0 index which is not needed. */
		if (index === 0) return;

		const column = document.createElement('div'); // Create a column
		column.className = `column ${device.status.toLowerCase()}`; // Add the status as a class

		const deviceName = document.createElement('p'); // Create a paragraph
		deviceName.textContent = `Device#${index}`; // Set the text content
		column.appendChild(deviceName); // Append the paragraph to the column

		const deviceStatus = document.createElement('p'); // Create a paragraph
		deviceStatus.textContent = `${device.status}`; // Set the text content
		column.appendChild(deviceStatus); // Append the paragraph to the column

		const switchContainer = document.createElement('div'); // Create a div
		switchContainer.className = 'switch-container'; // Add the class 'switch-container'

		const switchLabel = document.createElement('label'); // Create a label
		switchLabel.className = 'switch'; // Add the class 'switch'

		const switchInput = document.createElement('input'); // Create an input
		switchInput.type = 'checkbox'; // Set the type to 'checkbox'
		switchInput.checked = device.status === 'ON'; // Set the checked status based on the device status

		// Add an event listener to the switch to Update the device status in the database
		switchInput.addEventListener('change', () => {
			devicesRef
				.child(index)
				.update({ status: switchInput.checked ? 'ON' : 'OFF' });
		});

		const switchSlider = document.createElement('span'); // Create a span
		switchSlider.className = 'slider'; // Add the class 'slider'

		switchLabel.appendChild(switchInput); // Append the input to the label
		switchLabel.appendChild(switchSlider); // Append the span to the label
		switchContainer.appendChild(switchLabel); // Append the label to the switch container
		column.appendChild(switchContainer); // Append the switch container to the column

		devicesList.appendChild(column); // Append the column to the devices list
	});
}

// Function to render audit trail
function renderAuditTrail(auditTrail) {
	const tableBody = document
		.getElementById('auditTrailTable')
		.querySelector('tbody');
	const imageModal = document.getElementById('imageModal'); // Get the modal
	const modalImage = document.getElementById('modalImage'); // Get the image
	const closeModal = document.getElementById('closeModal'); // Get the close button

	tableBody.innerHTML = ''; // Clear previous table rows

	// For each item in the audit trail, create a table row and append the data
	auditTrail.forEach((item) => {
		const row = document.createElement('tr'); // Create a table row

		Object.entries(item).forEach(([key, value]) => {
			if (key === 'image') return; // Ignore the image name as we don't need it

			const cell = document.createElement('td'); // Create a table cell

			if (key === 'image_url') {
				const img = document.createElement('img');
				img.src = value; // Set the image source
				img.style.width = '150px'; // Adjust the size as needed
				img.style.cursor = 'pointer'; // Change the cursor to a pointer when hovering over the image

				// Add an event listener to the image to open the modal
				img.onclick = function () {
					modalImage.src = value;
					imageModal.classList.add('is-active');
				};
				cell.appendChild(img); // Append the image to the cell
			} else {
				cell.textContent = value; // Set the text content of the cell
			}

			row.appendChild(cell); // Append the cell to the row
		});

		tableBody.appendChild(row);
	}); // End of forEach loop
}

// Function to get the audit trail data
function getAuditTrail() {
	let query = auditTrailRef.orderByChild('timestamp').limitToLast(5);

	query.on('value', (snapshot) => {
		const auditTrailData = snapshot.val();
		const auditTrailArray = Object.values(auditTrailData);

		// Reverse the array to display the latest results first
		const latestItems = auditTrailArray.reverse();

		renderAuditTrail(latestItems);
	});
}

document.addEventListener('DOMContentLoaded', function () {
	// navbar button event listener to enable the password modal
	document
		.querySelector('.navbar .button')
		.addEventListener('click', function () {
			const target = this.getAttribute('data-target');
			const modal = document.getElementById(target);
			modal.classList.add('is-active');
			document.getElementById('password-input').focus();
		});

	// password modal close button event listener to disable the password modal
	document
		.querySelector('#password-modal .modal-close')
		.addEventListener('click', function () {
			this.parentElement.classList.remove('is-active');
		});

	// password modal form event listener to check the password
	document
		.getElementById('admin-form')
		.addEventListener('submit', function (event) {
			event.preventDefault();

			const passwordError = document.getElementById('password-error'); // Get the password-error label
			// Get the entered password
			const enteredPassword = this.querySelector(
				'input[type="password"]'
			).value;

			this.querySelector('#password-input').value = ''; // Clear the password input

			// Get the password from the database
			adminRef.once('value').then(function (snapshot) {
				const password = snapshot.val().password;

				//debugging
				//console.log(`Entered password: "${enteredPassword}"`); // Log the entered password
				//console.log(`Password from database: "${password}"`); // Log the password from the database

				if (enteredPassword == password) {
					// Close the modal
					document
						.getElementById('password-modal')
						.classList.remove('is-active');

					passwordError.style.display = 'none'; // Disable the password-error label

					const switches = document.querySelectorAll('.switch'); // Get all the switches
					// Enable the switches
					switches.forEach(function (switchElement) {
						switchElement.style.pointerEvents = 'all';
						switchElement.style.opacity = '1';
					});
				} else {
					// Enable the password-error label
					passwordError.style.display = 'block';
					passwordError.textContent = 'Password Incorrect!';
					event.target.querySelector('input[type="password"]').value = ''; // Clear the password input
					event.target.querySelector('input[type="password"]').focus();
				}
			});
		});

	document.getElementById('close-modal').addEventListener('click', function () {
		document.getElementById('password-modal').classList.remove('is-active'); // Close the modal
		const passwordError = document.getElementById('password-error'); // Get the password-error label
		passwordError.style.display = 'none'; // Disable the password-error label
		const passwordInput = document.getElementById('password-input'); // Get the password-error label
		passwordInput.value = ''; // Clear the password input
	});

	document
		.querySelector('#imageModal .modal-close')
		.addEventListener('click', function () {
			this.parentElement.classList.remove('is-active');
		});

	document
		.getElementById('close-modal-image')
		.addEventListener('click', function () {
			document.getElementById('imageModal').classList.remove('is-active');
		});
});
