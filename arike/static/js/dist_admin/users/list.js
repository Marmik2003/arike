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

$("#filter_form").submit(function(e) {
    e.preventDefault();
    const ward = $("#input-ward").val();
    const facility = $("#input-facility").val();
    let params = parseURLParams();
    params.page = 1;
    if (ward.trim() !== '') {
        params.ward = ward;
    } else {
        delete params.ward;
    }
    params.facility = facility;
    params.role = $("#input-role").val();
    window.location.href = window.location.href.split('?')[0] + '?' + joinParam(params);
});
