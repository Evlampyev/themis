### Ссылки на ресурсы, в которых много интересного

* Классное [меню](https://codepen.io/alticreation/pen/YWyEpm) адаптируется на ширину экрана.

* [Таблица](https://codepen.io/takaneichinose/pen/QWyXjNP?editors=1000) очень красивая, не знаю как её в нормальный html
  перевезти

* Различные **анимации** и другие [плюшки](https://www.cssportal.com) для html

* ManyToMany поля и работа с ними [тут](https://metanit.com/python/django/5.7.php)

* Аутентификация и авторизация пользователя в джанго [тут](https://habr.com/ru/articles/787040/)

* Связывание [абстрактного класса User](https://proproprogs.ru/django4/django4-rasshirenie-modeli-user-klass-abstractuser) 
(встроенного) со своей моделью для авторизации и всего остального


* Стратегии расширения [Django User Model](https://habr.com/ru/articles/313764/)

* Работа с формами [proglib.io](https://proglib.io/p/study_html_forms)

* Слияние [веток](https://git.github.io/git-scm.com/book/ru/v2/Ветвление-в-Git-Перебазирование/)

#### развернуть на vds с debian/ubuntu:

1. apt install git
2. mkdir project
3. git clone...
4. apt install python3.11-venv
5. python3 -m venv venv
6. pip install -r project/requirements.txt
7. mkdir logs
8. python3.11 manage.py migrate
9. python3.11 manage.py runserver
10. через nginx выбрасываем в интернет, 5 минут, сайт готов

> cerbot для бесплатного сертификата, ну и свой домен для доменного имени

#### git helper

__git merge feature --squash__ - объединит изменения всех коммитов ветки feature, перенесет их в ветку master
и добавит в индекс. При этом коммит слияния не будет создан, вам нужно будет сделать его вручную.

__git merge --abort__ - отменить слияние

__лучшее слияния веток__
-- o -- o -- o [main]
    \
     o -- o [tasks]
в tasks все хорошо стало работать и нужно сделать её основной веткой, для этого: 

git checkout tasks # переключится в tasks
git merge master # слияние ветки master с текущей

- o -- o -- o [main]
    \         \
     o -- o -- o [HEAD -> tasks]

Запустите несколько тестов; убедитесь, что все работает как ожидалось. 
Затем проверьте __main__ и объедините __tasks__ в нем:

git checkout main
git merge tasks

Тогда ваш репозиторий будет выглядеть следующим образом:

-- o -- o -- o
    \         \
     o -- o -- o [HEAD -> main,tasks]

Теперь переходим на ветку tasks и продолжаем в ней работать.