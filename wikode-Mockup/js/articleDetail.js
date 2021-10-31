// Tag upvote/downvote Logic

var isUpvoted = false;
var isDownvoted = false;

// Upvote
function incrementValue() {
    var upvoteNumberText = document.getElementById('totalVotes').innerText;
    console.log(upvoteNumberText)
    var upvoteNumber = parseInt(upvoteNumberText);
    console.log(upvoteNumber)

    if (isUpvoted) {
        upvoteNumber -= 1;
        isUpvoted = false
    } else {
        upvoteNumber += 1;
        isUpvoted = true
    }

    document.getElementById('totalVotes').innerText = upvoteNumber;
}

// Downvote
function decrementValue() {
    var downvoteNumberText = document.getElementById('totalVotes').innerText;
    console.log(downvoteNumberText)
    var downvoteNumber = parseInt(downvoteNumberText);
    console.log(downvoteNumber)

    if (isDownvoted) {
        downvoteNumber += 1;
        isDownvoted = false
    } else {
        downvoteNumber -= 1;
        isDownvoted = true
    }

    document.getElementById('totalVotes').innerText = downvoteNumber;
}