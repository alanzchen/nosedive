'use strict';

var screen = document.querySelector('.screen');

$('.menu').on('click', function () {
    $('.menu').toggleClass('active');
    $('.navigation').toggleClass('active');
});

if ($(".share-home").length) {
    var quote = "How close are you to be a four-two?";
    var fb_url = "https://www.facebook.com/dialog/share?app_id=1274857269241144&display=popup&href="
        + encodeURIComponent(window.location.href) + '&quote=' + encodeURIComponent(quote);
    $(".share-home").attr("href", fb_url);
}

var num = parseInt(250 * 100, 10);
if ($("#data").length || $("login").length) {
    var done = true;
    var score = $("#data").attr("score");
    var quote = "I'm " + score + ". How close are you to be a four-two?";
    var fb_url = "https://www.facebook.com/dialog/share?app_id=1274857269241144&display=popup&href="
        + encodeURIComponent(window.location.href) + '&quote=' + encodeURIComponent(quote);
    $(".share-link").attr("href", fb_url);
} else {
    var done = false;
    jQuery.ajax({
        url: "/calculate",
        success: function (result) {
            done = true;
            var response = JSON.parse(JSON.stringify(result));
            // $('#spinner').hide();
            var newnum = parseInt(response["final_score"] * 100000, 10);
            console.log(num);
            console.log(newnum);
            if (newnum * 100 > num) {
                $('#waiting').fadeOut();
                $('#waiting').html("Wow, someone just rated you 5 stars!");
                $('#waiting').fadeIn();
                num = newnum
                set_num();
                setTimeout(function () {
                    $('#waiting').fadeOut();
                }, 1000)
            } else {
                $('#waiting').fadeOut();
                $('#waiting').html("Oops, someone just rated you 1 star.");
                $('#waiting').fadeIn();
                num = newnum
                set_num();
                setTimeout(function () {
                    $('#waiting').fadeOut();
                }, 1000)
            }
            $("#final_score").html("Your rating is " + response["int"] + "\<sup\>" + response["decimal"] + "\</sup\>");
            $("#bonus").html("\<small\>You got " + response["bonus"] + " bonus points \<br\> from your PRIME friends.\</small\>");
            setTimeout(function () {
                $("#final_score").fadeIn();
                $("#bonus").fadeIn();
                $("#share").fadeIn();
            }, 1500)
            var quote = "I'm " + response["int"] + response["decimal"] + ". How close are you to be a four-two?";
            var fb_url = "https://www.facebook.com/dialog/share?app_id=1274857269241144&display=popup&href="
                + encodeURIComponent(window.location.href) + '&quote=' + encodeURIComponent(quote);
            $(".share-link").attr("href", fb_url);
        }
    });
}


function pad(n, width, z) {
    z = z || '0';
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

if (!done) {
    setTimeout(function () {
        $('.cou-item').find('ul').each(function (i, el) {
            var val = pad(num, 4, 0).split("");
            var $el = $(this);
            $el.removeClass();
            $el.addClass('goto-' + val[i]);
        })
    }, 10);

    setTimeout(function () {
        counter();
    }, 2500)
}


function counter() {
    setInterval(function () {
        if (!done) {
            $('.cou-item').find('ul').each(function (i, el) {
                    num += 1;
                    var val = pad(num, 4, 0).split("");
                    var $el = $(this);
                    $el.removeClass();
                    $el.addClass('goto-' + val[i]);
                }
            )
        }
    }, Math.random());
}

function set_num() {
    $('.cou-item').find('ul').each(function (i, el) {
        var val = pad(num, 4, 0).split("");
        var $el = $(this);
        $el.removeClass();
        $el.addClass('goto-' + val[i]);
    })
}