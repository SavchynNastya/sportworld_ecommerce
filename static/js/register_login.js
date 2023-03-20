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
const openModalBtn = document.getElementById("open-modal");
const closeModalBtn = document.getElementById("close-modal");
const modalTitle = document.getElementById("modal-title");
const switchToRegisterLink = document.getElementById("switch-to-register");


openModalBtn.addEventListener("click", function () {
  modal.style.display = "block";
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
            window.location.href = response.redirect_url;
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
  submitForm(loginForm.firstChild, "/registration-form/", "Register");
};

const loginFormSubmitHandler = function (event) {
  event.preventDefault();
  submitForm(loginForm.firstChild, "/login/", "Login");
};


openModalBtn.addEventListener("click", function () {
  // const loginForm = document.getElementById("login-form");
  // const modalTitle = document.getElementById("modal-title");

  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      loginForm.innerHTML = xhr.responseText;
      modalTitle.innerHTML = "Login";
    }
  };
  xhr.open("GET", "/login/");
  xhr.send();

  loginForm.addEventListener("submit", loginFormSubmitHandler);
});


function switchToRegisterForm() {
  // const loginForm = document.getElementById("login-form");
  // const modalTitle = document.getElementById("modal-title");

  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      loginForm.innerHTML = xhr.responseText;
      modalTitle.innerHTML = "Register";
    }
  };
  xhr.open("GET", "/registration-form/");
  xhr.send();

  loginForm.removeEventListener("submit", loginFormSubmitHandler);
  loginForm.addEventListener("submit", registrationFormSubmitHandler);

  switchToRegisterLink.innerHTML = "Login";
  switchToRegisterLink.removeEventListener("click", switchToRegisterForm);
  switchToRegisterLink.addEventListener("click", switchToLoginForm);
}

function switchToLoginForm() {
  // const loginForm = document.getElementById("login-form");
  // const modalTitle = document.getElementById("modal-title");

  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      loginForm.innerHTML = xhr.responseText;
      modalTitle.innerHTML = "Login";
    }
  };
  xhr.open("GET", "/login/");
  xhr.send();

  loginForm.removeEventListener("submit", registrationFormSubmitHandler);
  loginForm.addEventListener("submit", loginFormSubmitHandler);

  switchToRegisterLink.innerHTML = "Register";
  switchToRegisterLink.removeEventListener("click", switchToLoginForm);
  switchToRegisterLink.addEventListener("click", switchToRegisterForm);

}

switchToRegisterLink.addEventListener("click", switchToRegisterForm);
