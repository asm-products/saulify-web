javascript: function saulify() {
    var e = document;
    try {
        if (!e.body) throw 0;
        window.location = "https://saulify.me/clean?u=" + encodeURIComponent(e.location.href)
    } catch (t) {
        alert("Saul politely asks that you please wait until the page has loaded.")
    }
}
saulify();
void 0