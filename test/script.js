const div = document.querySelector('.target');

async function fetchData() {
    const res = await fetch("http://127.0.0.1:5000/auth/login", {
        method:"POST",
        headers: {'content-type':'application/json'},
        body: JSON.stringify({ username:"test" ,password: "test"})
        
    });

    if (res.ok) {
        const data = await res.json();
        console.log(data);
        div.innerHTML = data;
    }
    else {
        console.log("some error occured");
    }
}