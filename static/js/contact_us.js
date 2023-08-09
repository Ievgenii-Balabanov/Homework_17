$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    console.log(loadForm)
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-contact-us .modal-content").html("");
        console.log("First")
        $("#modal-contact-us").modal("show");
      },
      success: function (data) {
        $("#modal-contact-us .modal-content").html(data.html_form);
        console.log("Second")
      }

    });
  };


  var emailForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-contact-us").modal("hide");
          alert("Success! Your message has been sent successfully!");
        }
        else {
          $("#modal-contact .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Contact Us
  $(".js-contact-us").click(loadForm);
  $("#modal-contact-us").on("submit", ".js-contact-form", emailForm);

});