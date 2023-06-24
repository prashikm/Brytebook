$("form").submit(function (e) {
  function ajax_call(userEmail) {
    var formData = {
      email: userEmail,
    };

    $.ajax({
      type: "POST",
      url: "/login",
      data: formData,
      dataType: "json",
      encode: true,
    }).done(function (data) {
      if (!data.success) {
        if (data.email_error) {
          setAlert("small:first", data.email_error);
        } else {
          setAlert("small:first", "");
        }
      } else {
        console.log("Success");
        window.location.href = "/home";
      }
    });
  }

  const email = $("#email").val().trim();
  let validateEmail = emailValidation(email);
  if (validateEmail !== true) {
    setAlert("small", validateEmail);
  } else {
    setAlert("small", "");
  }

  if (validateEmail === true) {
    ajax_call(email);
  }

  e.preventDefault();
});
