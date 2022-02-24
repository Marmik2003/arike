$("#next_page").click(function() {
    var first_name = $("#id_first_name").val();
    var last_name = $("#id_last_name").val();
    var email = $("#id_email").val();
    var phone_number = $("#id_phone_number").val();
    if (first_name == "" || last_name == "" || email == "" || phone_number == "") {
        toastr.warning("Warning", "Please fill all the fields");
    } else {
        $("#form_1").removeClass("block").addClass("hidden");
        $("#form_2").removeClass("hidden").addClass("block");
    }
});
$("#prev_page").click(function() {
    $("#form_1").removeClass("hidden").addClass("block");
    $("#form_2").removeClass("block").addClass("hidden");
});

$("#ward_id").change(function() {
    var ward_id = $(this).val();
    $.ajax({
        url: '/district_admin/users/get_facility_from_ward/',
        type: 'GET',
        data: {
            'ward': ward_id,
            'get_id': 'facility_id'
        },
        success: function(data) {
            $("#id_facility").html(data);
        }
    });
});

