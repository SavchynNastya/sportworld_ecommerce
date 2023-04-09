(function () {
  const items = document.querySelectorAll(".cart__item__card");

  function updateTotalCartPrice() {
    let total = 0;
    items.forEach((item) => {
      const quantity = parseInt(
        item.querySelector(".items__quantity-input").value
      );
      const price = parseFloat(item.querySelector(".item__cost").textContent);
      const itemTotal = (quantity * price).toFixed(0);
      item.querySelector(".cart__summary__pricing-value #value").textContent =
        itemTotal;
      total += parseFloat(itemTotal);
    });
    document.getElementById("total-value").textContent = total.toFixed(0);
  }

  items.forEach((item) => {
    const increaseQuantityBtn = item.querySelector(".increase");
    const decreaseQuantityBtn = item.querySelector(".decrease");
    const inputQuantity = item.querySelector(".items__quantity-input");

    increaseQuantityBtn.addEventListener("click", function () {
      inputQuantity.value = parseInt(inputQuantity.value) + 1;

      const itemId = item.dataset.id;

      var xhr = new XMLHttpRequest();
      xhr.open("GET", `/increment-cart-item/${itemId}/`);
      xhr.onload = function () {
        window.location.href = xhr.responseURL;
      };
      xhr.send();

    });

    decreaseQuantityBtn.addEventListener("click", function () {
      if (parseInt(inputQuantity.value) > 1) {
        inputQuantity.value = parseInt(inputQuantity.value) - 1;

        const itemId = item.dataset.id;

        var xhr = new XMLHttpRequest();
        xhr.open("GET", `/decrement-cart-item/${itemId}/`);
        xhr.onload = function () {
          window.location.href = xhr.responseURL;
        };
        xhr.send();
      }
    });
  });

  updateTotalCartPrice();
})();

(function () {
  const itemCards = document.querySelectorAll(".cart__item__card");
  itemCards.forEach((itemCard) => {
    console.log(itemCard);
    const likeItemButton = itemCard.querySelector(".cart__like__item-button");
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

(function (){
  const openContactForm = document.querySelectorAll(".open-contact-form");
  console.log(openContactForm);
  const closeModal = document.getElementById("close-contact-modal");
  let cookie = document.cookie;
  let csrfToken = cookie.substring(cookie.indexOf("=") + 1);
  csrfToken = csrfToken.substring(csrfToken.indexOf("=") + 1);
  console.log(csrfToken);


  var formContainer = document.getElementById("modal-contact");
  var contactForm = document.getElementById("contact-form");

  openContactForm.forEach((openForm) => {
    openForm.addEventListener("click", function () {
      formContainer.style.display = "block";
    });
  });

  closeModal.addEventListener("click", function () {
    formContainer.style.display = "none";
  });

  contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const url = "form-order/";
    // const contactNumber = document.getElementById("contact-number").value;
    const contactNumber = document.getElementById("id_phone_number").value;
    const countryCode = document.getElementById("id_country_code").value;
    console.log(contactNumber)
    console.log(countryCode)
    const data = {
      contact_number: contactNumber,
      country_code: countryCode,
    };
    console.log(data)
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(data),
      credentials: "same-origin",
    }).then((response) => {
      if (response.ok) {
        formContainer.style.display = "none";
        alert("Замовлення сформовано успішно, очікуйте дзвінка");
      } else {
        alert("Сталася помилка");
      }
    });
      // .catch((error) => {
      //   // handle error
      // });
  });

})();