document.addEventListener("DOMContentLoaded", function () {
    var toggleBtn = document.getElementById("theme-toggle");

    if (!toggleBtn) return;

    var icon = toggleBtn.querySelector("i");
    var label = toggleBtn.querySelector(".theme-toggle-text");

    function updateIcon(theme) {
        if (icon) {
            icon.classList.toggle("fa-sun", theme === "light");
            icon.classList.toggle("fa-moon", theme !== "light");
        }
        if (label) {
            label.textContent = theme === "light" ? "Light" : "Dark";
        }
    }

    updateIcon(document.documentElement.getAttribute("data-theme") || "dark");

    toggleBtn.addEventListener("click", function () {
        var current = document.documentElement.getAttribute("data-theme") || "dark";
        var next = current === "light" ? "dark" : "light";

        document.documentElement.setAttribute("data-theme", next);
        localStorage.setItem("theme", next);
        updateIcon(next);
    });
});

document.addEventListener("DOMContentLoaded", function () {
    if (typeof Quill === "undefined") return;

    var textareas = document.querySelectorAll("textarea[data-richtext]");

    textareas.forEach(function (textarea) {
        var container = document.createElement("div");
        container.innerHTML = textarea.value;
        textarea.parentNode.insertBefore(container, textarea);
        textarea.style.display = "none";

        var quill = new Quill(container, {
            theme: "snow",
            modules: {
                toolbar: [
                    ["bold", "italic", "underline"],
                    [{ header: [2, 3, false] }],
                    [{ list: "ordered" }, { list: "bullet" }],
                    ["link", "blockquote"],
                    ["clean"]
                ]
            }
        });

        var form = textarea.closest("form");
        if (form) {
            form.addEventListener("submit", function () {
                textarea.value = quill.root.innerHTML;
            });
        }
    });
});
