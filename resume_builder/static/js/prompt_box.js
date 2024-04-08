const promptChat = document.querySelector('.prompt-chat');
const bulbButton = document.querySelector('.bulb-btn');

const promptSendButton = document.querySelector('.send-prompt');

const promptInput = document.querySelector('.input-prompt');
const promptResponse = document.querySelector('.response-chat');
const loadingIndicator = document.querySelector('.loading-indicator');

bulbButton.addEventListener('click',(e) => {
    
    if (promptChat.classList.contains("animate-in")) {

        promptChat.classList.remove("animate-in");   
        promptChat.classList.add("animate-out");
    }
    else{
        promptChat.classList.add("animate-in");
        promptChat.classList.remove("animate-out");
    }

})

promptSendButton.addEventListener('click',async (e) =>{
    const inputValue = promptInput.value.trim();
    
    if (!inputValue) {
        return;
    }

    try {
        loadingIndicator.style.display = "block";
        const rawResponse = await fetch("/generate-text",{
            method: "POST",
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                searchText: inputValue
            })
        })
        
        const response = await rawResponse.json();
        
        if (promptResponse) {
            promptResponse.value = "";
            promptResponse.value = response;
        }
        
    } catch (err) {
        console.log(err);
    }
    loadingIndicator.style.display = "none";

    
})

