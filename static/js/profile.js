(function () {
  const openReviewForm = document.querySelectorAll(".open-review-form");
  console.log(openReviewForm);
  const closeReviewModal = document.getElementById("close-review-modal");
  let cookie = document.cookie;
  let reviewCsrfToken = cookie.substring(cookie.indexOf("=") + 1);
  reviewCsrfToken = reviewCsrfToken.substring(reviewCsrfToken.indexOf("=") + 1);
  console.log(reviewCsrfToken);

  var formReviewContainer = document.getElementById("modal-review");
  console.log(formReviewContainer);
  var ratingForm = document.getElementById("rating-form");

  let itemId = null;

  openReviewForm.forEach((openForm) => {
    openForm.addEventListener("click", function (e) {
      formReviewContainer.style.display = "block";

      itemId = e.target
        .closest(".order__item__info")
        .getAttribute("data-id");
      console.log(itemId);
    });
  });

  closeReviewModal.addEventListener("click", function () {
    formReviewContainer.style.display = "none";
  });


    const stars = document.querySelectorAll("input[type=radio][name='rating']");
    const starLabels = document.querySelectorAll(".star-label");
    console.log(stars);
    let value = null;

    stars.forEach((star) => {
      star.addEventListener("click", () => {
        value = star.getAttribute("value");
        console.log(value);

        for (let i = 0; i < value; i++) {
          stars[i].classList.add("filled");
          starLabels[i].classList.add("filled");
        }

        for (let i = value; i < stars.length; i++) {
          stars[i].classList.remove("filled");
          starLabels[i].classList.remove("filled");
        }
      });
    });

  ratingForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const url = "profile/";

    const textReview = document.getElementById("id_message").value;
    console.log(value);
    console.log(textReview);
    const data = {
      item_id: itemId,
      message: textReview,
      rating: value,
    };
    console.log(data);
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": reviewCsrfToken,
      },
      body: JSON.stringify(data),
      credentials: "same-origin",
    }).then((response) => {
      if (response.ok) {
        formReviewContainer.style.display = "none";
      } else {
        alert("Сталася помилка");
      }
    });
  });
})();


(function () {
  const openContactForm = document.getElementById("add_contact");
  console.log(openContactForm);
  const closeModal = document.getElementById("close-contact-modal");
  let cookie = document.cookie;
  let csrfToken = cookie.substring(cookie.indexOf("=") + 1);
  csrfToken = csrfToken.substring(csrfToken.indexOf("=") + 1);
  console.log(csrfToken);

  var formContainer = document.getElementById("modal-contact");
  var contactForm = document.getElementById("contact-form");

  openContactForm.addEventListener("click", function () {
    formContainer.style.display = "block";
  });

  closeModal.addEventListener("click", function () {
    formContainer.style.display = "none";
  });

  contactForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const url = "add-contact-number-to-profile/";
    const contactNumber = document.getElementById("id_phone_number").value;
    const countryCode = document.getElementById("id_country_code").value;
    console.log(contactNumber);
    console.log(countryCode);
    const data = {
      contact_number: contactNumber,
      country_code: countryCode,
    };
    console.log(data);
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
      } else {
        alert("Сталася помилка");
      }
    });
  });
})();