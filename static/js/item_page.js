const descHeadings = document.querySelectorAll(
  ".item-page__item__desc-heading"
);

descHeadings.forEach((descHeading) => {
    descHeading.addEventListener("click", () => {
        const description = document.querySelector(
          ".item-page__item__desc-text"
        );

        if (description.style.display === "none") {
        description.style.display = "block";
        descHeading.querySelector(".item-page__tick").classList.add("rotate");
        } else {
        description.style.display = "none";
        descHeading.querySelector(".item-page__tick").classList.remove("rotate");
        }
    });
});


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

function likeItemPage(){
  const likeButton = document.querySelector(
    ".item-page__add__to__liked"
  );
  likeButton.addEventListener("click", () => {
    const likeIcon = likeButton.querySelector(".item-page-like");
    if(likeIcon.src.includes("/img/svg/heart_item-page.svg")) {
      likeIcon.src = "img/svg/heart_item-page-liked.svg";
    } else {
      likeIcon.src = "img/svg/heart_item-page.svg";
    }
  });
}