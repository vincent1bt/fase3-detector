document.addEventListener("DOMContentLoaded", ready);

function get_prediction(image) {
    const formData = new FormData()
    formData.append('image', image);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => {
        response.json().then(data => {
            const bytesImage = data["final_image"];
            const finalImage = bytesImage.split('\'')[1];
            
            const segmentation_image = document.querySelector("#segmentation_image");
            segmentation_image.setAttribute('src', 'data:image/jpeg;base64,' + finalImage); 
        });
    })
    .catch(error => {
        console.log("Hubo un error :c");
    });
}

function imageUploaded(event) {
    const target = event.target;
    const image = target.files[0];

    if (!image) return;
    
    const original_image = document.querySelector("#original_image");
    original_image.src = window.URL.createObjectURL(image);

    get_prediction(image);
}

function ready() {
    const inputFile = document.querySelector("#image");
    inputFile.addEventListener('change', imageUploaded);
}