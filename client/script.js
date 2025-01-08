// Пример фильмов
const movies = ["Начало", "Интерстеллар", "Темный рыцарь", "Криминальное чтиво", "Матрица"];

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
                input.value = movie
