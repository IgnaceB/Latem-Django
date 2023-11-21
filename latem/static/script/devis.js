let dataset = JSON.parse(document.currentScript.nextElementSibling.textContent)
let alreadyModifying=0
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


const afficherDeleteFormulaire = (cellule,table)=>{
		let formToFill
		let inputId
		let typeOfFormInput
	switch (table){

	case 'devis':
		let id_devis = document.getElementById('devis_id').innerText
		formToFill=document.getElementById('deleteDevisForm')

		inputId=formToFill.querySelector('#id_id')
		inputId.value=id_devis
		typeOfFormInput=formToFill.querySelector('#id_formulaire_id')
		typeOfFormInput.value='deleteDevis'

		confirmationAlert(event, formToFill)
		break
	case 'description' :
		id_ligne = cellule.parentElement.getAttribute('lignedescid') 
	
		formToFill=document.getElementById('suppressionForms')
		
		inputId=formToFill.querySelector('#id_id')
		inputId.value=id_ligne

		typeOfFormInput=formToFill.querySelector('#id_formulaire_id')
		typeOfFormInput.value='deleteDescription'
	
		confirmationAlert(event, formToFill)

		break
	case 'item' :
	
		id_ligne = cellule.parentElement.getAttribute('ligneitemid') 
	
		formToFill=document.getElementById('suppressionForms')
		
		inputId=formToFill.querySelector('#id_id')
		inputId.value=id_ligne

		typeOfFormInput=formToFill.querySelector('#id_formulaire_id')
		typeOfFormInput.value='deleteItem'
	
		confirmationAlert(event, formToFill)
		break
	}


}

const afficherAddFormulaire = (cellule, table)=>{
	let typeOfFormInput
	let formToFill
	switch (table) { 
		case 'description' :
			id_item = cellule.parentElement.getAttribute('ligneitemid')
		formToFill=document.getElementById('addDescriptionForm')

		userInput = prompt(`caractéristique à ajouter à l'objet `)
		if (userInput!== null) {
			textCustom=userInput

			let inputId_item = formToFill.querySelector('#id_LignesItemsDevisId')
			inputId_item.value = id_item
			let inputId_textCustom = formToFill.querySelector('#id_textCustom')
			inputId_textCustom.value = textCustom
			typeOfFormInput=formToFill.querySelector('#id_formulaire_id')
			typeOfFormInput.value='addDescription'

			confirmationAlert(event, formToFill)
			break
		}

		case 'item' :

			formToFill=document.getElementById('createLineItemForm')
			let id_devis=document.getElementById('devis_id').innerText

			userInput = prompt(`nom de l'objet objet à ajouter au devis`)
			if (userInput!== null){
				let inputId_devis = formToFill.querySelector('#id_devisId')
				inputId_devis.value = id_devis
				let inputTextCustom = formToFill.querySelector('#id_textCustom')
				inputTextCustom.value = userInput
				typeOfFormInput = formToFill.querySelector('#id_formulaire_id')
				typeOfFormInput.value = 'addItem'

			}
			confirmationAlert(event, formToFill)
			break


	}


}

const afficherModifyFormulaire = (event,cellule,table)=>{
	let typeOfFormInput
	let formToFill
	switch (table){
	case 'devis':
		if (event==null || event.keyCode==13 || event.key==='Tab' || event.keyCode ==229){
			
		
		let id_devis = document.getElementById('devis_id').innerText
		let newStatus = document.getElementById('status').value
		let newTotal=document.getElementById('total').value
		if (newTotal==''){
			newTotal=0
		}
		let responsable=document.getElementById('responsable').value
		
		formToFill=document.getElementById('updateDevisStatusForm')
	
		let statusInput = formToFill.querySelector('#id_status')
		statusInput.value = newStatus
		let id_devisInput = formToFill.querySelector('#id_id')
		id_devisInput.value = id_devis
		let totalInput = formToFill.querySelector('#id_total')
		totalInput.value=newTotal
		let responsableInput = formToFill.querySelector('#id_responsableId')
		responsableInput.value=responsable
		typeOfFormInput= formToFill.querySelector('#id_formulaire_id')
		typeOfFormInput.value = 'updateStatus'

		confirmationAlert(event, formToFill)
	}
		break
	case 'item' :
	
		if (event.keyCode==13 || event.key ==='Tab' || event.keyCode ==229) {
			event.preventDefault()
			let quantite = cellule.firstElementChild.value
			let id_item = cellule.parentElement.getAttribute('ligneitemid')
			
			formToFill=document.getElementById('updateQuantityForm')

			let quantiteInput = formToFill.querySelector('#id_quantity')
			quantiteInput.value = quantite
			let idInput = formToFill.querySelector('#id_id')
			idInput.value = id_item
			typeOfFormInput=formToFill.querySelector('#id_formulaire_id')
			typeOfFormInput.value = 'updateQuantity'

			confirmationAlert(event, formToFill)
		}

		break
	case 'description':
		alreadyModifying++
		let celluleToModify = cellule.previousElementSibling.previousElementSibling
		let idLigneDescription= cellule.parentElement.getAttribute('lignedescid')
		if (alreadyModifying<=1){
			celluleToModify.innerHTML=`<input id="input_textCustom" type="text" value="${celluleToModify.innerText}"></input>`

		formToFill = document.getElementById('updateDescriptionForm')

		celluleToModify.addEventListener("keypress", (event2) =>{
			if (event2.keyCode==13 || event2.key==='Tab' || event2.keyCode ==229) {
			event2.preventDefault()
			let inputId = formToFill.querySelector('#id_id')
			inputId.value=idLigneDescription
			let textCustom = document.getElementById('input_textCustom').value
			let textInput = formToFill.querySelector('#id_textCustom')
			textInput.value=textCustom
			typeOfFormInput=formToFill.querySelector('#id_formulaire_id')
			typeOfFormInput.value='modifyDescription'
			confirmationAlert(event2,formToFill)
			alreadyModifying=0

	}
		})
	}
	else {
		alert("veuillez enregistrer d'abord les modifications")
	}

		break
	}


}
/*const openDropbox= async ()=> {
	 let csrf_token = $("#dropbox [name=csrfmiddlewaretoken]").val()
	 console.log(csrf_token)
    // Effectuer une requête AJAX au backend pour obtenir l'URL Dropbox
	 const response = await fetch(window.location.href, {

        method: 'POST',
        headers: {
              	'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrf_token,
        }       })
	 console.log('test')
 	const data = await response.json()
 	console.log(data)
    window.open(data.dropboxUrl, '_blank');
}*/

//applique un event listener sur le status du devis => sauvegarde automatique
let selectorStatus = document.getElementById('status')
let selectorResponsable = document.getElementById('responsable')

selectorStatus.addEventListener('change', () =>{
	afficherModifyFormulaire(null,null, 'devis')
})
selectorResponsable.addEventListener('change', () =>{
	afficherModifyFormulaire(null,null, 'devis')
})

let date = document.getElementById('date');
let dateISO = date.innerText;
let dateObj = new Date(dateISO);
let formattedDate = dateObj.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' });
date.innerText=formattedDate

const sendEmail=()=>{
	let tableDevis=document.getElementById('tableDevis')
	console.log(tableDevis.innerHTML)
}