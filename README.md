# Асинхронный ml-сервис

## Разработка ML сервисов на Python

**[Выбранный набор данных](https://www.kaggle.com/datasets/imgowthamg/car-price)** для задачи предсказания цены автомобиля на основании некоторых аттрибутов

## [**Смотреть демо работы**](https://drive.google.com/file/d/1SI6vH_cXoaSQreiKyVk6Fx_P_aUUVcqE/view?usp=sharing)

## Обученные алгоритмы

`sklearn.linear_models.LinearRegression`

`sklearn.ensemble.GradientBoostingRegressor`

`sklearn.ensemble.RandomForestRegressor`


## Запуск

1. Заполнить файл `.env` на подобии `.env.template`.
2. Выполнить ноутбук с обучением моделей.
3. Выполнить `sudo docker compose up -d`.


## Структура compose проекта
- **postgres**. Развернутая БД для хранения информации.
- **redis**. REDIS для асинхронных очередей
- **worker**. В отдельном контейнере worker для прослушивания новых запросов на добавление в очередь
- **app**. CORE приложение на FastAPI
- **streamlit**. Веб-морда


## Структура директорий


```plain
.
├── docker  # Докерфайлы для сервисов
│   ├── Dockerfile.app
│   ├── Dockerfile.streamlit
│   └── Dockerfile.worker
├── ml  # Ноутбук с обучением, сохранением чекпоинтов
│   ├── __init__.py
│   └── preprocessing.ipynb
├── src
│   ├── __init__.py
│   ├── config  # Настройка подключения к БД
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── core
│   │   ├── entities
│   │   │   ├── __init__.py
│   │   │   ├── prediction_event.py
│   │   │   ├── predictor.py
│   │   │   ├── user.py
│   │   │   └── user_balance.py
│   │   ├── repositories
│   │   │   ├── __init__.py
│   │   │   ├── prediction_event_repository.py
│   │   │   ├── predictor_repository.py
│   │   │   ├── user_balance_repository.py
│   │   │   └── user_repository.py
│   │   └── use_cases
│   │       ├── __init__.py
│   │       ├── prediction_event_use_cases.py
│   │       ├── predictor_use_cases.py
│   │       ├── user_balance_use_cases.py
│   │       └── user_use_cases.py
│   ├── infrastructure
│   │   ├── db
│   │   │   ├── models  # Модели для SQLAlchemy
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── prediction_event_model.py
│   │   │   │   ├── predictor_model.py
│   │   │   │   ├── user_balance_model.py
│   │   │   │   └── user_model.py
│   │   │   ├── repositories
│   │   │   │   ├── __init__.py
│   │   │   │   ├── prediction_event_repository_impl.py
│   │   │   │   ├── predictor_repository_impl.py
│   │   │   │   ├── user_balance_repository_impl.py
│   │   │   │   └── user_repository_impl.py
│   │   │   └── utils.py
│   │   ├── tasks   # Таски для очереди в Redis
│   │   │   └── model_predict.py
│   │   └── web
│   │       ├── controllers
│   │       │   ├── get_current_user.py
│   │       │   ├── predictor_controller.py
│   │       │   ├── user_balance_controller.py
│   │       │   └── user_controller.py
│   │       └── models  # API модели в Pydantic
│   │           ├── __init__.py
│   │           ├── predict_models.py
│   │           ├── user_balance_models.py
│   │           └── user_models.py
│   ├── main.py     # Точка входа в приложение FastAPI
│   └── utils.py
├── streamlit_app   # Streamlit веб
│   ├── main.py     # Точка входа в приложение Streamlit
│   ├── pages
│   │   ├── 1_start.py
│   │   └── 2_history.py
│   ├── post_requests.py
└── workers
    └── rq_worker.py    # Worker для запуска
```

## FastAPI Backend

### Модели базы данных

- `predictors`. Таблица со всеми доступными моделями для инференса (список моделей, их цена в кредитах)
- `users`. Таблица пользователей, включая их credentials
- `balances`. Таблица с балансом счета пользователей
- `prediction_events`. Таблица с историей запуска для каждого пользователя (one-to-many).


```sql
CREATE TABLE predictors (
	id SERIAL NOT NULL, 
	model_name VARCHAR(50) NOT NULL, 
	price INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (model_name)
);

CREATE TABLE users (
	id SERIAL NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	hashed_password VARCHAR(128) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);

CREATE TABLE balances (
	user_id INTEGER NOT NULL, 
	amount INTEGER NOT NULL, 
	PRIMARY KEY (user_id), 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE prediction_events (
	id SERIAL NOT NULL, 
	model_name VARCHAR(50) NOT NULL, 
	job_id VARCHAR(50) NOT NULL, 
	created_at VARCHAR(50) NOT NULL, 
	finished_at VARCHAR(50), 
	result FLOAT, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (job_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
```
---

### Алгоритм работы
1. Пользователь задает `name` + `email` + `password`.
2. Данные сохраняются в БД, пароль хешируется. По API пароль не светится нигде.
3. Пользователь проходит аутентификацию, создается JWT токен со временным ограничением в 30 минут на сессию.
4. При дальнейшем доступе к функционалу пользователь авторизуется с помощью этого токена.
5. Пользователь может просмотреть баланс.
6. Пользователь может пополнить баланс.
7. Пользователь может просмотреть список доступных `scikit-learn` моделей и их цену в кредитах за использование. Лучшая модель дороже.
8. Пользователь может запустить инференс выбранной модели на своих признаках чтобы узнать стоимость автомобиля.
9. Пользователь может просмотреть статус выполнения.
10. Пользователь может просмотреть историю запусков и ее результаты.
11. Все статусы и результаты автоматически обновляются в БД.
12. Пользователь может получить список всех текущих запущенных процессов.
---

### Обработка ошибок
- Исключения на уже зарегистрированного пользователя
- Исключения на некорректную авторизацию
- Исключения на попытку доступа без аутентификации и авторизации
- Исключения на попытку использования моделей если недостаточно кредитов
- Исключения на некорректный `request body` благодаря pydantic API моделям

---
### Маршрутизация

### 🔐 Аутентификация

#### 🔸 POST `/sign_up`

Создание нового пользователя.

**Request Body:**

```json
{
  "name": "John",
  "email": "john@example.com",
  "password": "yourpassword"
}
```

**Response:**

```json
{
  "name": "John",
  "email": "john@example.com"
}
```

---

#### 🔸 POST `/sign_in`

Авторизация пользователя.

**Request Body:**

```json
{
  "email": "john@example.com",
  "password": "yourpassword"
}
```

**Response:**

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer",
  "name": "John",
  "email": "john@example.com"
}
```

---

### 💰 Баланс пользователя

#### 🔸 GET `/balance`

Получить текущий баланс пользователя.

**Headers:**

```
Authorization: Bearer <JWT_TOKEN>
```

**Response:**

```json
{
  "amount": 50
}
```

---

#### 🔸 POST `/balance`

Обновить баланс пользователя.

**Headers:**

```
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**

```json
{
  "new_amount": 100
}
```

**Response:**

```json
{
  "amount": 100
}
```

---

### 📊 Предсказания

#### 🔸 GET `/predictors`

Получить список доступных моделей.

**Headers:**

```
Authorization: Bearer <JWT_TOKEN>
```

**Response:**

```json
{
  "models": [
    {"model_name": "linear_regression", "price": 10},
    {"model_name": "random_forest", "price": 40}
  ]
}
```

---

#### 🔸 POST `/predict`

Запустить задачу предсказания.

**Headers:**

```
Authorization: Bearer <JWT_TOKEN>
```

**Request Body:**

```json
{
  "model_name": "linear_regression",
  "data": {
    "horsepower": [110],
    "fueltype": ["gas"],
    "...": "..."
  }
}
```

**Response:**

```json
{
  "job_id": "rq:job:abc123"
}
```

---

#### 🔸 GET `/predict`

Получить статус задачи предсказания.

**Request Body:**

```json
{
  "job_id": "rq:job:abc123",
}
```

**Headers:**

```
Authorization: Bearer <JWT_TOKEN>
```

**Response:**

```json
{
  "job_id": "rq:job:abc123",
  "status": "finished",
  "model_name": "linear_regression",
  "created_at": "10/05/2025, 15:00:00",
  "finished_at": "10/05/2025, 15:00:05",
  "result": 13456.8
}
```

---

#### 🔸 GET `/history`

Получить историю всех задач пользователя.

**Headers:**

```
Authorization: Bearer <JWT_TOKEN>
```

**Response:**

```json
{
  "job_ids": [
    "rq:job:abc123",
    "rq:job:def456"
  ]
}
```
---

## Streamlit Frontend

### Алгоритм работы
1. Пользователь попадает на экран входа.
2. После регистрации/авторизации получает доступ к своему балансу и страницам с вводом данных, выбором моделей и истории запусков.
3. Все работает в рамках одной сессии.
4. Веб-интерфейс предлагает выбрать все аттрибуты автомобиля для определения цены, значения многих задаются по умолчанию на основании датасета, который был использован для обучения.

---
## Заключение
Асинхронный ML-сервис разработан с учетом требований к проекту, обернут в docker compose проект и работает с БД и асинхронной очередью задач для выполнения, что не блокирует FastAPI.

В качестве путей улучшения можно рассмотреть следующие шаги:
1. Улучшение UI/UX, сделать более user-friendly.
2. Расширить метаданную в базе данных (сохранение даты последних обновлений, параметры запуска и т.п.).
