//Makes sure the select can be validated
$("select").material_select();

// for HTML5 "required" attribute
$("select[required]").css({display: "inline", height: 0, padding: 0, width: 0});

$.validator.addMethod("youtube", function(value) {
  return /^(http(s)??\:\/\/)?(www\.)?((youtube\.com\/watch\?v=)|(youtu.be\/))([a-zA-Z0-9\-_])+/.test(value);
}, "Make sure to enter a youtube url");

$("form[name='add_video']").validate({
    rules: {
      video_url: {
        required: true,
        url: true,
        youtube:true
      },
      category: {
          required: true
      },
      language_name: {
          required: true
      },
      body_part_name: {
          required: true
      },
      contributor_username: {
          required: true
      }
    },
    
    messages: {
      video_url: {
        required: "Please enter a Youtube url",
        url: "Please enter a valid Youtube url (don't forget the 'http://')",
        youtube: "Please enter a valid Youtube url (don't forget the 'http://')"
      },
      category:{
        required: "Please select a category",
      },
      language_name: {
        required: "Please select a language",
      },
      body_part_name: {
        required: "Please select a targetted body part",
      },
      contributor_username: {
        required: "Please enter your username",
      }
    },

    submitHandler: function(form) {
      form.submit();
    },
    
    errorElement : 'div',
        errorPlacement: function(error, element) {
          var placement = $(element).data('error');
          if (placement) {
            $(placement).append(error)
          } else {
            error.insertAfter(element);
          }
        }
})