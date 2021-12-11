followersList = JSON.parse(document.getElementById("followee_list").value);
followingsList = JSON.parse(document.getElementById("follower_list").value);

const followingsAnchor = document.getElementById("followings");
const followersAnchor = document.getElementById("followers")
const followModal = document.getElementById("followModal");
let modalBody = document.getElementById("modalBody");

followingsAnchor.addEventListener('click', (e) => {
    modalBody.innerHTML = "";
    showModal("Followings", followingsList);
})

followersAnchor.addEventListener('click', (e) => {
    modalBody.innerHTML = "";
    console.log()
    showModal("Followers", followersList);
})

// Show modal when called
const showModal = function(header, list) {
    followModal.style.display="block";

    let listTable = document.createElement("table");
    listTable.classList.add("table")
    listTable.classList.add("table-hover")

    let listTableBody = document.createElement("tbody");

    list.forEach(item => {

        let row = document.createElement("tr")
        let tdItem = document.createElement("td")

        let itemAnchor = document.createElement("a");
        itemAnchor.innerHTML = item[1]
        itemAnchor.href = item[0]
        tdItem.appendChild(itemAnchor)

        let tdButton = document.createElement("td")
        let button = getFollowButton()
        tdButton.appendChild(button)

        row.appendChild(tdItem)
        row.appendChild(tdButton)
        listTableBody.appendChild(row)
    })

    document.getElementById("modal-header-text").innerHTML = header;
    listTable.appendChild(listTableBody)
    modalBody.appendChild(listTable);
}

const getFollowButton = function () {
    const followButton = document.createElement("button");
    followButton.innerHTML = "Follow"
    followButton.classList.add("btn")
    followButton.classList.add("btn-primary")
    followButton.classList.add("btn-sm")
    return followButton
}

// Select modal close icon element
const closeSpan = document.getElementById("close");

// When the user clicks modal close icon, close modal
closeSpan.addEventListener('click', () => { followModal.style.display="none"; })

// When the user clicks anywhere outside of the modal, close modal
window.onclick = function(event) {
    if (event.target === followModal) {
        followModal.style.display="none";
    }
}

const taggedArticlesTab = document.getElementById("tagged-articles-id");
const recentActivitiesTab = document.getElementById("recent-activities-id");
const taggedArticles = document.getElementById("tagged-articles");
const recentActivities = document.getElementById("recent-activities");

taggedArticlesTab.addEventListener('click', () => {
    recentActivities.style.display = "none";
    recentActivitiesTab.className = recentActivitiesTab.className.replace("active", "");
    taggedArticlesTab.className += " active";
    taggedArticles.style.display = "block";
})

recentActivitiesTab.addEventListener('click', () => {
    taggedArticles.style.display = "none";
    taggedArticlesTab.className = taggedArticlesTab.className.replace("active", "");
    recentActivitiesTab.className += " active";
    recentActivities.style.display = "block";
})

const followButton = document.getElementById("follow-button");

followButton.addEventListener('click', () => {

    if (followButton.innerText === "Follow") {
        followButton.innerText = "Unfollow"
        followButton.classList.replace("btn-primary", "btn-danger")
    } else {
        followButton.innerText = "Follow"
        followButton.classList.replace("btn-danger", "btn-primary")
    }
})