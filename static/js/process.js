document.addEventListener("DOMContentLoaded", () => {
    const dropArea = document.getElementById("drop-area");
    const fileElem = document.getElementById("fileElem");
    const uploadForm = document.getElementById("upload-form");
    const errorMsg = document.getElementById("error-message");
    const loader = document.getElementById("loader");
    const dropIcon = document.getElementById("drop-icon");
    const fileCounter = document.getElementById("file-counter");

    let selectedFiles = [];

    const showLoader = () => {
        loader.hidden = false;
        loader.classList.add("fade-in");
    };

    const hideLoader = () => {
        loader.hidden = true;
    };

    const showError = (message) => {
        errorMsg.textContent = message;
        errorMsg.classList.add("shake");
        setTimeout(() => errorMsg.classList.remove("shake"), 500);
        hideLoader();
    };

    const clearError = () => {
        errorMsg.textContent = "";
    };

    const updateFileCounter = () => {
        if (fileCounter) {
            fileCounter.textContent = selectedFiles.length > 0 ? `${selectedFiles.length} files selected` : "";
            fileCounter.style.display = selectedFiles.length > 0 ? "block" : "none";
        }
    };

    const isValidImage = (file) => {
        const name = file.name.toLowerCase();
        return (
            file.type.startsWith("image/") ||
            name.endsWith(".dng") ||
            name.endsWith(".arw") ||
            name.endsWith(".nef") ||
            name.endsWith(".cr2")
        );
    };

    const setFiles = (files) => {
        const validFiles = Array.from(files).filter(isValidImage);
        selectedFiles = validFiles;

        const dt = new DataTransfer();
        validFiles.forEach(file => dt.items.add(file));
        fileElem.files = dt.files;

        updateFileCounter();

        if (selectedFiles.length >= 3) {
            dropArea.classList.add("files-added");
            clearError();
        } else {
            dropArea.classList.remove("files-added");
            showError("Please select at least 4 valid images.");
        }
    };

    // Handle file input change (Browse)
    fileElem.addEventListener("change", () => {
        setFiles(fileElem.files);
    });

    // Handle form submit
    uploadForm.addEventListener("submit", (e) => {
        if (!selectedFiles || selectedFiles.length < 4) {
            e.preventDefault();
            showError("Please select at least 4 images.");
            dropArea.classList.add("error-shake");
            setTimeout(() => dropArea.classList.remove("error-shake"), 500);
        } else {
            clearError();
            showLoader();
            const rotatingCircle = document.querySelector(".rotating-circle");
            if (rotatingCircle) {
                rotatingCircle.classList.add("processing");
            }
        }
    });

    // Drag and drop logic
    ["dragenter", "dragover"].forEach(eventName => {
        dropArea.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropArea.classList.add("highlight");
            if (dropIcon) dropIcon.classList.add("bounce");
        });
    });

    ["dragleave", "drop"].forEach(eventName => {
        dropArea.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropArea.classList.remove("highlight");
            if (dropIcon) dropIcon.classList.remove("bounce");
        });
    });

    dropArea.addEventListener("drop", (e) => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        setFiles(files);
    });

    // Clicking drop area opens file dialog
    dropArea.addEventListener("click", (e) => {
        if (e.target !== fileElem) {
            fileElem.click();
        }
    });

    // Preload image logic
    window.addEventListener("load", () => {
        document.querySelectorAll(".preload").forEach(img => {
            const src = img.getAttribute("data-src");
            if (src) img.src = src;
        });
        document.body.classList.add("page-loaded");
    });

    // Optional: Particle effects
    if (typeof initParticles === 'function') {
        initParticles();
    }
});
