BalloonBlockEditor.create(document.querySelector("#text-editor"), {
  placeholder: "Start writing...",
  extraPlugins: [MyCustomUploadAdapterPlugin],
  image: {
    toolbar: [
      "imageStyle:alignCenter",
      "imageResize",
      "|",
      "toggleImageCaption",
      "imageTextAlternative",
    ],
  },
  mediaEmbed: {
    previewsInData: true,
    removeProviders: [
      "instagram",
      "twitter",
      "googleMaps",
      "flickr",
      "facebook",
    ],
  },
})
  .then((editor) => {
    window.editor = editor;
  })
  .catch((error) => {
    console.error("Oops, something went wrong!");
    iziToast.error({
      position: "topRight",
      title: "Error",
      message: "Something went wrong, please refresh page.",
    });
  });

var saved = true;
document.getElementById("text-editor").addEventListener(
  "input",
  function () {
    saved = false;
  },
  false
);

$(window).on("beforeunload", function (e) {
  if (saved == false) {
    return false;
  }
});
