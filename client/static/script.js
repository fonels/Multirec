// Пример фильмов
const movies = [
    "Начало", "Интерстеллар", "Тёмный рыцарь", "Криминальное чтиво", "Матрица"
];

// Поиск и фильтрация списка фильмов
function filterMovies(input) {
    const query = input.value.toLowerCase();
    const dropdown = input.nextElementSibling;
    dropdown.innerHTML = '';
    movies.forEach(movie => {
        if (movie.toLowerCase().includes(query)) {
            const option = document.createElement('div');
            option.textContent = movie;
            option.onclick = () => {
                input.value = movie;
                dropdown.style.display = 'none';
            };
            dropdown.appendChild(option);
        }
    });
    dropdown.style.display = query ? 'block' : 'none';
}

// Добавить новое поле для ввода фильма
function addFilmInput() {
    const filmInputs = document.getElementById("filmInputs");
    const newBlock = document.createElement("div");
    newBlock.className = "film-select-block";
    newBlock.innerHTML = `
        <input type="text" oninput="filterMovies(this)" placeholder="Выберите фильм" onfocus="showInput(this)">
        <div class="film-dropdown"></div>
    `;
    filmInputs.appendChild(newBlock);
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
        const response = await fetch("http://127.0.0.1:5000/api/get-movie", {
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
    document.getElementById("movieRating").textContent = "Рейтинг IMDb: " + (data.rating || "Нет информации");
    document.getElementById("movieDescription").textContent = "Описание: " + (data.description || "Нет информации");
    document.getElementById("movieReason").textContent = "Почему этот фильм подходит: " + (data.reason || "Нет информации");

    const similarMoviesDiv = document.getElementById("similarMovies");
    similarMoviesDiv.innerHTML = "";
    (data.similarMovies || []).forEach(movie => {
        const movieDiv = document.createElement("div");
        movieDiv.textContent = movie;
        similarMoviesDiv.appendChild(movieDiv);
    });

    document.getElementById("result").style.display = "block";
}

function showInput(input) {
    console.log("Input field focused:", input);
}
