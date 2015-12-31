$(function() {
    // 全局变量
    var $Menu = $('#nav');          // 左部菜单
    var $aMenuLi = $Menu.find('li');  // 菜单按钮

    //滚轮事件合并scroll
    function scrollAll(){
        var t = $Menu.offset().top;

        var $all = $('.container .section');

        var arrHeight = [];
        for(var i=0;i<$all.length;i++){
            arrHeight[i] = $all.eq(i).offset().top;
        }

        __fnFixNav();
        __fnScrollShowNav();
        $(window).on('scroll',function (){
            __fnFixNav();
            __fnScrollShowNav()
        });

        // 固定左边菜单
        function __fnFixNav(){
            var top = $(window).scrollTop();
            if(top > t){
                $Menu.css({
                    'position': 'fixed',
                    'top':        0,
                    'left':       0,
                    'z-index':    1000
                });
            }else{
                $Menu.css({
                    'position': 'relative'
                });
            }
        }

         //滚动自动显示左边菜单
        function __fnScrollShowNav(){
            var t = $(window).scrollTop();
            var isTrue = false;
            for(var i=0;i<arrHeight.length;i++){
                if(t<arrHeight[i]){
                    isTrue = true;
                    if(i==0){
                        $aMenuLi.removeClass('current').eq(0).addClass('current');
                    }else{
                        $aMenuLi.removeClass('current').eq(i-1).addClass('current');
                    }

                    break;
                }
            }
            if(!isTrue){
                $aMenuLi.removeClass('current').eq(arrHeight.length-1).addClass('current');
            }
        }
    }



    // 点击滑动菜单
    function moveMeue(){
        $aMenuLi.on('touchstart',function (){
            $aMenuLi.removeClass('current');
            $(this).addClass('current');

            var $item = $($(this).attr('data-href'));
            var t = $item.offset().top + $('.container-divzw').eq(-1).height();

            if($(this).index()===0){
                t = 0;
            }
            Mobile.scrollMove({
                y: t,
                time: 300
            });
        })
    }




    function init(){
        scrollAll();
        moveMeue();
    }

    init();
});