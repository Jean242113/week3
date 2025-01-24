// Select elements
const burgerMenuIcon = document.getElementById('burgerMenuIcon');
const popupMenu = document.getElementById('popupMenu');
const closeIcon = document.getElementById('closeIcon');

// Show popup menu when burger icon is clicked
burgerMenuIcon.addEventListener('click', () => {
    popupMenu.classList.remove('hidden');
});

// Hide popup menu when close icon is clicked
closeIcon.addEventListener('click', () => {
    popupMenu.classList.add('hidden');
});
let index = 0;
const createData = function () {
    const baseUrl = "https://";
    const apiUrl = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1";

    fetch(apiUrl)
        .then((response) => response.json())
        .then((data) => {
            const spots = data.data.results;
            const smallBoxContainer = document.getElementsByClassName("small-box-container")[0];
            const bigBoxContainer = document.getElementsByClassName("big-box-container")[0];

            for (let i = index; i < index + 3; i++) {
                const spot = spots[i];
                const smallBox = document.createElement("div");
                smallBox.classList.add("small-box");

                const imageUrl = baseUrl + spot.filelist.split("https://")[1];
                const image = document.createElement("img");
                image.src = imageUrl;
                image.alt = spot.stitle;

                const title = document.createElement("span");
                title.textContent = spot.stitle;
                title.className = "text-block";

                smallBox.appendChild(image);
                smallBox.appendChild(title);
                smallBoxContainer.appendChild(smallBox);
            }
            index += 3;
            createBigBox();
        });
};

const createBigBox = function () {
    const baseUrl = "https://";
    const apiUrl = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1";

    fetch(apiUrl)
        .then((response) => response.json())
        .then((data) => {
            const spots = data.data.results;
            const bigBoxContainer = document.getElementsByClassName("big-box-container")[0];

            for (let i = index; i < index + 10; i++) {
                if (i == spots.length) {
                    index = spots.length;
                    return;
                }
                const spot = spots[i];
                const bigBox = document.createElement("div");
                bigBox.classList.add("big-box");

                const imageUrl = baseUrl + spot.filelist.split("https://")[1];
                bigBox.style.backgroundImage = `url('${imageUrl}')`;

                const star = document.createElement("div");
                star.classList.add("star");

                const textBlock = document.createElement("div");
                textBlock.classList.add("text-block");
                textBlock.textContent = spot.stitle;

                bigBox.appendChild(star);
                bigBox.appendChild(textBlock);
                bigBoxContainer.appendChild(bigBox);
            }
            index += 10;
        })
        .catch((error) => {
            console.error("抓取資料時發生錯誤: ", error);
        });
};

document.addEventListener("DOMContentLoaded", createData());
