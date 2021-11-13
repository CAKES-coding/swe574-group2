//Prevent enter to submit search form
function checkEnter(e) {
    e = e || event;
    var txtArea = /textarea/i.test((e.target || e.srcElement).tagName);
    return txtArea || (e.keyCode || e.which || e.charCode || 0) !== 13;
}

$(".tag_name").click(function () {
    $("#tag_name")[0].value = $(this).text();
})


$(".confirm_action").click(function () {
    let isValid = confirm('Are you sure ?');
    if (!isValid) {
        event.preventDefault();
    }
})

$(document).ready(function () {
    $("#basicSearchButton").click(function () {
        $(".searchContainer").toggle();
    });


});

document.querySelector('.noEnter').onkeypress = checkEnter;