function startProgress() {
    let progressBar = document.getElementById("myProgressBar");
    let width = 1;
    let interval = setInterval(frame, 10);

    function frame() {
        if (width >= 100) {
            clearInterval(interval);
        } else {
            width++;
            progressBar.style.width = width + "%";
        }
    }
}
