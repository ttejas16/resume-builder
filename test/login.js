const form = document.querySelector('form');





async function handleClick(e){
    // console.log(e);
    e.preventDefault();

    const res = await fetch("http://127.0.0.1:5000/auth/login",{
        method: "POST",
        mode: "cors",
        headers: {
            "Content-type":"application/json"
        },
        body:JSON.stringify({
            email: form.email.value,
            password: form.password.value
        }),
        

    });
    if (!res.ok) {
        // catch logic
        // return;
        const data = await res.json();
    
        console.log(data);
    }
    const data = await res.json();
    console.log(data);
    


}