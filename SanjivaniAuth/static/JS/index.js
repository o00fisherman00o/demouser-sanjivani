var perfEntries = performance.getEntriesByType("navigation");

if (perfEntries[0].type === "back_forward") {
    window.location.reload();
}

let msg



$("#forget-password").click(function() {
    $(this).css({ "display": "none" });
    $("#extra-option").css({ "display": "none" });
    $("#primary-login-form").css({ "display": "none" });
    $("#forget-pwd-form").css({ "display": "block" });
})

$("#login").click(function() {
    var phone = "+91" + $("#phone").val();
    var password = $("#password").val();
    $.ajax({
        url: '/login',
        data: { 'phone': phone, 'password': password },
        type: 'POST',
        success: function(response) {

            msg = response['msg'];
            if (msg === 'otp') {
                $("#primary-login-form").css({ "display": "none" });
                $("#secondary-login-form").css({ "display": "block" });

                var max_min = 4;
                var max_sec = 59;

                $("#error").css({ "color": "red" });

                setInterval(function() {
                    if (max_min === 0 && max_sec === 0) {
                        $("#error").text("00:00 , your OTP has expired");
                        window.location.reload();
                        clearInterval();
                    } else {
                        if (max_sec < 0) {
                            max_min--;
                            max_sec = 59;
                        } else {
                            max_sec--;
                        }
                        $("#error").text("Your otp will expire in" + max_min + ":" + max_sec);
                    }
                }, 1000);
            } else {
                $("#error").css({ "color": "red" });
                $("#error").text(msg);
            }

        },
        error: function() {
            console.log("error");
        }


    });

})
$("#otp-submit").click(function() {
    var otp = $("#otp").val();
    $.ajax({
        url: '/auth',
        data: { 'otp': otp },
        type: 'POST',
        success: function(response) {
            msg = response['msg'];
            if (msg === "loggedin") {
                window.location.href = "http://127.0.0.1:5000/"
            } else {
                $("#error").css({ "color": "red" });
                $("#error").text(msg);
            }
        },
        error: function() {
            console.log("some error");

        }

    })
})