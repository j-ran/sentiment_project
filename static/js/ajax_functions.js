"use strict";
console.log('AJAX functions functioning')

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