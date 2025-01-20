# Multirec

## Overview

Multirec is a web application that allows users to combine movie information in unique ways to create personalized recommendations tailored to their input. This process leverages both OMDB and OpenAI APIs to provide enriched insights and a seamless user experience. The project consists of a backend implemented with Flask and a frontend built with HTML, CSS, and JavaScript.

## Features

- Fetches movie information using the OMDB API.
- Processes movie data and provides recommendations.
- Responsive web design for desktop and mobile devices.

## Requirements

- Python 3.8+
- Flask
- Internet connection (for OMDB and OpenAI requests)

## Installation

### Step 1: Clone the Repository

```bash
git clone <repository_url>
cd Multirec
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

Create a `.env` file in the root directory with the following content:

```env
OMDB_API_KEY=<your_omdb_api_key>
OPENAI_API_KEY=<your_openai_api_key>
```

### Step 4: Run the Application

```bash
python app.py
```

### Step 5: Access the Application

Open your web browser and go to `http://127.0.0.1:5000/`.

## Project Structure

```
project/
├── server/
│   ├── routes.py          # API Endpoints
│   ├── services/
│   │   ├── omdb_service.py  # Interaction with OMDB API
│   │   ├── movie_info.py    # Movie data processing
│   ├── utils/
│       ├── gpt_request.py   # GPT API interaction
│       ├── config.py        # Environment variable loading
├── client/
│   ├── index.html           # Main HTML file
│   ├── static/
│       ├── favicon.ico      # Favicon
│       ├── images/          # Image assets
│       ├── fonts/           # Font assets
│       ├── script.js        # Frontend logic
│       ├── style.css        # Styling
├── .env                     # Environment variables
├── .gitignore               # Git ignored files
├── README.md                # Project documentation
├── app.py                   # Flask server entry point
├── requirements.txt         # Python dependencies
├── Procfile                 # Deployment configuration
```

## Authors

- Roman Gainutdinov
- Anton Sharoinin
- Arseniy Kiselev
- Dmitriy Pleskachev
- Dmitriy Kornev

## Contact

- Email: [roman.gainutdinov@urfu.me](mailto:roman.gainutdinov@urfu.me)
- Telegram: [@ffonel](https://t.me/ffonel)

## Additional Information

This project was developed by first-year students of Ural Federal University (UrFU), Institute of Radioelectronics and Information Technology (IRIT-RTF), specializing in Applied Artificial Intelligence.

---

# Multirec (Russian Version)

## Обзор

Multirec — это веб-приложение, которое позволяет пользователям комбинировать информацию о фильмах для создания новых рекомендаций на основе их ввода. Проект состоит из серверной части, реализованной с использованием Flask, и клиентской части на HTML, CSS и JavaScript.

## Возможности

- Получение информации о фильмах через OMDB API.
- Обработка данных о фильмах и генерация рекомендаций.
- Адаптивный дизайн для настольных и мобильных устройств.

## Требования

- Python 3.8+
- Flask
- Подключение к Интернету (для запросов к OMDB и OpenAI API). Убедитесь, что вы настроили ключ OpenAI API в файле `.env`.

## Установка

### Шаг 1: Клонируйте Репозиторий

```bash
git clone <repository_url>
cd Multirec
```

### Шаг 2: Установите Зависимости

```bash
pip install -r requirements.txt
```

### Шаг 3: Настройте Переменные Окружения

Создайте файл `.env` в корневой директории со следующим содержанием:

```env
OMDB_API_KEY=<ваш_ключ_omdb_api>
OPENAI_API_KEY=<ваш_ключ_openai_api>
```

### Шаг 4: Запустите Приложение

```bash
python app.py
```

### Шаг 5: Откройте Приложение

Введите в адресной строке браузера `http://127.0.0.1:5000/`.

## Структура Проекта

```
project/
├── server/
│   ├── routes.py          # Конечные точки API
│   ├── services/
│   │   ├── omdb_service.py  # Взаимодействие с OMDB API
│   │   ├── movie_info.py    # Обработка данных о фильмах
│   ├── utils/
│       ├── gpt_request.py   # Взаимодействие с GPT API
│       ├── config.py        # Загрузка переменных окружения
├── client/
│   ├── index.html           # Главный HTML файл
│   ├── static/
│       ├── favicon.ico      # Фавикон
│       ├── images/          # Изображения
│       ├── fonts/           # Шрифты
│       ├── script.js        # Логика фронтенда
│       ├── style.css        # Стили
├── .env                     # Переменные окружения
├── .gitignore               # Игнорируемые файлы Git
├── README.md                # Документация проекта
├── app.py                   # Точка входа Flask
├── requirements.txt         # Зависимости Python
├── Procfile                 # Конфигурация для деплоя
```

## Авторы

- Роман Гайнутдинов
- Антон Шаронин
- Арсений Киселев
- Дмитрий Плескачёв
- Дмитрий Корнев

## Контакты

- Email: [roman.gainutdinov@urfu.me](mailto:roman.gainutdinov@urfu.me)
- Telegram: [@ffonel](https://t.me/ffonel)

## Дополнительная Информация

Этот проект был разработан студентами 1 курса Уральского федерального университета (УрФУ), Института радиоэлектроники и информационных технологий (ИРИТ-РТФ), направления "Прикладной искусственный интеллект".