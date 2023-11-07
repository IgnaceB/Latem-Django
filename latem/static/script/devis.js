
const getAttribute=()=>{
	let descriptionContainer = document.getElementById('elemDescription')
	let selector = document.getElementById('listElem')
	selector.addEventListener("change",event=>{
		selectedOption=selector.options[selector.options.selectedIndex]
		descriptionContainer.innerText=selectedOption.getAttribute("description")
	})

}				

getAttribute()
const displayNextList=()=>{
let description = JSON.parse(document.currentScript.previousElementSibling.textContent
					)

				for (let i=1; i<description.length; i++) {

    // Obtenir une référence aux éléments de sélection
					let previousListSelect = document.getElementById(`listCharac${i-1}`);
					let listCharacSelect = document.getElementById(`listCharac${i}`);

    // Écouter les changements de sélection dans le premier menu déroulant
					previousListSelect.addEventListener("change", function () {
						let selectedElem = previousListSelect.options[previousListSelect.selectedIndex];
						let selectedElemDescription = selectedElem.getAttribute("id");

        // Nettoyer le deuxième menu déroulant
						listCharacSelect.innerHTML = "";

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
									listCharacSelect.appendChild(option);}

								}
								else if(selectedElemDescription == element.parent_item) {

									let option = document.createElement("option");
									option.value = element.name;
									option.text = element.name;
									option.setAttribute('id', element.id)
									option.setAttribute('description', element.description)
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
let finitions = JSON.parse(document.currentScript.nextElementSibling.textContent
					)
    // Obtenir une référence aux éléments de sélection
					let listItemSelect = document.getElementById(`listFinit`);
					let listFinitSelect = document.getElementById(`listFinit1`);

    // Écouter les changements de sélection dans le premier menu déroulant
					listItemSelect.addEventListener("change", function () {
						let selectedElem = listItemSelect.options[listItemSelect.selectedIndex];
						let selectedElemDescription = selectedElem.getAttribute("id");

        // Nettoyer le deuxième menu déroulant
						listFinitSelect.innerHTML = "";

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
}
displayNextListFinit()
