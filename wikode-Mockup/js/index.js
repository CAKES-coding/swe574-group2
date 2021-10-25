//Prevent enter to submit search form
function checkEnter(e){
    e = e || event;
    var txtArea = /textarea/i.test((e.target || e.srcElement).tagName);
    return txtArea || (e.keyCode || e.which || e.charCode || 0) !== 13;
}
document.querySelector('.noEnter').onkeypress = checkEnter;

function myFunction() {
    $('#description').val('disease caused by infection of pathogenic biological agents in a host organism');
    $('#label').val('infectious disease');
}

$(document).ready(function () {
    $("#basicSearchButton").click(function () {
        $(".searchContainer").toggle();
    });

    // $("#checkURL").click(function () {
    //     $('#description').val('disease caused by infection of pathogenic biological agents in a host organism');
    //     $('#label').val('infectious disease');
    // });

});





// document.getElementById('tagModal').addEventListener('shown.mdb.modal', () => {
//     $('#label').val('infectious disease')
// })