(function () {
    const inputQuantity = document.querySelector(".items__quantity-input");
    const increaseQuantityBtn = document.querySelector(".increase");
    const decreaseQuantityBtn = document.querySelector(".decrease");

    increaseQuantityBtn.addEventListener("click", function () {
      inputQuantity.value = parseInt(inputQuantity.value) + 1;
    });

    decreaseQuantityBtn.addEventListener("click", function () {
        if (parseInt(inputQuantity.value) > 1) {
            inputQuantity.value = parseInt(inputQuantity.value) - 1;
        }
    });
})();

(function () {
  const likeItemButton = document.querySelectorAll(".like__item-button");
  likeItemButton.forEach((likeButton) => {
    likeButton.addEventListener("click", () => {
      let likeButtonIcon = likeButton.querySelector(".like__item");
      console.log(likeButtonIcon);
      if (likeButtonIcon.src.includes("/img/svg/item_liked.svg")) {
        likeButtonIcon.src = "img/svg/item_like.svg";
      } else {
        likeButtonIcon.src = "img/svg/item_liked.svg";
      }
    });
  });
})();

(function () {
  const burgerItem = document.querySelector(".burger");
  const menu = document.querySelector(".nav__links");
  const menuCloseItem = document.querySelector(".header__nav-close");
  const menuLinks = document.querySelectorAll(".header__link");
  // const hiddenLinks = document.querySelectorAll(".hidden__link");
  burgerItem.addEventListener("click", () => {
    menu.classList.add("header__nav_active");
    // hiddenLinks.forEach((link) => {
    //   // link.classList.add("hidden__link_active");
    // });
  });
  menuCloseItem.addEventListener("click", () => {
    menu.classList.remove("header__nav_active");
  });
  // if (window.innerWidth < 768) {
  for (let i = 0; i < menuLinks.length; i += 1) {
    menuLinks[i].addEventListener("click", () => {
      menu.classList.remove("header__nav_active");
    });
  }
  // }
})();