window.onload = function () {
    /*
    // можем получить DOM-объект меню через JS
    var menu = document.getElementsByClassName('menu')[0];
    menu.addEventListener('click', function () {
        console.log(event);
        event.preventDefault();
    });
    */
    /*
    // можем получить DOM-объект меню через jQuery
    $('.menu').on('click', 'a', function () {
        console.log('event', event);
        console.log('this', this);
        console.log('event.target', event.target);
        event.preventDefault();
    });
    */
    /*
    // получаем атрибут href
    $('.menu').on('click', 'a', function () {
        var target_href = event.target.href;
        if (target_href) {
            console.log('нужно перейти: ', target_href);
        }
        event.preventDefault();
    });
    */

    // добавляем ajax-обработчик для обновления количества товара
    $('.basket_list').on('click', 'input[type="number"]', function (event) {
        var target_href = event.target;
        //alert(target_href.value)
        console.log(target_href);
        if (target_href) {
            //window.location.href = "/basket/edit/" + target_href.name + "/" + target_href.value + "/";
            $.ajax({
                url: "/basket/edit/" + target_href.name + "/" + target_href.value + "/",

                success: function (data) {
                    $('.basket_list').html(data.result);
                    console.log('ajax done');
                },
            });
        }
        event.preventDefault();
    });
    // добавляем ajax-обработчик для удаления товара
    $('.basket_list').on('click', 'button[class="btn_good"]', function (event) {
        var target_href = event.target;
        //alert(target_href.value)
        console.log(target_href);
        if (target_href) {
            //window.location.href = "/basket/edit/" + target_href.name + "/" + target_href.value + "/";
            $.ajax({
                url: "/basket/delete/" + target_href.name + "/",

                success: function (data) {
                    $('.basket_list').html(data.result);
                    console.log('ajax done');
                },
            });
        }
        event.preventDefault();
    });
    
}