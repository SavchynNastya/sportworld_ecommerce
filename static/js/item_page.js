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

(function () {
  const itemCard = document.querySelector(".item__page__item__full-info");
    console.log(itemCard);
    const likeItemButton = itemCard.querySelector(".item-page__add__to__liked");
    likeItemButton.addEventListener("click", () => {
      const itemId = itemCard.dataset.id;
      console.log(itemId);

    fetch(`/add-to-liked/${itemId}`)
      .then((response) => response.json())
      .then((data) => {
        let likeButtonIcon = likeItemButton.querySelector(".item-page-like");
        console.log(data);
        if (data.liked) {
          likeButtonIcon.src = "../static/img/svg/heart_item-page-liked.svg";
        } else {
          likeButtonIcon.src = "../static/img/svg/heart_item-page.svg";
        }

        if (window.location.href.includes("/liked/")) {
          window.location.reload();
        }
      })
      .catch((error) => console.error(error));
  });
})();