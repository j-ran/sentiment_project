"use strict";
console.log('jQuery functions functioning')

// SORT THREE WAYS DIVS

$("#month-sort").on("click", () => {
    $("#month-form").show();
    $("#feeling-form").hide();
    $("#region-form").hide();
    $("#make-button").show();
})

$("#feeling-sort").on("click", () => {
    $("#month-form").hide();
    $("#feeling-form").show();
    $("#region-form").hide();
    $("#make-button").show();
})

$("#region-sort").on("click", () => {
    $("#month-form").hide();
    $("#feeling-form").hide();
    $("#region-form").show();
    $("#make-button").show();
})


// ADD PHRASE DIVS
$("#here-1a").on("click", () => {
    $("#here-1").show();
    $("#prelim-1").fadeIn("slow");
    $("#prelim-2").hide();
    $("#prelim-3").hide();
    $("#thinking-1").hide();
    $("#thinking-2").hide();
})

$("#prelim-1a").on("click", () => {
    $("#here-1").show();
    $("#prelim-1").show();
    $("#prelim-2").slideDown();
    $("#prelim-3").hide();
    $("#thinking-1").hide();
    $("#thinking-2").hide();
})

$("#prelim-2a").on("click", () => {
    $("#here-1").show();
    $("#prelim-1").show();
    $("#prelim-2").show();
    $("#prelim-3").slideDown();
    $("#thinking-1").hide();
    $("#thinking-2").hide();
})

$("#prelim-3a").on("click", () => {
    $("#here-1").show();
    $("#prelim-1").show();
    $("#prelim-2").show();
    $("#prelim-3").show();
    $("#thinking-1").fadeIn("slow");
    $("#thinking-2").hide();
})

$("#thinking-1a").on("click", () => {
    $("#here-1").hide();
    $("#prelim-1").hide();
    $("#prelim-2").hide();
    $("#prelim-3").hide();
    $("#thinking-1").hide();
    $("#thinking-2").fadeIn();
})