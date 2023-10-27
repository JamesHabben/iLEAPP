// This function saves the theme choice to localStorage when the switch is toggled.
// This code should live on your settings page.
$(document).ready(function() {
    var darkSwitch = document.getElementById("darkSwitch");
    if (darkSwitch) {
        // Check localStorage and update the switch's state
        var darkThemeSelected = localStorage.getItem("darkSwitch") === "dark";
        darkSwitch.checked = darkThemeSelected;

        darkSwitch.addEventListener("change", function(event) {
            if (darkSwitch.checked) {
                localStorage.setItem("darkSwitch", "dark");

            } else {
                localStorage.removeItem("darkSwitch");
            }
            applyTheme();
        });
    }
});

// This function applies the theme choice from localStorage.
// This code should live on all pages, or in a script file that's included on all pages.
function applyTheme() {
    var darkThemeSelected =
        localStorage.getItem("darkSwitch") !== null &&
        localStorage.getItem("darkSwitch") === "dark";
    darkThemeSelected
        ? document.body.setAttribute("data-theme", "dark")
        : document.body.removeAttribute("data-theme");
}

// Call applyTheme on page load to set the theme based on localStorage.
//$(document).ready(function() {
    applyTheme();
//});
