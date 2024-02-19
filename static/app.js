
const api_url = "http://www.omdbapi.com/?apikey=b3726a50&";


$("body").on("click", ".movie-info", function () {
    const event = this

    console.log(this);

    $(".row").text("");
    $(this).width(600)
    $(".row").html(event).addClass("movie-center");

    $(".heading b").html("<b>Sign Up/Log In</b> to search for a specific movie and/or add a movie to a list");
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
