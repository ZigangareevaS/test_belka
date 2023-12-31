## **1. Подготовка данных**

Изучены данные о продаже квратир с сайта магнитогорской недвижимости www.citystar.ru.

Собран датасет, который включает в себя 397 наблюдений (после удаления дубликатов) и 15 столбцов, в том числе целевой признак - цену недвижимости. Пропусков в данных нет, но есть поля, содержащие пустые строки.

Признаки приведены к правильным типам данных и предобработаны:
Удалены неинформативные признаки: url (ссылка на объявление), house(дом), layout(планировка).

Видно, что в данных представлены объявления о продаже недвижимости за период с октября 2021 года по август 2023. Период после обновления объявления (редактирования) представлен с марта 2023 по август 2023г.
Ожидаемо, основная масса объявлений были опубликованы в 2023 году, в период с апреля по август и редактировалась большая часть из них в последний месяц. Т.е. нерелевантных объявлений нет.

Исправлены отпечатки в названиях районов. Район не указан почти в 40% случаев. 
Чаще всего продаются квартиры на ул. Ленина, Маркса, Советсткой, Зеленый лог, труда. Возможно, это связано с тем, что проспект Ленина и проспект Карла Маркса - одни из самых протяженных в Магнитогорске. Отсутствуют названия улиц в 6 случаях.

Больше всего в данных представлено 2 и 3-х комнатных квартир, на третьем месте 1-комнатные.

Удалены наблюдения со стоимость равной 0 (аномалии). 

В датасет добавлены новые признаки:
 - возраст объявления age (исходные признаки удалены после создания новых)
 - living/total и kitchen/living - признаки показывающие соотношение (планировку) между разными типами площадей
 - среднее количество просмотров в день
 - векторное представление столбца note - после лемматизации и очистки текстов от цифр, знаков препинания и пр. приведен в векторный формат при помощи tf-idf. В итоге получена матрица размерности (394, 426). С учетом небольшого количества данных такое признаковое пространство может приводить к проблемам при обучении модели. Поэтому размерность матрицы после tf-idf снижена при помощи метода главных компонент PCA с количеством компонент = 5.

При оценке соотношений между разными типами площадей видно, что жилая площадь как правило составляет 60-70% от общей. А площадь кухни составляет 20% от жилой.
Медианно значение признака mean_views равняется 0.78, это означает, что объявление просматривают менее одного раза в день. Объявления с количеством просмотров 3 - 7 в день почти не встречаются.
Видно, что объявления как правило включают до 1000 знаков, но есть и пустые объявления. Максимальная длина 3500 знаков.

После предобработки и добавления новых признаков размер датафрейма стал (355, 20).

## **2. Подготовка к обучению модели**

При оценке влияния признаков на целевой признак отмечено, что тип недвижимости влияет на стоимость. Так видно, что однокомнатный квартиры обычно дешевле двухкомнатных, а трехкомнатные дороже двухкомнатных.
Четырехкомнатных квартир немного и они не выходят по стоимости за пределы трехкомнатных. 

При анализе влияния района нахождения квартиры на стоимость выявлено, что у самых дешевых квартир не указан район. Из тех, у которых район указан самые недорогие варианты находятся в районе Оржоникидзевский (левый берег), но их представлено не много, затем Правобережный, Ленинский и  самый дорогой Оржоникидзевский.

У квартир 1, 2 и 3 этажей разброс цен выше тех, что на 4 или 5 этаже.

Почти прямая зависимость с ценой у признака total_area - площадь квартиры и признака living_area. Площадь кухни kitchen_area показывает меньшую зависимость.

По матрице корреляций видно, что высокие показатели корреляции Спирмена (~ 0.7) корреляции у:
 - total_area - living_area (0.93)
 - living_area - kitchen/living (-0.71)
 - views - age (0.82)
 - kitchen/living - living/total (-0.75)
 - PCA_2 - len_text (-0.67)
 - mean_views - age (-0.63)
 
Для пространства признаков, в котором есть мультиколлинеарные признаки, подходят модели, которые устойчивы к мультиколлинеарности и имеют методы выбора признаков, такие как регуляризация (например, L1 или L2-регуляризация), чтобы уменьшить влияние коррелированных признаков и избежать переобучения модели.

С учетом наличия категориальных признаков, таких как street и neighborhood и малого количества данных (не хочется увеличивать пространство признаков при OHE-кодировании), будем использовать модели на основе деревьев решений, так как они не нуждаются в масштабировании данных. Категориальные переменные закодируем Ordinal Encoding. 

Поэтому для обучения будем использовать модели:

 - Random Forest
 - LGBMRegressor

## **3. Подбор и обучение моделей**

Так как в задании не указана метрика для оценки модели, будем использовать MAE. Эта метрика измеряет среднюю абсолютную разницу между прогнозируемыми и фактическими значениями стоимости недвижимости. Она более устойчива к выбросам и может быть полезной в случае наличия выбросов в данных.

MAE наивного регрессора, который для всех наблюдений предсказывает среднее значение составляет 1041.95 тысяч.

Подбор лучших гиперпараметров осуществлялся при помощи RandomizedSearchCV.

Лучшая модель - RandomForestRegressor, MAE для best_estimator_ составляет 605.05 на кросс-валидации. Лучшие результаты для остальных моделей представлены в таблице.


| Модель | среднее MAE на кроссвалидации | Место в итоговой таблице |
|----------|----------|----------|
| RandomForestRegressor    | 605.05 | 1 |
| LGBMRegressor    | 649.38 | 7 |


Лучшая модель была проверена на тестовой выборке, ее результат составляет 532.23 тысячи.

При анализе важности признаков на первом месте ожидаемо с большим отрывов total_area.

__Топ-10 признаков:__
1. total_area	
2. living_area	
3. PCA_4	
4. total_floors	
5. mean_views	
6. age	
7. PCA_5	
8. views	
9. kitchen_area	
10. street	

Среди исходных видны так же признаки, созданные - это PCA_4, PCA_5, total_floors, mean_views, age. Т.е., сгенерированные признаки содержат информацию, которая является важной и релевантной для целевой переменной или помогают модели лучше предсказывать целевую переменную.

**Что можно сделать еще:**

 - Данных недостаточно - спарсить еще, чтобы модели было проще находить закономерности в данных.
 - Добавить еще признаки, например, по адресу восстановить широту и долготу или другие географические данные (расстояние до ближайших объектов инфраструктуры их количество и типы, ближайшие остановки общественного транспорта) или информацию о продавце.
 - Проанализировать ошибки модели - посмотреть на чем она ошибается и использовать эту информацию для улучшения прогноза.
