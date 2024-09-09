
const api_url = "http://www.omdbapi.com/?apikey=b3726a50&";


$("body").on("click", ".movie-poster", function () {
    const event = this;

    $(".container").html("")
    $(this).width(600)
        .addClass("movie-home")
        // .removeClass("movie-poster");
    $(".container")
        .append("<h1><b>Sign Up/Log In</b> to search for a specific movie and/or add a movie to a list</h1>")
        .append(event);

    console.log(this);
});


async function getMovie(s, api_url) {
    const result = await axios.get(api_url, { params: { s } });
    return result.data;
}


async function addMovie(term, func) {
    const searchTerm = await func(term);
    $("#imagesContainer").append(`<img src="${searchTerm}" class="img-thumbnail">`);
}


$("form").on("click", "#btn-danger", function (e) {
    e.preventDefault();
    $("#imagesContainer").html("");
});

// window.addEventListener("pageshow", function (event) {
//     var perfEntries = performance.getEntriesByType("navigation");
//     if (perfEntries[0].type === "back_forward") {
//         location.reload();
//     }
// });