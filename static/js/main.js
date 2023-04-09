(function () {
  let slides = document.querySelectorAll(".slide");
  let dots = document.querySelectorAll(".dot");

  let index = 0;

  const activeSlide = (n) => {
    for (slide of slides) {
      slide.classList.remove("active__slide");
    }
    slides[n].classList.add("active__slide");
  };

  const nextSlide = () => {
    if (index == slides.length - 1) {
      index = 0;
      prepareCurrentSlide(index);
    } else {
      index++;
      prepareCurrentSlide(index);
    }
  };

  const activeDot = (n) => {
    for (dot of dots) {
      dot.classList.remove("active__dot");
    }
    dots[n].classList.add("active__dot");
  };

  const prepareCurrentSlide = (ind) => {
    activeSlide(ind);
    activeDot(ind);
  };

  dots.forEach((item, indexDot) => {
    item.addEventListener("click", () => {
      index = indexDot;
      prepareCurrentSlide(index);
    });
  });

  setInterval(nextSlide, 7000);
})();

// (function () {
//   const likeItemButton = document.querySelectorAll(".main__like__item-button");
//   console.log(likeItemButton)
//   likeItemButton.forEach((likeButton) =>{
//     likeButton.addEventListener('click', () => {
//       let likeButtonIcon = likeButton.querySelector(".like__item");
//       console.log(likeButtonIcon)
//       if(likeButtonIcon.src.includes("static/img/svg/item_liked.svg")){
//         likeButtonIcon.src = "static/img/svg/item_like.svg";
//       } else{
//         likeButtonIcon.src = "static/img/svg/item_liked.svg";
//       }
//     });
//   });
// })();

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
  for (let i = 0; i < menuLinks.length; i += 1) {
    menuLinks[i].addEventListener("click", () => {
      menu.classList.remove("header__nav_active");
    });
  }
})();


const sortOrders = document.querySelectorAll('input[name="sort-orders"]');
sortOrders.forEach((order) => {
  order.addEventListener("change", (event) => {
    sortItems(event.target.value);
  });
});

function sortItems(sortOrder) {
  const items = document.querySelectorAll(".main__item__card");
  const sortedItems = Array.from(items).sort((a, b) => {
    const priceA = parseFloat(a.dataset.price);
    const priceB = parseFloat(b.dataset.price);
    if (sortOrder === "descending") {
      return priceB - priceA;
    } else {
      return priceA - priceB;
    }
  });
  const container = document.querySelector(".items__container");
  container.innerHTML = "";
  sortedItems.forEach((item) => container.appendChild(item));
}


(function () {
  var checkboxes = document.querySelectorAll(".checkbox__producer");
  checkboxes.forEach(function (checkbox) {
    checkbox.addEventListener("change", function () {
      var checkedValues = Array.from(
        document.querySelectorAll(".checkbox__producer:checked")
      ).map(function (checkbox) {
        return checkbox.value;
      });
      var xhr = new XMLHttpRequest();

      var searchParams = new URLSearchParams(window.location.search);
      var categoryValue = searchParams.get("category");
      var subcategoryValue = searchParams.get("subcategory");

      let url = "/main";

      if (checkedValues.length > 0) {
        url += "?producer=" + checkedValues.join("&producer=");
      }
      if (categoryValue !== null) {
        url += (checkedValues.length > 0 ? "&" : "?") + "category=" + categoryValue;
      }
      if (subcategoryValue !== null) {
        url += (checkedValues.length > 0 || categoryValue !== null ? "&" : "?") +
          "subcategory=" +
          subcategoryValue;
      }

      xhr.open("GET", url);
      
      xhr.onload = function () {
        if (xhr.status === 200) {
          var items = JSON.parse(xhr.responseText).items;
          var itemList = document.querySelector(".items__container");
          itemList.innerHTML = "";
          if (items.length == 0){
            var div = document.createElement("div");
            div.className = "empty items__container-no-items";
            var h2 = document.createElement("h2");
            h2.className = "empty-message";
            h2.textContent = "Товарів за запитом не знайдено";
            div.appendChild(h2);
            var container = document.querySelector(".items__container");
            container.appendChild(div);
          } else {
            items.forEach(function (item) {
              var itemCard = document.createElement("a");
              itemCard.href = "/product/" + item.id + "/";
              itemCard.classList.add("main__item__card");
              itemCard.dataset.price = item.price;

              var likeButton = document.createElement("button");
              likeButton.classList.add("main__like__item-button");
              var likeIcon = document.createElement("img");
              likeIcon.src = "../static/img/svg/item_like.svg";
              likeIcon.alt = "like__item";
              likeIcon.classList.add("like__item");
              likeButton.appendChild(likeIcon);
              itemCard.appendChild(likeButton);

              var cartButton = document.createElement("button");
              cartButton.classList.add("main__add-to-cart-button");
              var cartIcon = document.createElement("img");
              cartIcon.src = "../static/img/svg/add-to-cart.svg";
              cartIcon.alt = "add to cart";
              cartIcon.classList.add("add_to_cart");
              cartButton.appendChild(cartIcon);
              itemCard.appendChild(cartButton);

              var cardContent = document.createElement("div");
              cardContent.classList.add("main__card__content");
              cardContent.addEventListener("click", function () {
                location.href = itemCard.href;
              });

              var imgContainer = document.createElement("div");
              imgContainer.classList.add("main__img__container");
              var itemImg = document.createElement("img");
              itemImg.src = "../media/" + item.image;
              itemImg.alt = "item_img";
              itemImg.classList.add("main__item__img");
              imgContainer.appendChild(itemImg);
              cardContent.appendChild(imgContainer);

              var itemInfo = document.createElement("div");
              itemInfo.classList.add("main__item__info");
              var itemName = document.createElement("p");
              itemName.classList.add("main__item__name");
              itemName.innerText = item.name;
              var itemCost = document.createElement("p");
              itemCost.classList.add("main__item__cost");
              itemCost.innerText = Number(item.price).toFixed(0) + " UAH";
              itemInfo.appendChild(itemName);
              itemInfo.appendChild(itemCost);
              cardContent.appendChild(itemInfo);

              itemCard.appendChild(cardContent);
              itemList.appendChild(itemCard);
            });
          }
        }
      };
      xhr.send();
    });
  });
})();

// (function(){
//   const itemCards = document.querySelectorAll(".main__item__card");
//   let clicked = false;

//   itemCards.forEach((item) => {
//     const addToCartButton = item.querySelector(".main__add-to-cart-button");
//     addToCartButton.addEventListener('click', () => {
//       clicked = true;
//       return;
//     });

//     if(clicked) return;

//     item.addEventListener('click', () => {
//       const itemId = item.dataset.id;

//       var xhr = new XMLHttpRequest();
//       xhr.open('GET', `/product/${itemId}`);
//       xhr.onload = function() {
//         window.location.href = xhr.responseURL;
//       };
//       xhr.send();
//     });
//   })

// })();

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


