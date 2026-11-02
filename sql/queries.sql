-- 1. Выборка всех актеров (SELECT)
SELECT * FROM actors ORDER BY full_name;

-- 2. Выборка конкретных полей (SELECT)
SELECT full_name, role_type FROM actors;

-- 3. Поиск по возрасту (WHERE)
SELECT * FROM actors WHERE age > 40;

-- 4. Поиск по статусу (WHERE)
SELECT * FROM actors WHERE is_active = 1;

-- 5. Поиск по амплуа (WHERE)
SELECT * FROM actors WHERE role_type = 'Главная роль';

-- 6. Сортировка и ограничение (ORDER BY + LIMIT)
SELECT * FROM actors ORDER BY age DESC LIMIT 2;

-- 7. Агрегатная функция: количество актеров (COUNT)
SELECT COUNT(*) AS total_actors FROM actors;

-- 8. Агрегатная функция: средний возраст (AVG)
SELECT AVG(age) AS average_age FROM actors;

-- 9. Группировка: сколько актеров в каждом амплуа (GROUP BY)
SELECT role_type, COUNT(*) AS count FROM actors GROUP BY role_type;

-- 10. Фильтрация групп: амплуа, где больше 1 актера (GROUP BY + HAVING)
SELECT role_type, COUNT(*) AS count FROM actors GROUP BY role_type HAVING COUNT(*) > 1;

-- 11. выборка активных актеров с их амплуа

SELECT a.full_name, a.role_type 
FROM actors a 
WHERE a.id IN (SELECT id FROM actors WHERE is_active = 1);