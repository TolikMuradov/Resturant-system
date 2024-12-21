const numbers = document.querySelectorAll('.numbers div');
    const images = document.querySelectorAll('.slider img');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    let currentIndex = 0;
    let interval;

    function changeSlide(index) {
        images[currentIndex].classList.remove('active');
        numbers[currentIndex].classList.remove('active');

        currentIndex = index;

        images[currentIndex].classList.add('active');
        numbers[currentIndex].classList.add('active');
    }

    function autoSlide() {
        interval = setInterval(() => {
            let nextIndex = (currentIndex + 1) % images.length;
            changeSlide(nextIndex);
        }, 3000);
    }

    function goToPrev() {
        clearInterval(interval);
        let prevIndex = (currentIndex - 1 + images.length) % images.length;
        changeSlide(prevIndex);
        autoSlide();
    }

    function goToNext() {
        clearInterval(interval);
        let nextIndex = (currentIndex + 1) % images.length;
        changeSlide(nextIndex);
        autoSlide();
    }

    numbers.forEach((number, index) => {
        number.addEventListener('click', () => {
            clearInterval(interval);
            changeSlide(index);
            autoSlide();
        });
    });

    prevButton.addEventListener('click', goToPrev);
    nextButton.addEventListener('click', goToNext);

    autoSlide();

