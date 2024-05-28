function startCountdown(duration, display) {
    let timer = duration, minutes, seconds;
    setInterval(() => {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = 0;
            display.textContent = "Desbloqueado";
        }
    }, 1000);
}

window.onload = () => {
    const countdownElement = document.querySelector('#countdown');
    const unlockTimeInMinutes = 5; 
    const unlockTimeInSeconds = unlockTimeInMinutes * 60;

    startCountdown(unlockTimeInSeconds, countdownElement);
};
