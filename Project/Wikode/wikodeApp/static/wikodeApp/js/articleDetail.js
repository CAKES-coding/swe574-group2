let abstractText = document.getElementById("abstract-text");
let tagPieceButton = document.getElementById("tag-piece-button");
let freeTagButton = document.getElementById("free-tag-piece-button");
let cancelWikitagButton = document.getElementById("cancel-wikitag");
let cancelFreeButton = document.getElementById("cancel-freetag");
let cancelWikiButton = document.getElementById("cancel-wikientry");
let clearFragmentButton = document.getElementById("clear-fragment-button")
let startIndex = 0;
let endIndex = 0;
let selectedText = "";

function openWikiForm() {
    document.getElementById("wikitag_form").style.display = "block";
}

function closeWikiForm() {
    document.getElementById("wikitag_form").style.display = "none";
}

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

let fragmentInfoGroupDiv = document.getElementById("fragment_info")
let fragmentTextLabel = document.getElementById("fragment_text")
let fragmentStartIndexInput = document.getElementById("fragment_start_index")
let fragmentEndIndexInput = document.getElementById("fragment_end_index");

tagPieceButton.addEventListener("click", () => {
    console.log(startIndex);
    console.log(endIndex);
    document.getElementById("wikientry_form").hidden = false;
    document.getElementById("tagContextMenu").style.display = "none";
    document.getElementById("fragment_text").value = selectedText;
    if (startIndex === endIndex) {
        document.getElementById("fragment_info").style.display = "none";
    } else {
        document.getElementById("fragment_info").style.display = "block";
        document.getElementById("fragment_start_index").value = startIndex;
        document.getElementById("fragment_end_index").value = endIndex;
        highlightAbstract(startIndex, endIndex);
    }
    startIndex = 0;
    endIndex = 0;
})

cancelWikiButton.addEventListener("click", () => {
    document.getElementById("wikientry_form").hidden = true;
    document.getElementById("fragment_text").value = "";
    document.getElementById("fragment_start_index").value = 0;
    document.getElementById("fragment_end_index").value = -1;
    unHighlightAbstract();
    startIndex = 0;
    endIndex = 0;
})

freeTagButton.addEventListener("click", () => {
    console.log(startIndex);
    console.log(endIndex);
    document.getElementById("free_tag_form").hidden = false;
    document.getElementById("tagContextMenu").style.display = "none";
    document.getElementById("free_tag_fragment_info").style.display = "block";
    document.getElementById("free_fragment_text").value = selectedText;
    if (startIndex === endIndex) {
        document.getElementById("free_tag_fragment_info").style.display = "none";
    } else {
        document.getElementById("free_tag_fragment_info").style.display = "block";
        document.getElementById("free_fragment_start_index").value = startIndex;
        document.getElementById("free_fragment_end_index").value = endIndex;
        highlightAbstract(startIndex, endIndex);
    }
    startIndex = 0;
    endIndex = 0;
})

cancelFreeButton.addEventListener("click", () => {
    document.getElementById("free_tag_form").hidden = true;
    document.getElementById("free_fragment_text").value = "";
    document.getElementById("free_fragment_start_index").value = 0;
    document.getElementById("free_fragment_end_index").value = -1;
    unHighlightAbstract();

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
    tagRows[i].addEventListener("mouseover", function () {
        highlightAbstract(tagRows[i].dataset.start, tagRows[i].dataset.end);
    });
    tagRows[i].addEventListener("mouseout", function () {
        unHighlightAbstract();
    })
}

function upVote(tagRelationId) {
    sendVoteRequest(tagRelationId, "upVote")
}

function downVote(tagRelationId) {
    sendVoteRequest(tagRelationId, "downVote")
}

function sendVoteRequest(tagRelationId, voteType) {
    let token = document.getElementsByName("csrfmiddlewaretoken")[0].value
    $.ajax({
        url: '/wikode/vote/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: token,
            tagRelationId: tagRelationId,
            voteType: voteType
        },
        success: function (vote) {
            document.getElementById("totalVotes-" + tagRelationId).innerHTML = vote["voteSum"];
            let userVote = vote["userVote"]
            adjustVoteButtonColor(userVote, tagRelationId)
        }
    })
}

function getTagRelationIds() {
    let tagRelationIds = [];
    let tagRows = document.getElementsByClassName("tag_row");
    for (let i = 0; i < tagRows.length; i++) {
        tagRelationIds[i] = parseInt(tagRows[i].id);
    }
    return tagRelationIds
}

window.onload = function () {
    let token = document.getElementsByName("csrfmiddlewaretoken")[0].value
    let tagRelationIds = getTagRelationIds().toString();
    if  (tagRelationIds) {
        $.ajax({
        url: '/wikode/vote/',
        type: 'GET',
        data: {
            csrfmiddlewaretoken: token,
            tagRelationIds: tagRelationIds
        },
        success: function (userVoteDict) {
            userVoteDict = userVoteDict['userVoteDict']
            for (let tagRelationId in userVoteDict) {
                adjustVoteButtonColor(userVoteDict[tagRelationId], tagRelationId)
            }
        }})
    }
}

function adjustVoteButtonColor(userVote, tagRelationId) {
    let upvoteButton = document.getElementById("upvote-button-" + tagRelationId);
    let downvoteButton = document.getElementById("downvote-button-" + tagRelationId);
    if (userVote === 1) {
        upvoteButton.className = "btn btn-primary";
        downvoteButton.className = "btn btn-outline-danger";
    } else if (userVote === 0) {
        upvoteButton.className = "btn btn-outline-primary";
        downvoteButton.className = "btn btn-outline-danger";
    } else if (userVote === -1) {
        upvoteButton.className = "btn btn-outline-primary";
        downvoteButton.className = "btn btn-danger";
    }
}

// Reload the page when visited via browser go back button
window.addEventListener("pageshow", function (event) {
    let navigationType = window.performance.getEntriesByType("navigation")[0].type
    console.log(navigationType)
    let historyTraversal = event.persisted ||
        (typeof window.performance != "undefined" &&
            navigationType === "back_forward");
    if (historyTraversal) {
        window.location.reload();
    }
});

cancelWikitagButton.addEventListener("click", () => {
    document.getElementById("wikitag_form").hidden = true;
    document.getElementById("fragment_text").value = "";
    document.getElementById("fragment_start_index").value = 0;
    document.getElementById("fragment_end_index").value = -1;
    unHighlightAbstract();
    startIndex = 0;
    endIndex = 0;
})
