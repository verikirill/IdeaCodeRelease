# TTBank - Платформа с сервисами для университета

## О проекте

TTBank - это многофункциональная платформа для студентов и преподавателей университета, объединяющая различные сервисы, включая базу знаний.

## Функциональности

- **Аутентификация и авторизация пользователей**
  - Регистрация, вход, сброс пароля
  - Разные роли (студент, преподаватель, администратор)

- **База знаний с OCR и AI-обработкой**
  - Загрузка файлов (PDF, изображения, документы)
  - Автоматическое распознавание текста (OCR)
  - AI-обработка и структурирование текста
  - Хранение и организация учебных материалов

- **Расписание занятий**
  - Просмотр расписания для групп и преподавателей
  - Фильтрация и поиск

- **Доска объявлений и форум**
  - Создание и просмотр публикаций
  - Комментирование и оценка

- **Меню столовой**
  - Просмотр меню по дням
  - Информация о блюдах

- **AI-ассистент**
  - Интерактивный помощник для ответов на вопросы
  - Контекстная помощь по сайту



### Настройка Backend

1. Клонируйте репозиторий
   ```bash
   git clone https://github.com/Mojarung/IdeaCodeRelease_Web.git
   cd IdeaCodeRelease_Web/Backend
   ```

2. Создайте виртуальное окружение
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

3. Установите зависимости
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` на основе `.env.example`
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=ttbank
   DB_USER=postgres
   DB_PASS=postgres
   ```

5. Примените миграции
   ```bash
   python migrations/add_ocr_fields_to_knowledge.py
   ```

6. Запустите сервер
   ```bash
   uvicorn server:app --reload
   ```

### Настройка Frontend

1. Перейдите в директорию Frontend
   ```bash
   cd ../Frontend
   ```

2. Установите зависимости
   ```bash
   npm install
   ```

3. Запустите сервер разработки
   ```bash
   npm run dev
   ```
4. Откройте браузер по адресу `http://localhost:5173`



   
![tvoyff](https://github.com/user-attachments/assets/d6996d59-3c50-4df9-8b81-f48987af8e8b)
