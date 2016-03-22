$(document).ready( function() {


    $('#track-selector').change(function() {
        var track = $('#track-selector option:selected');
        track = track.text();
        $.get('/TRECapp/relevant-tasks/', {selected_track: track}, function(data) {
            $('#task-selector').find('option').remove().end()
            $('#task-selector').append(data);
        });

    });

});