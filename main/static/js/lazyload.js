(function ($, window, undefined) {
    $.fn.DataLazyLoad = function (options) {
        var elements = $(this);
        var settings = {
            //Data Load Offset
            offset: 200,
            //Load data callback
            load: function () { },
            //Which page to load
            page: 2
        }
        if (options) {
            $.extend(settings, options);
        }
        //The height of the browser window
        var winHeight = $(window).height();
        var locked = false;
        $(window).scroll(function () {
            var scrollTop = $(window).scrollTop();
            //elements height + elements top - (scrollbar top + browser window height)
            var offset = $(elements).offset().top + $(elements).height() - (scrollTop + winHeight);
            if (offset < settings.offset && !locked) {
                locked = true;
                settings.load(settings.page, function () {
                    locked = false;
                });
            }
        });
    }
    $.fn.DataLazyLoad = function (options) {
        var elements = $(this);
        var settings = {
            //Data Load Offset
            offset: 200,
            //Load data callback
            load: function () { },
            //Which page to load
            page: 2
        }
        if (options) {
            $.extend(settings, options);
        }
        //The height of the browser window
        var winHeight = $(window).height();
        var locked = false;
        var unLock = function (nextPage) {
            //Next load page, 0 is end
            if (nextPage > 0) {
                settings.page = nextPage;
                locked = false;
            }
        }
        $(window).scroll(function () {
            var scrollTop = $(window).scrollTop();
            //elements height + elements top - (scrollbar top + browser window height)
            var offset = $(elements).offset().top + $(elements).height() - (scrollTop + winHeight);
            if (offset < settings.offset && !locked) {
                locked = true;
                settings.load(settings.page, unLock);
            }
        });
    }
})(jQuery, window);