(function () {
  const smoothScroll = function (targetEl, duration) {
    const headerElHeight = document.querySelector(".header").clientHeight;
    let target = document.querySelector(targetEl);
    let targetPosition = target.getBoundingClientRect().top - headerElHeight;
    let startPosition = window.pageYOffset;
    let startTime = null;

    const ease = function (t, b, c, d) {
      t /= d / 2;
      if (t < 1) return (c / 2) * t * t + b;
      t--;
      return (-c / 2) * (t * (t - 2) - 1) + b;
    };

    const animation = function (currentTime) {
      if (startTime === null) startTime = currentTime;
      const timeElapsed = currentTime - startTime;
      const run = ease(timeElapsed, startPosition, targetPosition, duration);
      window.scrollTo(0, run);
      if (timeElapsed < duration) requestAnimationFrame(animation);
    };
    requestAnimationFrame(animation);
  };

  const scrollTo = function () {
    const links = document.querySelectorAll(".js-scroll");
    links.forEach((each) => {
      each.addEventListener("click", function () {
        const currentTarget = this.getAttribute("href");
        smoothScroll(currentTarget, 1000);
      });
    });
  };
  scrollTo();
})();


(function () {
  const sliderItems = document.querySelector(".slider__wrapper");
  const prevButton = document.querySelector(".prev-button");
  const nextButton = document.querySelector(".next-button");

  let currentPosition = 0;

  function slide(direction) {
    const itemWidth = sliderItems.querySelector(".card").offsetWidth;

    let maxPosition;
    
    maxPosition = (sliderItems.children.length - 4) * itemWidth;

    if (window.innerWidth < 1200)
      maxPosition = (sliderItems.children.length - 3) * itemWidth;

    if (window.innerWidth < 850)
      maxPosition = (sliderItems.children.length - 2) * itemWidth;

    if(window.innerWidth < 620)
      maxPosition = (sliderItems.children.length - 1) * itemWidth;
      
    currentPosition += direction * itemWidth;
    console.log(
      window.innerWidth,
      maxPosition,
      sliderItems.children.length - 3,
      itemWidth
    );
    if (currentPosition > 0) {
      currentPosition = -maxPosition;
    } else if (currentPosition < -maxPosition) {
      currentPosition = 0;
    }
    sliderItems.style.transform = `translateX(${currentPosition}px)`;
  }

  prevButton.addEventListener("click", () => {
    slide(1);
  });

  nextButton.addEventListener("click", () => {
    slide(-1);
  });

})();


(function () {
  const itemCards = document.querySelectorAll(".main__item__card");
  // console.log(likeItemButton)
  itemCards.forEach((itemCard) => {
    console.log(itemCard);
    const likeItemButton = itemCard.querySelector(".main__like__item-button");
    likeItemButton.addEventListener("click", () => {
      const itemId = itemCard.dataset.id;
      console.log(itemId);

      fetch(`/add-to-liked/${itemId}`)
        .then((response) => response.json())
        .then((data) => {
          let likeButtonIcon = likeItemButton.querySelector(".like__item");
          console.log(data);
          if (data.liked) {
            likeButtonIcon.src = "static/img/svg/item_liked.svg";
          } else {
            likeButtonIcon.src = "static/img/svg/item_like.svg";
          }

          if (window.location.href.includes("/liked/")) {
            window.location.reload();
          }
        })
        .catch((error) => console.error(error));
    });
  });
})();