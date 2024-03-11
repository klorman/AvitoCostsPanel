-- Предполагается, что таблица categories уже создана, так как вы не запросили скрипт для её создания.
-- Очистка таблицы categories от предыдущих записей для избежания дубликатов.
-- Внимание: Это приведет к удалению всех существующих данных в таблице!
TRUNCATE TABLE categories RESTART IDENTITY CASCADE;

-- Временно отключаем проверку внешних ключей для упрощения вставки данных.
-- В PostgreSQL это делать не обязательно, но в некоторых СУБД это может быть полезно.
-- ALTER TABLE categories DISABLE TRIGGER ALL;

-- Вставка родительских категорий
INSERT INTO categories (name, parent_id)
VALUES
    ('Бытовая электроника', NULL),
    ('Готовый бизнес и оборудование', NULL),
    ('Для дома и дачи', NULL),
    ('Животные', NULL),
    ('Личные вещи', NULL),
    ('Недвижимость', NULL),
    ('Работа', NULL),
    ('Транспорт', NULL),
    ('Услуги', NULL),
    ('Хобби и отдых', NULL);

-- Вставка подкатегорий для "Для дома и дачи"
INSERT INTO categories (name, parent_id)
VALUES
    ('Мебель и интерьер', (SELECT id FROM categories WHERE name = 'Для дома и дачи')),
    ('Ремонт и строительство', (SELECT id FROM categories WHERE name = 'Для дома и дачи')),
    ('Продукты питания', (SELECT id FROM categories WHERE name = 'Для дома и дачи')),
    ('Растения', (SELECT id FROM categories WHERE name = 'Для дома и дачи')),
    ('Бытовая техника', (SELECT id FROM categories WHERE name = 'Для дома и дачи')),
    ('Посуда и товары для кухни', (SELECT id FROM categories WHERE name = 'Для дома и дачи'));

-- Вставка подкатегорий для "Животные"
INSERT INTO categories (name, parent_id)
VALUES
    ('Другие животные', (SELECT id FROM categories WHERE name = 'Животные')),
    ('Товары для животных', (SELECT id FROM categories WHERE name = 'Животные')),
    ('Птицы', (SELECT id FROM categories WHERE name = 'Животные')),
    ('Аквариум', (SELECT id FROM categories WHERE name = 'Животные')),
    ('Кошки', (SELECT id FROM categories WHERE name = 'Животные')),
    ('Собаки', (SELECT id FROM categories WHERE name = 'Животные'));


-- Вставка подкатегорий для "Готовый бизнес и оборудование"
INSERT INTO categories (name, parent_id)
VALUES
    ('Готовый бизнес', (SELECT id FROM categories WHERE name = 'Готовый бизнес и оборудование')),
    ('Оборудование для бизнеса', (SELECT id FROM categories WHERE name = 'Готовый бизнес и оборудование'));

-- Вставка подкатегорий для "Бытовая электроника"
INSERT INTO categories (name, parent_id)
VALUES
    ('Товары для компьютера', (SELECT id FROM categories WHERE name = 'Бытовая электроника')),
    ('Фототехника', (SELECT id FROM categories WHERE name = 'Бытовая электроника')),
    ('Телефоны', (SELECT id FROM categories WHERE name = 'Бытовая электроника')),
    ('Планшеты и электронные книги', (SELECT id FROM categories WHERE name = 'Бытовая электроника')),
    ('Оргтехника и расходники', (SELECT id FROM categories WHERE name = 'Бытовая электроника')),
    ('Ноутбуки', (SELECT id FROM categories WHERE name = 'Бытовая электроника')),
    ('Настольные компьютеры', (SELECT id FROM categories WHERE name = 'Бытовая электроника')),
    ('Игры, приставки и программы', (SELECT id FROM categories WHERE name = 'Бытовая электроника')),
    ('Аудио и видео', (SELECT id FROM categories WHERE name = 'Бытовая электроника'));



INSERT INTO categories (name, parent_id)
VALUES
    ('Детская одежда и обувь', (SELECT id FROM categories WHERE name = 'Личные вещи')),
    ('Одежда, обувь, аксессуары', (SELECT id FROM categories WHERE name = 'Личные вещи')),
    ('Товары для детей и игрушки', (SELECT id FROM categories WHERE name = 'Личные вещи')),
    ('Часы и украшения', (SELECT id FROM categories WHERE name = 'Личные вещи')),
    ('Красота и здоровье', (SELECT id FROM categories WHERE name = 'Личные вещи'));


INSERT INTO categories (name, parent_id)
VALUES
    ('Недвижимость за рубежом', (SELECT id FROM categories WHERE name = 'Недвижимость')),
    ('Квартиры', (SELECT id FROM categories WHERE name = 'Недвижимость')),
    ('Коммерческая недвижимость', (SELECT id FROM categories WHERE name = 'Недвижимость')),
    ('Гаражи и машиноместа', (SELECT id FROM categories WHERE name = 'Недвижимость')),
    ('Земельные участки', (SELECT id FROM categories WHERE name = 'Недвижимость')),
    ('Дома, дачи, коттеджи', (SELECT id FROM categories WHERE name = 'Недвижимость')),
    ('Комнаты', (SELECT id FROM categories WHERE name = 'Недвижимость'));


INSERT INTO categories (name, parent_id)
VALUES
    ('Резюме', (SELECT id FROM categories WHERE name = 'Работа')),
    ('Вакансии', (SELECT id FROM categories WHERE name = 'Работа'));


INSERT INTO categories (name, parent_id)
VALUES
    ('Предложения услуг', (SELECT id FROM categories WHERE name = 'Услуги'));


INSERT INTO categories (name, parent_id)
VALUES
    ('Охота и рыбалка', (SELECT id FROM categories WHERE name = 'Хобби и отдых')),
    ('Спорт и отдых', (SELECT id FROM categories WHERE name = 'Хобби и отдых')),
    ('Коллекционирование', (SELECT id FROM categories WHERE name = 'Хобби и отдых')),
    ('Книги и журналы', (SELECT id FROM categories WHERE name = 'Хобби и отдых')),
    ('Велосипеды', (SELECT id FROM categories WHERE name = 'Хобби и отдых')),
    ('Музыкальные инструменты', (SELECT id FROM categories WHERE name = 'Хобби и отдых')),
    ('Билеты и путешествия', (SELECT id FROM categories WHERE name = 'Хобби и отдых'));



INSERT INTO categories (name, parent_id)
VALUES
    ('Автомобили', (SELECT id FROM categories WHERE name = 'Транспорт')),
    ('Запчасти и аксессуары', (SELECT id FROM categories WHERE name = 'Транспорт')),
    ('Грузовики и спецтехника', (SELECT id FROM categories WHERE name = 'Транспорт')),
    ('Водный транспорт', (SELECT id FROM categories WHERE name = 'Транспорт')),
    ('Мотоциклы и мототехника', (SELECT id FROM categories WHERE name = 'Транспорт'));