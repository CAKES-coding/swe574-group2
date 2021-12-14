let abstractText = document.getElementById("abstract-text");
let tagPieceButton = document.getElementById("tag-piece-button");

let startIndex = 0;
let endIndex = 0;
let selectedText = "";

abstractText.addEventListener("mouseup", () => {
    if (window.getSelection) {
        let selection = window.getSelection()
        selectedText = selection.toString();
        if (selection.anchorOffset < selection.focusOffset) {
            startIndex = selection.anchorOffset;
            endIndex = selection.focusOffset;
        } else {
            startIndex = selection.focusOffset;
            endIndex = selection.anchorOffset;
        }
    }
})

document.addEventListener("click", () => {
    document.getElementById("tagContextMenu").style.display = "none";
})

document.addEventListener("contextmenu", () => {
    document.getElementById("tagContextMenu").style.display = "none";
})

abstractText.addEventListener("contextmenu", (e) => {
    e.stopPropagation();
    e.preventDefault();
    rightClick(e);
    return false;
}, false);

rightClick = (e) => {
    let tagContextMenu = document.getElementById("tagContextMenu");
    tagContextMenu.style.display = "block";
    tagContextMenu.style.left = e.clientX + window.pageXOffset + "px";
    tagContextMenu.style.top = e.clientY + window.pageYOffset + "px";
}

tagPieceButton.addEventListener("click", () => {
    console.log(startIndex);
    console.log(endIndex);
    document.getElementById("tagContextMenu").style.display = "none";
    document.getElementById("fragment_info").style.display = "block";
    document.getElementById("fragment_text").value = selectedText;
    document.getElementById("fragment_start_index").value = startIndex;
    document.getElementById("fragment_end_index").value = endIndex;
    highlightAbstract(startIndex, endIndex);
    startIndex = 0;
    endIndex = 0;
})

function highlightAbstract(startInd, endInd) {
    let abstract = document.getElementById("abstract-text");
    let abstractInnerHTML = abstract.innerText;
    if (startInd >= 0) {
        abstractInnerHTML = abstractInnerHTML.substring(0, startInd) + "<span class='abstract_highlight'>" + abstractInnerHTML.substring(startInd, endInd) + "</span>" + abstractInnerHTML.substring(endInd);
        abstract.innerHTML = abstractInnerHTML;
    }
}

function unHighlightAbstract() {
    let abstract = document.getElementById("abstract-text");
    abstract.innerHTML = abstract.innerText;
}

let tagRows = document.getElementsByClassName('tag_row');

for (let i = 0; i < tagRows.length; i++) {
    tagRows[i].addEventListener("mouseover", function (event) {
        highlightAbstract(tagRows[i].dataset.start, tagRows[i].dataset.end);
    });
    tagRows[i].addEventListener("mouseout", function () {
        unHighlightAbstract();
    })
}

function upVote(tagRelationId) {
    sendVoteRequest('/wikode/upVote/', tagRelationId)
}

function downVote(tagRelationId) {
    sendVoteRequest('/wikode/downVote/', tagRelationId)
}

function sendVoteRequest(url, tagRelationId) {
    let token = document.getElementsByName("csrfmiddlewaretoken")[0].value
    $.ajax({
        url: url,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: token,
            tagRelationId: tagRelationId
        },
        success: function (voteSum) {
            document.getElementById("totalVotes-" + tagRelationId).innerHTML = voteSum["voteSum"];
        }
    })
}




