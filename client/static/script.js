// Добавить новое поле для ввода фильма
function addFilmInput() {
    const filmInputs = document.getElementById("filmInputs");
    const newBlock = document.createElement("div");
    newBlock.className = "film-select-block";
    newBlock.innerHTML = `
        <input type="text" oninput="filterMovies(this)" placeholder="Введите фильм" onfocus="showInput(this)">
        <div class="film-dropdown"></div>
        <button class="film-select-block button" onclick="removeSpecificBlock(this)">-</button>
    `;
    filmInputs.appendChild(newBlock);
}

function removeSpecificBlock(button) {
    const block = button.parentElement;
    block.remove();
}

// Удалить последнее поле для ввода фильма
function removeFilmInput() {
    const filmInputs = document.getElementById("filmInputs");
    // Находим последний блок с классом "film-select-block"
    const lastBlock = filmInputs.querySelector(".film-select-block:last-child");

    // Если блок существует, удаляем его
    if (lastBlock) {
        filmInputs.removeChild(lastBlock);
    } else {
        console.warn("Нет блоков для удаления.");
    }
}

// Отправить запрос к серверу
async function searchMovies() {
    const filmInputs = document.querySelectorAll("#filmInputs input");
    const selectedMovies = Array.from(filmInputs).map(input => input.value).filter(Boolean);

    if (selectedMovies.length === 0) {
        alert("Выберите хотя бы один фильм!");
        return;
    }

    try {
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
    }
}

function updateResult(data) {
    document.getElementById("moviePoster").src = data.poster || "poster-placeholder.png";
    document.getElementById("movieTitle").textContent = data.title || "Название фильма";
    document.getElementById("movieYear").textContent = "Год выпуска: " + (data.year || "Неизвестно");
    document.getElementById("movieAge").textContent = "Возрастное ограничение: " + (data.age_restriction || "Неизвестно");
    document.getElementById("movieCountry").textContent = "Страна: " + (data.country || "Неизвестно");
    document.getElementById("movieDirector").textContent = "Режиссёр: " + (data.director || "Неизвестно");
    document.getElementById("movieActors").textContent = "Актёры: " + (data.actors || "Неизвестно");
    document.getElementById("movieGenres").textContent = "Жанры: " + (data.genres || "Нет информации");
    document.getElementById("movieRating").textContent = "Рейтинг IMDb: " + (data.imdb_rating || "Нет информации");
    document.getElementById("movieDescription").textContent = "Описание: " + (data.description || "Нет информации");
    document.getElementById("movieReason").textContent = "Почему этот фильм подходит: " + (data.reason || "Нет информации");
    document.getElementById("similarMovies").textContent = "Так же советуем посмотреть: " + (data.similar);
    }

    document.getElementById("result").style.display = "block";

function showInput(input) {
    console.log("Input field focused:", input);
}