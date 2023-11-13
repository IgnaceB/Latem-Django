let description = JSON.parse(document.currentScript.previousElementSibling.textContent)
let finitions = JSON.parse(document.currentScript.nextElementSibling.textContent)


//renvoie la description de l'element selctionné
const getAttribute=(container,selection)=>{
	let descriptionContainer = document.getElementById(container)
	let selector = document.getElementById(selection)
	selector.addEventListener("change",event=>{
		selectedOption=selector.options[selector.options.selectedIndex]
		descriptionContainer.innerText=`Description : ${selectedOption.getAttribute("description")}`
	})

}	

getAttribute('elemDescription','listElem')	


// update the hidden fiels in the forms Charac, before submission
const updateFieldsCharac=()=>{
	let parent_description={}
	let inputParentDescription = document.getElementById('id_parent_description')
	let inputParentItem = document.getElementById('id_parent_item')
	let inputLevel = document.getElementById('id_level')
	let inputDescriptionType = document.getElementById('id_description_type')

	let item=document.getElementById('listCharac0')
	let selectedItem=item.options[item.selectedIndex]

	inputDescriptionType.value='charac'
	inputLevel.value=1
	inputParentItem.value=selectedItem.getAttribute('id')
	inputParentDescription.value=''
	let parent={}
	for (let i=1; i<description.length+1; i++) {


		let selectList = document.getElementById(`listCharac${i}`)

		if (selectList.value !== '') {

			let selectedOption = selectList.options[selectList.selectedIndex]

				parent = {
			  'parent_description': selectedOption.getAttribute('id'),
			  'level': i + 1
			};
		}
		else {
			continue
		}

	inputLevel.value=parent.level
	inputParentDescription.value=parent.parent_description
}
}	


const updateFieldsFinit=()=>{

	/*Utilisation de selcteur CSS obligatoire : les deux forms appelé ont les meme ID si autre que css => seulement le form
	charac sera rempli*/
	let finitSection= document.querySelector('#finitions')

	let inputParentDescription = finitSection.querySelector('#id_parent_description')
	let inputParentItem = finitSection.querySelector('#id_parent_item')
	let inputLevel = finitSection.querySelector('#id_level')
	let inputDescriptionType = finitSection.querySelector('#id_description_type')

	let item=document.getElementById('listFinit')
	let selectedItem=item.options[item.selectedIndex]

	inputDescriptionType.value='finitions'
	inputLevel.value=1
	inputParentItem.value=selectedItem.getAttribute('id')
	inputParentDescription.value=''
	inputLevel.value=1

}	

let submitCharac = document.getElementById('submitCharac')
submitCharac.addEventListener('click',updateFieldsCharac)


let submitFinit = document.getElementById('submitFinit')
submitFinit.addEventListener('click',updateFieldsFinit)

const displayNextList=()=>{
/*let description = JSON.parse(document.currentScript.previousElementSibling.textContent
					)*/

				for (let i=1; i<description.length; i++) {

    // Obtenir une référence aux éléments de sélection
					let previousListSelect = document.getElementById(`listCharac${i-1}`);
					let listCharacSelect = document.getElementById(`listCharac${i}`);

    // Écouter les changements de sélection dans le premier menu déroulant
					previousListSelect.addEventListener("change", function () {
						let selectedElem = previousListSelect.options[previousListSelect.selectedIndex];
						let selectedElemDescription = selectedElem.getAttribute("id");
						//update description
						let descriptionContainer = document.getElementById('characDescription')
						descriptionContainer.innerText=`Description : ${selectedElem.getAttribute('description')}`
        // Nettoyer le deuxième menu déroulant
						listCharacSelect.innerHTML = "";

						      let emptyOption = document.createElement("option");
						      emptyOption.value = '';
						      emptyOption.text = ''; // Vous pouvez également définir un texte par défaut si nécessaire.
						      listCharacSelect.appendChild(emptyOption);
											        // Remplir le deuxième menu déroulant avec les caractéristiques correspondantes
						description[i].forEach(element=>{
							
							if (i>1){
								if (selectedElemDescription == element.parent_description) {
									let option = document.createElement("option");
									option.value = element.name;
									option.text = element.name;
									option.setAttribute('id', element.id)
									option.setAttribute('description', element.description)
									option.setAttribute('parent_description', element.parent_description)
									option.setAttribute('parent_item', element.parent_item)
									listCharacSelect.appendChild(option);}

								}
								else if(selectedElemDescription == element.parent_item) {

									let option = document.createElement("option");
									option.value = element.name;
									option.text = element.name;
									option.setAttribute('id', element.id)
									option.setAttribute('description', element.description)
									option.setAttribute('parent_item', element.parent_item)
									option.setAttribute('parent_description', element.parent_description)
									listCharacSelect.appendChild(option);}
							})
						for (let j=1; j<description.length+1;j++){
							if (j<=i){
								let listsToShow=document.getElementById(`listCharac${j}`)
								listsToShow.style.visibility='visible'
							}
							else {
								let listsToHide=document.getElementById(`listCharac${j}`)
								listsToHide.style.visibility='hidden'
								listsToHide.value=''
							}
						}
					})

				};

}

displayNextList()


displayNextListFinit=()=>{
/*let finitions = JSON.parse(document.currentScript.nextElementSibling.textContent
					)*/
    // Obtenir une référence aux éléments de sélection
					let listItemSelect = document.getElementById(`listFinit`);
					let listFinitSelect = document.getElementById(`listFinit1`);

    // Écouter les changements de sélection dans le premier menu déroulant
					listItemSelect.addEventListener("change", function () {
						let selectedElem = listItemSelect.options[listItemSelect.selectedIndex];
						let selectedElemDescription = selectedElem.getAttribute("id");

					//update description
						let descriptionContainer = document.getElementById('finitionDescription')
						descriptionContainer.innerText=`Description : ${selectedElem.getAttribute('description')}`
        // Nettoyer le deuxième menu déroulant
						listFinitSelect.innerHTML = "";

						let emptyOption = document.createElement("option");
						      emptyOption.value = '';
						      emptyOption.text = ''; // Vous pouvez également définir un texte par défaut si nécessaire.
						      listFinitSelect.appendChild(emptyOption);
        // Remplir le deuxième menu déroulant avec les caractéristiques correspondantes
						finitions.forEach(element=>{
				
								if(selectedElemDescription == element.parent_item) {

									let option = document.createElement("option");
									option.value = element.name;
									option.text = element.name;
									option.setAttribute('id', element.id)
									option.setAttribute('description', element.description)
									option.setAttribute('parent_description', element.parent_description)
									
									listFinitSelect.appendChild(option);}


								})
			
})
					listFinitSelect.addEventListener('change',event=>{
						let selectedElem = listFinitSelect.options[listFinitSelect.selectedIndex];
						let descriptionContainer = document.getElementById('finitionDescription')
						descriptionContainer.innerText=`Description : ${selectedElem.getAttribute('description')}`
					})
}
displayNextListFinit()


// Fonction de suppression d'un item
const deleteItem=()=>{
		let selector = document.getElementById('listElem')
		item=selector.options[selector.options.selectedIndex]
		console.log(item)
		let section= document.querySelector('#object')

		let inputId = section.querySelector('#id_id')
		inputId.value=item.getAttribute('id')

}

//Fonction de suppression d'une charactéristique (charac ou finit)
const deleteCharac=()=>{
		let selectedDescription={}
	for (let i=1; i<description.length+1; i++) {


		let selectList = document.getElementById(`listCharac${i}`)

		if (selectList.value !== '') {

			let selectedOption = selectList.options[selectList.selectedIndex]

				selectedDescription = {
			  'id': selectedOption.getAttribute('id'),
			  
			};
		}
		else {
			continue
		}
	}

		let section= document.querySelector('#charac')


		let inputId = section.querySelector('#id_id')

		inputId.value=selectedDescription.id

}

const deleteFinit=()=>{

		let selectList = document.getElementById(`listFinit1`)


			let selectedOption = selectList.options[selectList.selectedIndex]

				selectedDescription = {
			  'id': selectedOption.getAttribute('id'),
			  
			};

		let section= document.querySelector('#finitions')


		let inputId = section.querySelector('#id_id')
		console.log(inputId)
		console.log(section)
		inputId.value=selectedDescription.id

}

//ajoute l'évenement de suppression sur le forms Item
let submitDeleteItem = document.getElementById('submitItemSuppression')
submitDeleteItem.addEventListener('click', deleteItem)


// ajoute l'evenement de suppression sur le forms Charac
let submitDeleteCharac = document.getElementById('submitCharacSuppression')
submitDeleteCharac.addEventListener('click', deleteCharac)

let submitDeleteFinit = document.getElementById('submitFinitSuppression')
submitDeleteFinit.addEventListener('click', deleteFinit)

// demande la validation de l'utilisateur
const confirmationAlert=(event)=>{
	   let confirmation = confirm("Êtes-vous sûr de vouloir supprimer cet élément ?");
        
        // Si l'utilisateur annule la confirmation, annuler la soumission du formulaire
        if (!confirmation) {
            event.preventDefault();
        }
}


//applique la fonction sur les 3 forms
document.getElementById('deleteItem').addEventListener('submit', confirmationAlert)

document.getElementById('deleteDescription').addEventListener('submit', confirmationAlert)

document.getElementById('deleteFinition').addEventListener('submit', confirmationAlert)