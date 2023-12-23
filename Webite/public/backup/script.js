
// Firebase configuration
const firebaseConfig = {
	apiKey: 'AIzaSyD2YPsAAvfCmHxtfxXtk8RHjCgj9GhGbW8',
	authDomain: 'compsysass.firebaseapp.com',
	databaseURL:
		'https://compsysass-default-rtdb.europe-west1.firebasedatabase.app',
	projectId: 'compsysass',
	storageBucket: 'compsysass.appspot.com',
	messagingSenderId: '515566407723',
	appId: '1:515566407723:web:d023a1f9f2a53d9cc21a6e',
	measurementId: 'G-VVC6HRTG8K',
};

firebase.initializeApp(firebaseConfig);

// Get a reference to the file storage service
const storage = firebase.storage();
// Get a reference to the database service
const database = firebase.database();

// Create camera database reference
const auditTrailRef = database.ref('audittrail');
// Create devices database reference
const devicesRef = database.ref('devices');

const adminRef = database.ref('admin');

// Function to render devices list
// Modify the renderDevices function to create columns for each device
function renderDevices(devices) {
	const devicesList = document.getElementById('devicesList');

	devicesList.innerHTML = ''; // Clear previous list items

	devices.forEach((device, index) => {
		if (index === 0) return; // Ignore the first device added this as i had an issue as had setup the database with devices 1-5 not using 0 index. the JS script kept adding in the 0 index which is not needed.

		const column = document.createElement('div');
		column.className = `column ${device.status.toLowerCase()}`;

		const deviceName = document.createElement('p');
		deviceName.textContent = `Device#${index}`;
		column.appendChild(deviceName);

		const deviceStatus = document.createElement('p');
		deviceStatus.textContent = `${device.status}`;
		column.appendChild(deviceStatus);

		const switchContainer = document.createElement('div');
		switchContainer.className = 'switch-container';

		const switchLabel = document.createElement('label');
		switchLabel.className = 'switch';

		const switchInput = document.createElement('input');
		switchInput.type = 'checkbox';
		switchInput.checked = device.status === 'ON';

		switchInput.addEventListener('change', () => {
			// Update the device status in the database
			devicesRef
				.child(index)
				.update({ status: switchInput.checked ? 'ON' : 'OFF' });
		});

		const switchSlider = document.createElement('span');
		switchSlider.className = 'slider';

		switchLabel.appendChild(switchInput);
		switchLabel.appendChild(switchSlider);
		switchContainer.appendChild(switchLabel);
		column.appendChild(switchContainer);

		devicesList.appendChild(column);
	});
}

// Function to update device status on real-time changes
devicesRef.on('value', function (snapshot) {
	const devicesData = snapshot.val();

	if (devicesData && Array.isArray(devicesData)) {
		renderDevices(devicesData.filter((device) => device !== null));
	}
});

// Sync on any updates to the DB. THIS CODE RUNS EVERY TIME AN UPDATE OCCURS ON THE DB.
// auditTrailRef.limitToLast(1).on('value', function (snapshot) {
// 	snapshot.forEach(function (childSnapshot) {
// 		const image = childSnapshot.val()['image'];
// 		const time = childSnapshot.val()['timestamp'];
// 		const storageRef = storage.ref('access/' + image);

// 		storageRef
// 			.getDownloadURL()
// 			.then(function (url) {
// 				console.log(url);
// 				document.getElementById('photo').src = url;
// 				document.getElementById('time').innerText = time;
// 				document.getElementById('image').innerText = image;
// 			})
// 			.catch(function (error) {
// 				console.log(error);
// 			});
// 	});
// });

// Function to render audit trail
function renderAuditTrail(auditTrail) {
	const tableBody = document
		.getElementById('auditTrailTable')
		.querySelector('tbody');
	const imageModal = document.getElementById('imageModal');
	const modalImage = document.getElementById('modalImage');
	const closeModal = document.getElementById('closeModal');

	tableBody.innerHTML = ''; // Clear previous table rows

	auditTrail.forEach((item) => {
		const row = document.createElement('tr');

		Object.entries(item).forEach(([key, value]) => {
			if (key === 'image') return; // Ignore the image

			const cell = document.createElement('td');

			if (key === 'image_url') {
				const img = document.createElement('img');
				img.src = value;
				img.style.width = '150px'; // Adjust the size as needed
				img.style.cursor = 'pointer'; // Change the cursor to a pointer when hovering over the image
				img.onclick = function () {
					modalImage.src = value;
					imageModal.classList.add('is-active');
				};
				cell.appendChild(img);
			} else {
				cell.textContent = value;
			}

			row.appendChild(cell);
		});

		tableBody.appendChild(row);
	});

	closeModal.onclick = function () {
		imageModal.classList.remove('is-active');
	};
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

// function getAuditTrail() {
//   let query = auditTrailRef
//       .orderByChild('timestamp')
//       .limitToLast(5);

//   query.once('value').then((snapshot) => {
//       const auditTrailData = snapshot.val();
//       const auditTrailArray = Object.values(auditTrailData);

//       // Reverse the array to display the latest results first
//       const latestItems = auditTrailArray.reverse();

//       renderAuditTrail(latestItems);
//   });
// }

// Get the initial audit trail data
getAuditTrail(true);

document.addEventListener('DOMContentLoaded', function () {
	document
		.getElementById('admin-form')
		.addEventListener('submit', function (event) {
			event.preventDefault();

			const enteredPassword = document.getElementById('password-input').value;

			// Fetch the password from the Firebase database
			// const adminRef = firebase.database().ref('admin');
			adminRef.once('value').then(function (snapshot) {
				const password = snapshot.val().password;

				console.log(`Entered password: "${enteredPassword}"`);
				console.log(`Password from database: "${password}"`);

				if (enteredPassword == password) {
					// Enable the switches
					alert('Correct password: ' + password);
					// Replace '.switch' with the actual selector of your switches
					const switches = document.querySelectorAll('.switch');
					switches.forEach(function (switchElement) {
						//switchElement.disabled = false;
						switchElement.style.pointerEvents = 'all';
						switchElement.style.opacity = '1';
					});
				} else {
					alert('Incorrect password: ' + password);
				}
			});
		});
});
