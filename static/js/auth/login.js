$("form").submit(function (e) {
  function loginCall(userEmail, userPassword) {
    $("#spinner").show();
    $("#loginBtn").attr("disabled", true);

    var formData = {
      email: userEmail,
      password: userPassword,
    };

    $.ajax({
      type: "POST",
      url: "/login",
      headers: {
        'X-CSRFToken': '{{ csrf_token }}'
      },
      data: formData,
      dataType: "json",
      encode: true,
    }).done(function (data) {
      if (!data.success) {
        $("#spinner").hide();
        $("#loginBtn").removeAttr("disabled");

        if (data.email_error) {
          setAlert("small:first", data.email_error);
        } else {
          setAlert("small:first", "");
        }

        if (data.some_error) {
          setAlert("small:last", data.some_error);
        } else {
          setAlert("small:last", "");
        }
      } else {
        window.location.href = "/home";
      }
    });
  }

  const email = $("#email").val().trim();
  let validateEmail = emailValidation(email);
  if (validateEmail !== true) {
    setAlert("small:first", validateEmail);
  } else {
    setAlert("small:first", "");
  }

  const password = $("#password").val().trim();
  let validatePassword = passwordValidation(password);
  if (validatePassword !== true) {
    setAlert("small:last", validatePassword);
  } else {
    setAlert("small:last", "");
  }

  if (validateEmail === true && validatePassword === true) {
    loginCall(email, password);
  }

  e.preventDefault();
});
