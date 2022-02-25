$(document).ready(function () {
    $('input[name="kind"]').change(function () {
        console.log("changed");
        if ($(this).val() === 'phc') {
            $('#CHC_box').removeClass('hidden');
        } else {
            $('#CHC_box').addClass('hidden');
        }
    });
});
$("#id_ward").change(function() {
    var ward_id = $(this).val();
    $.ajax({
        url: '/district_admin/users/get_facility_from_ward/',
        type: 'GET',
        data: {
            'ward': ward_id,
            'get_chc': 'facility_id'
        },
        success: function(data) {
            $("#id_chc").html(data);
        }
    });
});
