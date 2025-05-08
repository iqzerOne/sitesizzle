$(function() {
    console.log("Инициализация автодополнения");
    var citiesUrl = $("#id_city").data("cities-url");
    $("#id_city").autocomplete({
        source: citiesUrl,
        minLength: 1,
        response: function(event, ui) {
            console.log("Получены данные:", ui.content);
        },
        select: function(event, ui) {
            event.preventDefault();
            $("#id_city").val(ui.item.label);
            $("#id_city_id_hide").val(ui.item.value);
            console.log($("#id_city_id_hide").val(ui.item.value));
            console.log("Выбран город:", ui.item.label, "с id:", ui.item.value);
        },
        focus: function(event, ui) {
            event.preventDefault();
            $("#id_city").val(ui.item.label);
        }
    });
});

input_phone = document.getElementById("id_number_phone")
input_phone.addEventListener("input", function() {
    let clean_text = input_phone.value.replace(/[\(\)\-\s]/g, "")

    if (/^\d/.test(clean_text)){
        input_phone.value = "+7" + clean_text.slice(0)
    }
    if (clean_text.length <= 5){
        input_phone.value = input_phone.value.slice(0,2) +clean_text.substring(2,5)
    }
    if (clean_text.length > 5){
        input_phone.value = clean_text.slice(0,2)+ "(" + clean_text.substring(2,5) + ")"
    }
    if (clean_text.substring(5,8).length > 0){
        input_phone.value = input_phone.value.slice(0,7)+" "+clean_text.substring(5,8) 
    }
    if (clean_text.substring(8,10).length > 0){
        input_phone.value = input_phone.value.slice(0,13)+"-"+clean_text.substring(8,10) 
    } 
    if (clean_text.substring(10,12).length > 0){
        input_phone.value = input_phone.value.slice(0,19)+"-"+clean_text.substring(10,12) 
    } 
})