const resume_images = document.querySelectorAll(".resume-image");
const mainForm = document.querySelector(".main-form");
const formSections = document.querySelectorAll(".form-section");

const addSocialLinkButton = document.querySelector(".add-more-social");
const personalInformationForm = document.querySelector(".personal-information");

const addMoreEducationButton = document.querySelector(".add-more-education");

if (resume_images.length != 0) {
    resume_images.forEach(node => {
        node.addEventListener('click',(e) => {
            // add selection to form
            // code ...

            const targetResume = e.currentTarget;
            const previousSelected = document.querySelector(".selected-resume");

            if (targetResume != previousSelected) {
                previousSelected?.classList.remove("selected-resume");
            }

            if (!targetResume.classList.contains('selected-resume')) {
                targetResume.classList.add('selected-resume');
            }
        })
    })
}


mainForm.onscroll = (e)=>{
    
    formSections.forEach((section,index) => {
        let scrollPosition = mainForm.scrollTop;
        // console.log(mainFormDiv.scrollBy);
        let sectionTopOffset = section.offsetTop - 50;
        let sectionHeight = section.offsetHeight;
        
        // console.log(sectionTopOffset,sectionHeight);
        if (scrollPosition >= sectionTopOffset && scrollPosition < (sectionTopOffset + Math.floor(sectionHeight/2))) {
            const activeBox = document.querySelector(".active-box");
            const newActiveBox = document.querySelector(`#checkbox-${index + 1}`);

            activeBox?.classList.remove("active-box");
            newActiveBox?.classList.add("active-box");

        }
    })
}


//  ------------- Adding more social links
function createSocialItem() {
    const containerDiv = document.createElement("div");
    containerDiv.classList.add("personal-socials", "span-3");

    const linkInput = document.createElement("input");
    linkInput.type = "text";
    linkInput.classList.add("form-field", "span-2");
    linkInput.placeholder = "Enter Social Link";
    linkInput.required = true;

    const socialIconsDiv = document.createElement("div");
    socialIconsDiv.classList.add("social-icons-div");

    const icons = [
        { name :"bxl-linkedin", value: "linkedin" },
        { name :"bxl-twitter", value: "twitter" },
        { name :"bxl-github", value: "github" },
        { name :"bx-globe", value: "globe" },
    ]

    icons.forEach((icon) => {
        const iconWrapper = document.createElement("div");
        iconWrapper.classList.add("icon-input");

        const iconInput = document.createElement("input");
        iconInput.type = "radio";
        iconInput.name = "social";
        iconInput.value = icon.value;

        const iconDiv = document.createElement("div");
        iconDiv.classList.add("icon-svg") ;

        const i = document.createElement("i");
        i.classList.add("bx",icon.name);
        
        iconDiv.appendChild(i);

        iconWrapper.append(iconInput,iconDiv);
        
        // console.log(iconWrapper);
        socialIconsDiv.appendChild(iconWrapper);
    })

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.classList.add("btn","delete-social","destructive");
    deleteButton.onclick = (e) => {
        e.preventDefault();
        e.currentTarget.parentElement.parentElement.remove();
    }

    const i = document.createElement("i");
    i.classList.add("bx","bx-trash");
    deleteButton.appendChild(i);

    socialIconsDiv.appendChild(deleteButton);

    containerDiv.append(linkInput,socialIconsDiv);
    addSocialLinkButton.before(containerDiv);

}

// delete education handler
function deleteEducation(e){
    e.preventDefault();
    e.currentTarget.parentElement.parentElement.parentElement.remove();
}

// -------------- Adding more education fields
function createEducationItems(){
    
    const containerDiv = document.createElement("div");
    containerDiv.classList.add("education-inputs","flex","flex-column");

    const first = document.createElement("div");
    first.classList.add("grid","grid-cols-3");
    const firstInputs = [
        { name:'degree-name', type:'text', placeholder:'Degree Name'},
        { name:'institute-name', type:'text', placeholder:'University or Institute Name'},
        { name:'graduation-year', type:'number', placeholder:'Graduation Year'},
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
    second.classList.add("grid","grid-cols-4");
    const secondInputs = [
        { name:'gpa', type:'number', placeholder:'Enter GPA'},
        { name:'state', type:'text', placeholder:'State'},
        { name:'city', type:'text', placeholder:'City'},
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

    const deleteEducationButton = document.createElement("button");
    deleteEducationButton.type = "button";
    deleteEducationButton.classList.add("btn","delete-education","destructive");
    deleteEducationButton.onclick = deleteEducation;

    const i = document.createElement("i");
    i.classList.add("bx","bx-trash");
    deleteEducationButton.appendChild(i);

    deleteEducationDiv.appendChild(deleteEducationButton);
    second.appendChild(deleteEducationDiv);

    containerDiv.append(first,second);
    addMoreEducationButton.before(containerDiv);
}



addMoreEducationButton.addEventListener("click",(e) => {
    e.preventDefault();
    createEducationItems();
})
addSocialLinkButton.addEventListener("click",(e) => {
    e.preventDefault();
    createSocialItem();
})