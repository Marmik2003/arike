$("#input-ward").change(function() {
    var ward_id = $(this).val();
    $.ajax({
        url: '/district_admin/users/get_facility_from_ward/',
        type: 'GET',
        data: {
            'ward': ward_id
        },
        success: function(data) {
            $("#input-facility").html(data);
        }
    });
});
