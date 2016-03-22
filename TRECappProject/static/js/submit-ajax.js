$(document).ready( function() {

    $('#id_track').change(function() {
        var track = $('#id_track option:selected');
        track = track.text();
        $.get('/TRECapp/leaderboard/relevant-tasks/', {selected_track: track}, function(data) {
            $('#id_task').find('option').remove().end()
            $('#id_task').append(data);
        });

    });



});