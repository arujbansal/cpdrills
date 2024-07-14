window.onload = function () {
    let seconds = 0;
    let hours = 0;
    let tens = 0;
    let minutes = 0;
    let appendTens = 0;
    let appendSeconds = document.getElementById("seconds")
    let appendMinutes = document.getElementById("minutes")
    let appendHours = document.getElementById("hours")
    let buttonStart = document.getElementById('button-start');
    let buttonStop = document.getElementById('button-stop');
    let buttonReset = document.getElementById('button-reset');
    let problemLink = document.getElementById('problem_url');
    let Interval;
    let running = false;
    let clicked_before = false;

    problemLink.onclick = function () {
        if (clicked_before) return;
        clicked_before = true;

        buttonStart.click()
    }

    buttonStart.onclick = function () {
        clearInterval(Interval);
        Interval = setInterval(startTimer, 10);
        running = true;

        console.log("clicked")

        seconds = parseInt(document.getElementById("seconds").value);
        minutes = parseInt(document.getElementById("minutes").value);
        hours = parseInt(document.getElementById("hours").value);
    }

    buttonStop.onclick = function () {
        clearInterval(Interval);
        running = false;
    }

    buttonReset.onclick = function () {
        clearInterval(Interval);
        tens = 0;
        seconds = 0;
        minutes = 0;
        hours = 0;
        appendTens.value = "00";
        appendSeconds.value = "00";
        appendMinutes.value = "00";
        appendHours.value = "00";
    }

    function startTimer() {
        tens++;

        if (tens <= 9)
            appendTens.value = "0" + tens;

        if (tens > 9)
            appendTens.value = tens;

        if (minutes > 59) {
            hours++;
            appendHours.value = hours;
            minutes = 0;
            appendMinutes.value = "0" + 0;
        }

        if (seconds > 59) {
            minutes++;
            appendMinutes.value = minutes;
            seconds = 0;
            appendSeconds.value = "0" + 0;
        }

        if (tens > 99) {
            console.log("seconds");
            seconds++;
            appendSeconds.value = "0" + seconds;
            tens = 0;
            appendTens.value = "0" + 0;
        }

        if (seconds > 9) {
            appendSeconds.value = seconds;
        }

        if (minutes < 9) appendMinutes.value = "0" + minutes;
    }
}