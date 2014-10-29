window.saulify = typeof window.saulify !== "object" ? {} : window.saulify;
window.saulify.bookmarklet = (function() {
    var baseUrl = 'http://saulify.me',
        saulifyUrl = baseUrl + '/articles/show'

    function init() {
        document.location = saulifyUrl + '?url_to_clean=' + encodeURIComponent(window.location.href);
        return false;
    }
    return {
        "init": init
    };
}());
window.saulify.bookmarklet.init();