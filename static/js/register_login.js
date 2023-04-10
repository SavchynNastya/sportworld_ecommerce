function showPassword() {
  let input = document.getElementById("id_password");
  let button = document.getElementsByClassName("password-button")[0];
  if (input.type === "password") {
    input.type = "text";
    button.classList.remove("fa-eye-slash");
    button.classList.add("fa-eye");
  } else {
    input.type = "password";
    button.classList.remove("fa-eye");
    button.classList.add("fa-eye-slash");
  }
}


const modal = document.getElementById("modal");
const openModalBtns = document.querySelectorAll(".open-modal");
console.log(openModalBtns);
const closeModalBtn = document.getElementById("close-modal");
const modalTitle = document.getElementById("modal-title");
// const modalFooter = document.getElementsByClassName("modal-footer");
const modalFooterText = document.getElementById("modal-footer-text");
const switchToRegisterLink = document.getElementById("switch-to-register");
const forgotPasswordLink = document.getElementById("forgot-password");


openModalBtns.forEach((openModalBtn) => {
  openModalBtn.addEventListener("click", function () {
    modal.style.display = "block";
  });
});

closeModalBtn.addEventListener("click", function () {
  modal.style.display = "none";
});

function submitForm(form, url, title) {
  const formData = new FormData(form);

  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        const contentType = xhr.getResponseHeader('Content-Type');
        if (contentType.includes('application/json')) {
          const response = JSON.parse(xhr.responseText);
          if (response.success) {
            if(response.message){
              modalTitle.innerHTML = response.message;
              const formContainer = form.parentElement;
              formContainer.innerHTML = "";
            }
            if(response.redirect_url){
              window.location.href = response.redirect_url;
            }

          } else {
            const formHtml = xhr.responseText;
            const formContainer = form.parentElement;
            formContainer.innerHTML = formHtml;
            const newForm = formContainer.firstElementChild;
            newForm.addEventListener("submit", function (event) {
              event.preventDefault();
              console.log(url)
              submitForm(newForm, url, title);
            });
          }
        } else {
          const formHtml = xhr.responseText;
          const formContainer = form.parentElement;
          formContainer.innerHTML = formHtml;
          const newForm = formContainer.firstElementChild;
          newForm.addEventListener("submit", function (event) {
            event.preventDefault();
            console.log(url);
            submitForm(newForm, url, title);
          });
        }
      } else {
        console.log(url);
        const errors = JSON.parse(xhr.response);
        const form = document.getElementById("login-form");
        console.log(form);
        for (const field in form.elements) {
          if (errors[field]) {
            const errorSpan = document.createElement("span");
            errorSpan.className = "error-message";
            errorSpan.innerText = errors[field];
            form.elements[field].parentNode.appendChild(errorSpan);
          }
        }
      }
    }
  };
  console.log(url);
  xhr.open("POST", url);
  xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  xhr.send(formData);

  modalTitle.innerHTML = title;
}

const loginForm = document.getElementById("login-form");

const registrationFormSubmitHandler = function (event) {
  event.preventDefault();
  submitForm(loginForm.firstChild, "/registration-form/", "Реєстрація");
};

const loginFormSubmitHandler = function (event) {
  event.preventDefault();
  submitForm(loginForm.firstChild, "/login/", "Вхід");
};

const forgotPasswordFormSubmitHandler = function (event) {
  event.preventDefault();
  submitForm(loginForm.firstChild, "/password_reset/", "Відновити пароль");
};

function switchToForgotPasswordForm(){
  forgotPasswordLink.style.display = "none";

  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      loginForm.innerHTML = xhr.responseText;
      modalTitle.innerHTML = "Відновити пароль";
    }
  };
  xhr.open("GET", "/password_reset/");
  xhr.send();

  loginForm.removeEventListener("submit", loginFormSubmitHandler);
  loginForm.addEventListener("submit", forgotPasswordFormSubmitHandler);
}


openModalBtns.forEach((openModalBtn) => {
  openModalBtn.addEventListener("click", function () {

    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        loginForm.innerHTML = xhr.responseText;
        modalTitle.innerHTML = "Вхід";
      }
    };
    xhr.open("GET", "/login/");
    xhr.send();

    loginForm.addEventListener("submit", loginFormSubmitHandler);

    forgotPasswordLink.addEventListener("click", switchToForgotPasswordForm);
  });

})

function switchToRegisterForm() {
  forgotPasswordLink.style.display = "none";

  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      loginForm.innerHTML = xhr.responseText;
      modalTitle.innerHTML = "Реєстрація";
    }
  };
  xhr.open("GET", "/registration-form/");
  xhr.send();

  loginForm.removeEventListener("submit", loginFormSubmitHandler);
  loginForm.addEventListener("submit", registrationFormSubmitHandler);

  modalFooterText.innerHTML = "Вже маєте акаунт?";
  switchToRegisterLink.innerHTML = "Увійти";
  switchToRegisterLink.removeEventListener("click", switchToRegisterForm);
  switchToRegisterLink.addEventListener("click", switchToLoginForm);
}

function switchToLoginForm() {
  forgotPasswordLink.style.display = "block";

  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      loginForm.innerHTML = xhr.responseText;
      modalTitle.innerHTML = "Вхід";
    }
  };
  xhr.open("GET", "/login/");
  xhr.send();

  loginForm.removeEventListener("submit", registrationFormSubmitHandler);
  loginForm.addEventListener("submit", loginFormSubmitHandler);

  modalFooterText.innerHTML = "Уперше тут?";
  switchToRegisterLink.innerHTML = "Зареєструватися";
  switchToRegisterLink.removeEventListener("click", switchToLoginForm);
  switchToRegisterLink.addEventListener("click", switchToRegisterForm);
  forgotPasswordLink.addEventListener("click", switchToForgotPasswordForm);
}

switchToRegisterLink.addEventListener("click", switchToRegisterForm);


(function () {
    const burgerItem = document.querySelector('.burger');
    const menu = document.querySelectorAll('.header__nav');
    const menuCloseItem = document.querySelector('.header__nav-close');
    const menuLinks = document.querySelectorAll(".header__link");
    const menuIcons = document.querySelectorAll(".header__icon_item");
    const hiddenLinks = document.querySelectorAll(".hidden__link");
    burgerItem.addEventListener('click', () => {
        menu.forEach(m => {
          m.classList.add("header__nav_active");
        });
        hiddenLinks.forEach((link) => {
          link.classList.add("hidden__link_active");
        });
    });
    menuCloseItem.addEventListener('click', () => {
        menu.forEach((m) => {
          m.classList.remove("header__nav_active");
        });
        hiddenLinks.forEach((link) => {
          link.classList.add("hidden__link_active");
        });
    });
    for (let i=0; i < menuLinks.length; i+=1){
        menuLinks[i].addEventListener('click', () => {
            menu.forEach((m) => {
              m.classList.remove("header__nav_active");
            });
        });
    }
    for (let i = 0; i < menuIcons.length; i += 1) {
      menuIcons[i].addEventListener("click", () => {
        menu.forEach((m) => {
          m.classList.remove("header__nav_active");
        });
      });
    }
}());