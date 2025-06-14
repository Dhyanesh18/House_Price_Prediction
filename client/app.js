function getBathValue() {
    var uiBathrooms = document.getElementsByName("uiBathrooms");
    for(var i = 0; i < uiBathrooms.length; i++) {
        if(uiBathrooms[i].checked) {
            return parseInt(uiBathrooms[i].value);
        }
    }
    return 1; // Default value
}

function getBHKValue() {
    var uiBHK = document.getElementsByName("uiBHK");
    for(var i = 0; i < uiBHK.length; i++) {
        if(uiBHK[i].checked) {
            console.log(6-parseInt(uiBHK[i].value))
            return 6 - parseInt(uiBHK[i].value);
        }
    }
    return 5; // Default value
}

function showError(message) {
    var estPrice = document.getElementById("uiEstimatedPrice");
    estPrice.innerHTML = `<h2 style="color:red">Error: ${message}</h2>`;
}

function onClickedEstimatePrice() {
    var sqft = document.getElementById("uiSqft");
    var bhk = getBHKValue();
    var bathrooms = getBathValue();
    var location = document.getElementById("uiLocations");
    var estPrice = document.getElementById("uiEstimatedPrice");

    // Basic validation
    if (!sqft.value || isNaN(sqft.value) || parseFloat(sqft.value) <= 0) {
        showError("Please enter valid square footage (greater than 0)");
        return;
    }

    // Fixed validation - check if no location is selected or default option is selected
    if (!location.value || location.value === "" || location.value === "Choose a Location") {
        showError("Please select a location");
        return;
    }

    // Show loading state
    estPrice.innerHTML = "<h2>Calculating...</h2>";

    $.ajax({
        url: "/predict_home_price",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            total_sqft: parseFloat(sqft.value),
            bhk: bhk,
            bath: bathrooms,
            location: location.value
        }),
        success: function(data) {
            if (data.error) {
                showError(data.error);
            } else {
                estPrice.innerHTML = `<h2>₹${data.estimated_price} Lakh</h2>`;
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error:", xhr.responseText);
            if (xhr.responseJSON && xhr.responseJSON.error) {
                showError(xhr.responseJSON.error);
            } else {
                showError("Server error: " + error);
            }
        }
    });
}

function onPageLoad() {
    $.ajax({
        url: "/get_location_names",
        method: "GET",
        success: function(data) {
            if (data.locations) {
                var uiLocations = document.getElementById("uiLocations");
                $('#uiLocations').empty();
                $('#uiLocations').append(new Option("Choose a Location", "", true, true));
                
                data.locations.forEach(function(location) {
                    $('#uiLocations').append(new Option(location, location));
                });
                
                console.log("Locations loaded successfully:", data.locations.length);
            } else {
                console.error("No locations data received");
            }
        },
        error: function(xhr, status, error) {
            console.error("Failed to load locations:", error);
            showError("Failed to load locations from server");
        }
    });
}

window.onload = onPageLoad;