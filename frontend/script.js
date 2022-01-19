import { drugInfo } from "./drug_info.js"

//selecting all required elements
const dragArea = document.querySelector(".drag-area");
const dragText = dragArea.querySelector("header");
const browseButton = dragArea.querySelector("button");
const input = dragArea.querySelector("input");

const dragAreaActiveContainer = document.querySelector(".drag-area-active-container");
const imageContainer = document.querySelector(".drag-area-image-container");
const imageElement = document.querySelector(".drag-area-image");

const clearButton = document.querySelector(".clear-button");

const classificationResultContainer = document.querySelector(".classification-result-container");

const pillLabel = document.querySelector(".classification-pill-label");
const pillGroup = document.querySelector(".classification-pill-group");
const pillIngredients = document.querySelector(".classification-pill-ingredients");
const pillUsage = document.querySelector(".classification-pill-usage");
const pillRegistrationNumber = document.querySelector(".classification-pill-registration-number");


let file; //this is a global variable and we'll use it inside multiple functions

browseButton.onclick = () => {
    input.click(); //if user click on the button then the input also clicked
}

input.addEventListener("change", function() {
    //getting user select file and [0] this means if user select multiple files then we'll select only the first one
    file = this.files[0];
    dragArea.classList.add("active");
    showFile(); //calling function
});


//If user Drag File Over DropArea
dragArea.addEventListener("dragover", (event) => {
    event.preventDefault(); //preventing from default behaviour
    dragArea.classList.add("active");
    dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dragArea.addEventListener("dragleave", () => {
    dragArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dragArea.addEventListener("drop", (event) => {
    event.preventDefault(); //preventing from default behaviour
    //getting user select file and [0] this means if user select multiple files then we'll select only the first one
    file = event.dataTransfer.files[0];
    showFile(); //calling function
});

clearButton.onclick = () => {
    clearFile();
}

function showFile() {
    classificationResultContainer.classList.add("hidden");

    let fileType = file.type; //getting selected file type
    let validExtensions = ["image/jpeg", "image/jpg", "image/png"]; //adding some valid image extensions in array
    if (validExtensions.includes(fileType)) { //if user selected file is an image file
        let fileReader = new FileReader(); //creating new FileReader object
        fileReader.onload = () => {
            let fileURL = fileReader.result; //passing user file source in fileURL variable

            imageElement.setAttribute("src", fileURL);

            dragAreaActiveContainer.classList.add("hidden");
            imageContainer.classList.remove("hidden");

            classifyImage(fileURL);
        }
        fileReader.readAsDataURL(file);
    } else {
        alert("This is not an Image File!");
        dragArea.classList.remove("active");
        dragText.textContent = "Drag & Drop to Upload File";
    }
}

function clearFile() {
    input.value = "";
    dragArea.classList.remove("active");

    dragAreaActiveContainer.classList.remove("hidden");
    imageContainer.classList.add("hidden");

    classificationResultContainer.classList.add("hidden");
}

async function classifyImage(base64EncodedImageURL) {
    const url = "http://localhost:8280/predictions/pill_model";

    const formData = new FormData();
    formData.append("body", JSON.stringify({
        "image": base64EncodedImageURL.split(",")[1]
    }));

    console.log(formData.toString());

    const response = await fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        body: formData
    });

    const result = await response.json();
    pillLabel.innerText = result.pill_label;

    const randomPillInfoIndex = Math.floor(Math.random() * drugInfo.length);
    const randomPillInfo = drugInfo[randomPillInfoIndex];

    pillGroup.innerText = randomPillInfo["group"];
    pillIngredients.innerText = randomPillInfo["ingredients"];
    pillUsage.innerText = randomPillInfo["usage"];
    pillRegistrationNumber.innerText = randomPillInfo["registration-number"];

    classificationResultContainer.classList.remove("hidden");
}