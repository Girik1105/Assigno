const container = document.querySelector('.container');
const text = document.querySelector('.text');

const totalTime = 7500;
const breathTime = (totalTime/5) * 2;
const holdTime = totalTime/5;

function animation () {
    text.innerHTML = 'Breath in!';
    container.className = 'container grow';

    setTimeout(() => {
        text.innerHTML = 'Hold';
        
        setTimeout(() => {
            text.innerHTML = 'Breath Out!';
            container.className = 'container shrink';
        }, holdTime)

    }, breathTime)
}

animation();
setInterval(animation, totalTime);