var circle = $("<span>").css({
    "z-index": 99,
    "background-color": "#3f51b5",
    "border-radius": "50%",
    position: "absolute",
    right: 61,
    bottom: 34
});
function waitAnimation() {
    $(".account-panel").append(circle.css({
        width: 0,
        height: 0,
        "margin-right": 0,
        "margin-bottom": 0
    }).animate({
        width: 1000,
        height: 1000,
        "margin-right": -500,
        "margin-bottom": -500
    }, 500, "swing", function() {
        $(this).detach();
    }));
}
function doneAnimation() {
    $(".account-panel").append(circle.css({
        width: 1000,
        height: 1000,
        "margin-right": -500,
        "margin-bottom": -500
    }).animate({
        width: 0,
        height: 0,
        "margin-right": 0,
        "margin-bottom": 0
    }, 500, "swing", function() {
        $(this).detach();
    }));
}
