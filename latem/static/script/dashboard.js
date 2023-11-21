let clients = JSON.parse(document.currentScript.nextElementSibling.textContent)

console.log(clients)

const confirmationAlert=(event, form)=>{
	   let confirmation = confirm("Êtes-vous sûr de vouloir appliquer ces changements ?");
        
        // Si l'utilisateur annule la confirmation, annuler la soumission du formulaire
        if (!confirmation) {
            event.preventDefault();
        }
        else{
        	form.submit()
        }
}

const selectClient=(id)=> {

	let form = document.getElementById('createDevisForm')
	let inputId=form.querySelector('#id_clientId')
	inputId.value=id
	let inputIdFormulaire=form.querySelector('#id_formulaire_id')
	inputIdFormulaire.value='devis'
	
	confirmationAlert(event,form)
}

const openPopUp=(idPopup)=>{
	if (idPopup=='devisPopup'){
		let table = document.getElementById('clientTable')
		let tbody = document.getElementById('clientList')

		clients.forEach(client => {let row = document.createElement('tr');

		    // Chaque cellule de la ligne
		    let cellFirstName = document.createElement('td');
		    cellFirstName.textContent = client.firstName;
		    row.appendChild(cellFirstName);

		    let cellLastName = document.createElement('td');
		    cellLastName.textContent = client.lastName;
		    row.appendChild(cellLastName);

		    let cellEmail = document.createElement('td');
		    cellEmail.textContent = client.email;
		    row.appendChild(cellEmail);

		    // Ajoutez un gestionnaire d'événements à la ligne
		    row.addEventListener('click', () => selectClient(client.id));

		    // Ajoutez la ligne au corps de la table
		    tbody.appendChild(row);
		});
	}
	else if (idPopup=='clientPopup'){
		form = document.getElementById('createClientForm')
		let inputIdFormulaire=form.querySelector('#id_formulaire_id')
		inputIdFormulaire.value='client'
	}
	let popUp = document.getElementById(idPopup)
	popUp.style.display='block'
}

const validatePopUp=(idPopup)=>{
	let popUp = document.getElementById(idPopup)
	popUp.style.display='none'
	if (idPopup=='devisPopup'){
		let listItem = document.getElementById('clientList')
		listItem.innerHTML=''
	}
}

const sortClients=(input)=> {
	if (event.keyCode==13 || event.key==='Tab' || event.keyCode ==229){
	let table = document.getElementById('clientTable')
	let tbody = document.getElementById('clientList')
    const filterText = input.value.toLowerCase();

    // Parcourez toutes les lignes de la table
    const rows = tbody.getElementsByTagName('tr');
    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];

        // Parcourez toutes les cellules de la ligne (sauf la dernière colonne avec les boutons)
        const cells = row.getElementsByTagName('td');
        let rowContainsText = false;
        for (let j = 0; j < cells.length; j++) {
            const cellText = cells[j].textContent.toLowerCase();
            if (cellText.includes(filterText)) {
                rowContainsText = true;
                break;
            }
        }

        // Affichez ou masquez la ligne en fonction du texte filtré
        row.style.display = rowContainsText ? '' : 'none';
    }
}}