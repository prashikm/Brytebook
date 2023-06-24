$("form").submit(function (e) {
  function ajax_call(theName, theBio) {
    var formData = {
      name: theName,
      bio: theBio,
    };

    $.ajax({
      type: "POST",
      url: "/profile/validate_profile/",
      data: formData,
      dataType: "json",
      encode: true,
    }).done(function (data) {
      if (!data.success) {
        if (data.name_error) {
          setAlert("small:first", data.name_error);
        } else {
          setAlert("small:first", "");
        }
      } else {
        window.location.href = "/signup/finished";
      }
    });
  }

  const name = $("#name").val().trim();
  let validateName = nameValidations(name);
  if (validateName !== true) {
    setAlert("small:first", validateName);
  } else {
    setAlert("small:first", "");
  }

  const bio = $("#bio").val().trim();
  let validateBio = bioValidation(password);
  if (validateBio !== true) {
    setAlert("small:last", validateBio);
  } else {
    setAlert("small:last", "");
  }

  if (validateName === true && validateBio === true) {
    ajax_call(name, bio);
  }

  e.preventDefault();
});

const messageEle = document.getElementById("bio");
const counterEle = document.getElementById("counter");

messageEle.addEventListener("input", function (e) {
    const target = e.target;

    // Get the `maxlength` attribute
    const maxLength = target.getAttribute("maxlength");

    // Count the current number of characters
    const currentLength = target.value.length;

    counterEle.innerHTML = `${currentLength}/${maxLength}`;
});