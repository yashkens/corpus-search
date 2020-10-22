## Корпус фантастики 

#### [Веб-приложение для поиска](https://corpus-search.herokuapp.com/)
* Для разметки использовался PyMorphy, поэтому набор частеречных тегов соответствующий. Он полностью приведен на сайте с приложением.
* На странице отображается максимум 20 предложений, всю выдачу целиком можно скачать на той же странице.

### Тексты
Тексты были скачаны с [Самиздата](http://samlib.ru/). Раздел фантастика.

### Структура файлов

* corpus-search.py - основной файл с кодом
* corpus.csv - файл с размеченными предложениями из корпуса
* templates - папка с html файлами

В основном файле отсутствует часть кода с разметкой предложений. Эту часть можно посмотреть в jupyter тетрадке, также там есть и все остальное, но запустить не получится, так как папка с текстами в репозиторий не загружена. Пожалуйста, сообщите, если ее нужно сюда внести!
* jupyter-notebook - папка с тетрадкой

----
*Предостережения*
* *Да, поиск работает не очень быстро. Пожалуйста, запаситесь терпением!*
* *Пожалуйста, не производите больше одного поиска одновременно, иначе веб-приложение выдаст неправильный файл со всеми ответами.*
----
Проект выполнила Яна Шишкина, БКЛ182