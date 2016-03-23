$(document).ready( function() {

    $('#submission').change( function() {

        var runName = $('#submission option:selected');
        runName = runName.text();
        $.get('/TRECapp/profile-info/', {selected_run: runName}, function(data) {
            $('#user-ranking-info').empty();
            $('#user-ranking-info').append(data);
        });

    });

});