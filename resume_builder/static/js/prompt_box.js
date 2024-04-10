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
        promptSendButton.disabled = true;

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

        if (promptResponse && response.success) {
            promptResponse.value = "";
            

            let id;
            function typingText(func){
                let index = 0;

                id = setInterval(() => {
                    promptResponse.value = response.data.slice(0, index + 1);
                    index += 1;

                    if (index >= response.data.length) {
                        func();
                    }
                },30);
            }
            typingText(() => {
                promptSendButton.disabled = false;
                clearInterval(id);
            });
          
        }else{
            console.log(response.data);
        }

        
    } catch (err) {
        console.log(err);
        promptSendButton.disabled = false;
    }
    loadingIndicator.style.display = "none";

    
})

