function parseURLParams() {
    const url = window.location.href;
    let queryStart = url.indexOf("?") + 1,
        queryEnd = url.indexOf("#") + 1 || url.length + 1,
        query = url.slice(queryStart, queryEnd - 1),
        pairs = query.replace(/\+/g, " ").split("&"),
        parms = {}, i, n, v, nv;
    if (query === url || query === "") return [];

    for (i = 0; i < pairs.length; i++) {
        nv = pairs[i].split("=", 2);
        n = decodeURIComponent(nv[0]);
        v = decodeURIComponent(nv[1]);

        if (!parms.hasOwnProperty(n)) parms[n] = [];
        parms[n].push(nv.length === 2 ? v : null);
    }

    return parms;
}

function joinParam(object) {
    var parameters = [];
    for (var property in object) {
        if (object.hasOwnProperty(property)) {
            parameters.push(encodeURI(property + '=' + object[property]));
        }
    }

    return parameters.join('&');
}

function changePage(page_no) {
    let params = parseURLParams();
    params.page = page_no;
    window.location.href = window.location.href.split('?')[0] + '?' + joinParam(params);
}

function searchQuery() {
    let params = parseURLParams();
    params.page = 1;
    console.log('searching');
    params.query = $('#search_query').val();
    window.location.href = window.location.href.split('?')[0] + '?' + joinParam(params);
}


