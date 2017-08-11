$( function() {
    $( document ).tooltip();
  } );
function send_message() {
    var $message_input = $('.message_input').val();
    speak($message_input);
    var message_side = 'right';

    var $messages, message;
    if ($message_input.trim() === '') {
        return;
    }


    $('.message_input').val('');    //to remove the typed message from the message box.
    $messages = $('.messages');     //to refer the messages box.

    $message = $($('.message_template').clone().html());
    $message.addClass(message_side).find('.text').html($message_input);
    $('.messages').append($message);
    $message.addClass('appeared');
    $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);



}

function put_message($message_input) {
    //var $message_input = $('.message_input').val();
    var message_side = 'left';

    var $messages, message;
    if ($message_input.trim() === '') {
        return;
    }


    $('.message_input').val('');    //to remove the typed message from the message box.
    $messages = $('.messages');     //to refer the messages box.

    $message = $($('.message_template').clone().html());
    $message.addClass(message_side).find('.text').html($message_input);
    $('.messages').append($message);
    return setTimeout(function () {
        $message.addClass('appeared');
        return $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
    }, 0);


}
function startDictation() {

    if (window.hasOwnProperty('webkitSpeechRecognition')) {

      var recognition = new webkitSpeechRecognition();

      recognition.continuous = true;
      recognition.interimResults = true;

      recognition.lang = "en-US";
      recognition.start();
      var st;
      recognition.onresult = function(e) {
        st = e.results[0][0].transcript;
        document.getElementById('message_input_id').value = st;
      };

      recognition.onerror = function(e) {
          recognition.stop();
      }
    }

}

function speak(text, callback) {
    var u = new SpeechSynthesisUtterance();
    u.text = text;
    u.lang = 'en-US';

    u.onend = function () {
        if (callback) {
            callback();
        }
    };

    u.onerror = function (e) {
        if (callback) {
            callback(e);
        }
    };

    speechSynthesis.speak(u);
}


function makeRequest_re(){

    var Country = $('#id_Country').val();
    var URL_key = $('#id_url').val();
    var start = $('#id_start').val();
    makeRequest(Country, URL_key, start);
}


function makeRequest(){


    var paragraph = $('#paragraph').val();
    var question = $('#id_url').val();
    var start = $('#id_start').val();
    args = {'Country': Country, 'URL_key': URL_key, 'start': start};
    $.ajax({url: '/', data: args, type: 'POST',




        error: function() {
            $('#output_text_id').html('An error has occurred');
        },
        success: function(data) {
            $('#output_text_id').html(data);
         }


     });
}