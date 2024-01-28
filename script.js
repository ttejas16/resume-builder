const div = document.querySelector('.target');

async function fetchData(){
    const res = await fetch("http://127.0.0.1:5000/resume/learn/information-on-movie");

    if (res.ok) {
        const data = await res.json();
        console.log(data);
        div.innerHTML = data;
    }
    else{
        console.log("some error occured");
    }
}