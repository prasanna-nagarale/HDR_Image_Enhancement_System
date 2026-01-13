document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.querySelector('input[type="file"]');
    const preview = document.getElementById('preview');

    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        fileInput.files = e.dataTransfer.files;
        previewFile(fileInput.files[0]);
    });

    fileInput.addEventListener('change', () => {
        previewFile(fileInput.files[0]);
    });

    function previewFile(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = `<img src="${e.target.result}" class="preview-img">`;
        };
        reader.readAsDataURL(file);
    }
});
