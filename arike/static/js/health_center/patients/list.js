$("#filter_form").submit(function(e) {
    e.preventDefault();
    const facility = $("#input-facility").val();
    let params = parseURLParams();
    params.page = 1;
    params.facility = facility;
    window.location.href = window.location.href.split('?')[0] + '?' + joinParam(params);
});
