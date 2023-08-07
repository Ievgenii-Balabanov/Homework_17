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
        $("#contact_us .modal-content").html("");
        console.log("First")
        $("#contact_us").modal("show");
      },
      success: function (data) {
        $("#contact_us .modal-content").html(data.html_form);
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
          $("#contact_us").modal("hide");
          alert("Fuck you");
        }
        else {
          $("#contact_us .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-contact-us").click(loadForm);
  $("#contact-us").on("submit", ".js-contact-us-form", emailForm);

});