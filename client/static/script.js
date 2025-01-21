function addFilmInput() {
    const filmInputs = document.getElementById("filmInputs");
    const newBlock = document.createElement("div");
    newBlock.className = "film-select-block";

    const input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Введите фильм";
    input.className = "styled-input";

    const button = document.createElement("button");
    button.className = "styled-button remove";
    button.textContent = "-";
    button.onclick = function () {
        removeSpecificBlock(button);
    };

    newBlock.appendChild(input);
    newBlock.appendChild(button);
    filmInputs.appendChild(newBlock);
}


function removeSpecificBlock(button) {
    const block = button.parentElement;
    block.remove();
}


function removeFilmInput() {
    const filmInputs = document.getElementById("filmInputs");
    const lastBlock = filmInputs.lastElementChild;
    if (lastBlock) {
        filmInputs.removeChild(lastBlock);
    } else {
        alert("Нет блоков для удаления!");
    }
}


function showLoader() {
    const loader = document.getElementById("loader");
    const result = document.getElementById("result");
    result.style.display = "none";
    loader.style.visibility = "visible";
    loader.style.opacity = "1";
}

function hideLoader() {
    const loader = document.getElementById("loader");
    loader.style.visibility = "hidden";
    loader.style.opacity = "0";
}


async function searchMovies() {
    const filmInputs = document.querySelectorAll("#filmInputs .styled-input");
    const selectedMovies = Array.from(filmInputs).map(input => input.value.trim()).filter(Boolean);

    if (selectedMovies.length === 0) {
        alert("Выберите хотя бы один фильм!");
        return;
    }

    try {
        showLoader();

        const response = await fetch("/api/get-movie", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ movies: selectedMovies })
        });

        if (!response.ok) throw new Error("Ошибка на сервере");

        const data = await response.json();
        updateResult(data);
    } catch (error) {
        console.error("Ошибка:", error);
        alert("Не удалось найти фильмы. Попробуйте ещё раз.");
    } finally {
        hideLoader();
    }
}


function updateResult(data) {
    document.getElementById("moviePoster").src = data.poster || "poster-placeholder.png";
    document.getElementById("movieTitle").textContent = data.title || "Название фильма";
    document.getElementById("movieYear").innerHTML = `<span class="title">Год выпуска:</span> ${data.year || "Неизвестно"}`;
    document.getElementById("movieAge").innerHTML = `<span class="title">Возрастное ограничение:</span> ${data.age_restriction || "Неизвестно"}`;
    document.getElementById("movieCountry").innerHTML = `<span class="title">Страна:</span> ${data.country || "Неизвестно"}`;
    document.getElementById("movieDirector").innerHTML = `<span class="title">Режиссёр:</span> ${data.director || "Неизвестно"}`;
    document.getElementById("movieActors").innerHTML = `<span class="title">Актёры:</span> ${data.actors || "Неизвестно"}`;
    document.getElementById("movieGenres").innerHTML = `<span class="title">Жанры:</span> ${data.genres || "Нет информации"}`;
    document.getElementById("movieRating").innerHTML = `<span class="title">Рейтинг IMDb:</span> ${data.imdb_rating || "Нет информации"}`;
    document.getElementById("movieDescription").innerHTML = `<span class="title">Описание:</span> ${data.description || "Нет информации"}`;
    document.getElementById("movieReason").innerHTML = `<span class="title">Почему этот фильм подходит:</span> ${data.reason || "Нет информации"}`;
    document.getElementById("similarMovies").innerHTML = `<span class="title">Так же советуем посмотреть:</span> ${data.similar || "Нет информации"}`;

    document.getElementById("result").style.display = "block";
}


function showInput(input) {
    console.log("Input field focused:", input);
}

document.addEventListener('click', function(event) {
  // Проверяем, что клик был вне текстового поля
  if (!event.target.closest('input')) {
    document.activeElement.blur(); // Снимаем фокус с текстового поля
  }
});

window.addEventListener('resize', () => {
  document.body.style.height = `${window.innerHeight}px`;
});
