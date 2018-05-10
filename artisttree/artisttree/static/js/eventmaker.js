$(document).ready(function() {
    $('#eventdate').datepicker({format: 'yyyy-mm-dd',});
    $('#eventstart').timepicker({'timeFormat': 'g:i a', 'scrollDefault': 'now'});
    $('#eventend').timepicker({'timeFormat': 'g:i a', 'scrollDefault': 'now'});
});