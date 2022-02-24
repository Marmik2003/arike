$("#filter_form").submit(function(e) {
    e.preventDefault();
    console.log('filter');
    const ward = $("#input-ward").val();
    const kind = $("#input-kind").val();
    let params = parseURLParams();
    params.page = 1;
    if (ward.trim() !== '') {
        params.ward = ward;
    } else {
        delete params.ward;
    }
    params.kind = kind;
    window.location.href = window.location.href.split('?')[0] + '?' + joinParam(params);
});
