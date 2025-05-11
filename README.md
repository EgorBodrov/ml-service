# ml-service

## Разработка ML сервисов на Python

**[Выбранный набор данных](https://www.kaggle.com/datasets/imgowthamg/car-price)** для задачи предсказания цены автомобиля на основании некоторых аттрибутов

### Обученные алгоритмы

`sklearn.linear_models.LinearRegression`

`sklearn.ensemble.GradientBoostingRegressor`

`sklearn.ensemble.RandomForestRegressor`


## Установка

**Создание окружения**

```shell
conda create -n <name_of_venv> python=3.12 -y
conda activate <name_of_venv>
```

**Установка пакетного менеджера poetry (версия 1.8.4)**
```shell
pip install poetry==1.8.4
```

**Установка зависимостей и пакетов**
```shell
poetry install --all-extras
```
