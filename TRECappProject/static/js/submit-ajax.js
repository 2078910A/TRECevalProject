$(document).ready( function() {

    $('#id_track').change(function() {
        var track = $('#id_track option:selected');
        track = track.text();
        //This is the function to change the task dropdown based on the track dropdown
        $.get('/TRECapp/relevant-tasks/', {selected_track: track}, function(data) {
            $('#id_task').find('option').remove().end()
            $('#id_task').append(data);
        });
        //This is the function to update the track table with the relevant info
        $.get('/TRECapp/track-task-info/', {selected_track: track}, function(data) {
            $('#submit-track-table').empty();
            $('#submit-track-table').append(data);


            var task = $('#id_task option:selected');
            task = task.text();
            $.get('/TRECapp/track-task-info/', {selected_task: task}, function(data) {
                $('#submit-task-table').empty();
                $('#submit-task-table').append(data);
            });//end task get


        });//end track get

    });//end select #id_track

    $('#id_task').change(function() {
        var task = $('#id_task option:selected');
        task = task.text();
        $.get('/TRECapp/track-task-info/', {selected_task: task}, function(data) {
            $('#submit-task-table').empty();
            $('#submit-task-table').append(data);
        });//end task get
    });//end select #id_task


});