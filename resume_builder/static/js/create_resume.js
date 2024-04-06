const resume_images = document.querySelectorAll(".resume-image");
const mainForm = document.querySelector(".main-form");
const formSections = document.querySelectorAll(".form-section");

const addMoreEducationButton = document.querySelector(".add-more-education");
const addMoreProjectButton = document.querySelector(".add-more-project");
const addMoreExperienceButton = document.querySelector(".add-more-experience");
const addMoreSkillButton = document.querySelector(".add-more-skill");

if (resume_images.length != 0) {
    resume_images.forEach((node,index) => {
        node.addEventListener('click', (e) => {
  
            const targetResume = e.currentTarget;
            const previousSelected = document.querySelector(".selected-resume");

            

            if (targetResume != previousSelected) {
                previousSelected?.classList.remove("selected-resume");
            }

            if (!targetResume.classList.contains('selected-resume')) {
                targetResume.classList.add('selected-resume');
            }

            const resumeChoice = document.querySelector("#resume-choice");
            resumeChoice.value = index + 1;
        })
    })
}


mainForm.onscroll = (e) => {

    formSections.forEach((section, index) => {
        let scrollPosition = mainForm.scrollTop;
        // console.log(mainFormDiv.scrollBy);
        let sectionTopOffset = section.offsetTop - 50;
        let sectionHeight = section.offsetHeight;

        // console.log(sectionTopOffset,sectionHeight);
        if (scrollPosition >= sectionTopOffset && scrollPosition < (sectionTopOffset + Math.floor(sectionHeight / 2))) {
            const activeBox = document.querySelector(".active-box");
            const newActiveBox = document.querySelector(`#checkbox-${index + 1}`);

            activeBox?.classList.remove("active-box");
            newActiveBox?.classList.add("active-box");

        }
    })
}


// delete education handler
function deleteEducation(e) {
    e.preventDefault();
    e.currentTarget.parentElement.parentElement.parentElement.remove();
}

// -------------- Adding more education fields
function createEducationItems() {

    const containerDiv = document.createElement("div");
    containerDiv.classList.add("education-inputs", "flex", "flex-column");

    const first = document.createElement("div");
    first.classList.add("grid", "grid-cols-3");
    const firstInputs = [
        { name: 'education-degree-name', type: 'text', placeholder: 'Degree Name' },
        { name: 'education-institute-name', type: 'text', placeholder: 'University or Institute Name' },
        { name: 'education-graduation-year', type: 'number', placeholder: 'Graduation Year' },
    ];

    firstInputs.forEach(input => {
        const newInput = document.createElement('input');;
        newInput.required = true;
        newInput.type = input.type;
        newInput.name = input.name;
        newInput.placeholder = input.placeholder;
        newInput.classList.add("form-field");
        first.appendChild(newInput);
    })

    const second = document.createElement("div");
    second.classList.add("grid", "grid-cols-4");
    const secondInputs = [
        { name: 'education-gpa', type: 'number', placeholder: 'Enter GPA/Percentage' },
        { name: 'education-state', type: 'text', placeholder: 'State' },
        { name: 'education-city', type: 'text', placeholder: 'City' },
    ];

    secondInputs.forEach(input => {
        const newInput = document.createElement('input');;
        newInput.required = true;
        newInput.type = input.type;
        newInput.name = input.name;
        newInput.placeholder = input.placeholder;
        newInput.classList.add("form-field");
        second.appendChild(newInput);
    })

    const deleteEducationDiv = document.createElement("div");
    deleteEducationDiv.classList.add("flex");

    const deleteBtn = createDeleteButton(deleteEducation);

    deleteEducationDiv.appendChild(deleteBtn);
    second.appendChild(deleteEducationDiv);

    containerDiv.append(first, second);
    addMoreEducationButton.before(containerDiv);
}


function deleteProject(e) {
    e.preventDefault();
    e.currentTarget.parentElement.parentElement.parentElement.remove();
}

function addMoreProject() {
    const containerDiv = document.createElement("div");
    containerDiv.classList.add("project-inputs", "flex", "flex-column");

    const first = document.createElement("div");
    first.classList.add("grid", "grid-cols-2");

    const firstInputs = [
        { name: 'project-title', type: 'text', placeholder: 'Project Title', required: true },
        { name: 'project-tech', type: 'text', placeholder: 'Tools Used (Optional)' }
    ];
    firstInputs.forEach(input => {
        const newInput = document.createElement('input');;
        newInput.required = input.required ? true : false;
        newInput.type = input.type;
        newInput.name = input.name;
        newInput.placeholder = input.placeholder;
        newInput.classList.add("form-field");
        first.appendChild(newInput);
    })

    const second = document.createElement("div");
    second.classList.add("grid", "grid-cols-2");

    const secondInputs = [
        { name: 'project-github-link', type: 'text', placeholder: 'Github Link (Optional)' },
        { name: 'project-live-link', type: 'text', placeholder: 'Live Link (Optional)' }
    ];
    secondInputs.forEach(input => {
        const newInput = document.createElement('input');;
        // newInput.required = true;
        newInput.type = input.type;
        newInput.name = input.name;
        newInput.placeholder = input.placeholder;
        newInput.classList.add("form-field");
        second.appendChild(newInput);
    })

    const third = document.createElement("div");
    third.classList.add("flex");

    const textArea = document.createElement("textarea");
    textArea.classList.add("textarea-full");
    textArea.required = true;
    textArea.placeholder = "Project Description..."
    textArea.name = "project-description"

    const buttonWrapper = document.createElement("div");
    buttonWrapper.classList.add("project-delete-div");

    const deleteBtn = createDeleteButton(deleteProject);
    buttonWrapper.appendChild(deleteBtn);

    third.append(textArea, buttonWrapper);

    containerDiv.append(first, second, third);

    addMoreProjectButton.before(containerDiv);
}


function createInputs(propertyObjects = []) {
    // { name: 'value', type: 'value', placeholder: 'value', ... },
    const res = propertyObjects.map((propertyObject, index) => {
        const newInput = document.createElement('input');

        for (const key in propertyObject) {

            if (key == "class") {
                newInput.classList.add(...propertyObject[key]);
                continue;
            }

            newInput[key] = propertyObject[key];
        }
        return newInput;
    })

    return res;
}

function createDeleteButton(listener){
    const button = document.createElement("button");
    button.type = "button";
    button.classList.add("btn", "delete", "destructive");
    button.onclick = listener;

    const i = document.createElement("i");
    i.classList.add("bx", "bx-trash");

    button.appendChild(i);

    return button;
}

function deleteExperience(e){
    e.preventDefault();
    e.currentTarget.parentElement.parentElement.parentElement.remove();
}

function addMoreExperience() {
    const containerDiv = document.createElement("div");
    containerDiv.classList.add("experience-inputs", "flex", "flex-column");

    const first = document.createElement("div");
    first.classList.add("grid","grid-cols-3");
    let props = [
        {
            name: "experience-company-name",
            type: "text", 
            placeholder: "Company / Organization name", 
            class: ["form-field"], 
            required: true
        },
        {
            name: "experience-position-name",
            type: "text", 
            placeholder: "Position Title", 
            class: ["form-field"], 
            required: true
        },
        {
            name: "experience-state",
            type: "text", 
            placeholder: "State", 
            class: ["form-field"], 
            required: true
        },
    ];
    let inputs = createInputs(props);
    first.append(...inputs);
    
    const second = document.createElement("div");
    second.classList.add("grid","grid-cols-3");
    props = [
        {
            name: "experience-city",
            type: "text", 
            placeholder: "City", 
            class: ["form-field"], 
            required: true
        },
        {
            name: "experience-start",
            type: "text", 
            placeholder: "Start year", 
            class: ["form-field"], 
            required: true
        },
        {
            name: "experience-end",
            type: "text", 
            placeholder: "End year", 
            class: ["form-field"], 
            required: false
        },
    ];
    inputs = createInputs(props);
    second.append(...inputs);

    const third = document.createElement("div");
    third.classList.add("flex");

    const textArea = document.createElement("textarea");
    textArea.classList.add("textarea-full");
    textArea.required = true;
    textArea.name = "experience-description"
    textArea.placeholder = "Description..."

    const buttonWrapper = document.createElement("div");
    buttonWrapper.classList.add("experience-delete-div");

    const deleteBtn = createDeleteButton(deleteExperience);
    buttonWrapper.appendChild(deleteBtn);

    third.append(textArea, buttonWrapper);

    containerDiv.append(first, second, third);
    console.log(containerDiv);
    addMoreExperienceButton.before(containerDiv);
}

function deleteSkill(e){
    e.preventDefault();
    e.currentTarget.parentElement.parentElement.remove();
}

function addSkill(){
    const skillInputWrapper = document.querySelector(".skill-input-wrapper");
    const containerDiv = document.createElement("div");
    containerDiv.classList.add("skill-inputs","flex");
    let props = [
        { 
            type: "text",
            placeholder: "Enter Skill",
            class: ["form-field"],
            name: "skill",
            required: true,

        }
    ];

    const inputs = createInputs(props);
    const buttonWrapper = document.createElement("div");
    buttonWrapper.classList.add("skill-delete-div");
    buttonWrapper.appendChild(createDeleteButton(deleteSkill));
    
    containerDiv.append(...inputs,buttonWrapper);

    skillInputWrapper.appendChild(containerDiv);

}


addMoreEducationButton.addEventListener("click", (e) => {
    e.preventDefault();
    createEducationItems();
})
addMoreProjectButton.addEventListener("click", (e) => {
    e.preventDefault();
    addMoreProject();
})

addMoreExperienceButton.addEventListener("click", (e) => {
    e.preventDefault();
    addMoreExperience();
})

addMoreSkillButton.addEventListener("click",(e) => {
    e.preventDefault();
    addSkill();
})