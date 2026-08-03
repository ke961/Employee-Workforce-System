"use strict";


/* =========================================================
   Configuration
========================================================= */

const LOGIN_ENDPOINT = "/api/auth/login";

const TOKEN_STORAGE_KEY = "ems_access_token";
const ADMIN_STORAGE_KEY = "ems_admin";
const EMAIL_STORAGE_KEY = "ems_remembered_email";


/* =========================================================
   DOM Elements
========================================================= */

const loginForm = document.getElementById("loginForm");

const loginEmail = document.getElementById("loginEmail");
const loginPassword = document.getElementById("loginPassword");

const rememberEmail = document.getElementById("rememberEmail");

const emailError = document.getElementById("emailError");
const passwordError = document.getElementById("passwordError");

const loginButton = document.getElementById("loginButton");
const loginButtonText = document.getElementById(
    "loginButtonText"
);

const loginSpinner = document.getElementById(
    "loginSpinner"
);

const loginMessage = document.getElementById(
    "loginMessage"
);

const togglePasswordButton = document.getElementById(
    "togglePasswordButton"
);


/* =========================================================
   Page Initialization
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    initializeLoginPage
);


function initializeLoginPage() {
    const existingToken = localStorage.getItem(
        TOKEN_STORAGE_KEY
    );

    if (existingToken) {
        window.location.replace("/dashboard.html");
        return;
    }

    loadRememberedEmail();

    loginEmail.focus();
}


/* =========================================================
   Remember Email
========================================================= */

function loadRememberedEmail() {
    const savedEmail = localStorage.getItem(
        EMAIL_STORAGE_KEY
    );

    if (savedEmail) {
        loginEmail.value = savedEmail;
        rememberEmail.checked = true;
    }
}


function saveRememberedEmail(email) {
    if (rememberEmail.checked) {
        localStorage.setItem(
            EMAIL_STORAGE_KEY,
            email
        );
    } else {
        localStorage.removeItem(
            EMAIL_STORAGE_KEY
        );
    }
}


/* =========================================================
   Password Visibility
========================================================= */

togglePasswordButton.addEventListener(
    "click",
    () => {
        const passwordIsHidden =
            loginPassword.type === "password";

        loginPassword.type = passwordIsHidden
            ? "text"
            : "password";

        togglePasswordButton.textContent =
            passwordIsHidden
                ? "Hide"
                : "Show";

        togglePasswordButton.setAttribute(
            "aria-label",
            passwordIsHidden
                ? "Hide password"
                : "Show password"
        );
    }
);


/* =========================================================
   Form Validation
========================================================= */

function validateLoginForm() {
    clearFieldErrors();

    let formIsValid = true;

    const email = loginEmail.value
        .trim()
        .toLowerCase();

    const password = loginPassword.value;

    if (!email) {
        showFieldError(
            loginEmail,
            emailError,
            "Email address is required."
        );

        formIsValid = false;

    } else if (!isValidEmail(email)) {
        showFieldError(
            loginEmail,
            emailError,
            "Enter a valid email address."
        );

        formIsValid = false;
    }

    if (!password) {
        showFieldError(
            loginPassword,
            passwordError,
            "Password is required."
        );

        formIsValid = false;

    } else if (password.length < 6) {
        showFieldError(
            loginPassword,
            passwordError,
            "Password must contain at least 6 characters."
        );

        formIsValid = false;
    }

    return formIsValid;
}


function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}


function showFieldError(
    inputElement,
    errorElement,
    message
) {
    inputElement.classList.add("input-error");
    errorElement.textContent = message;
}


function clearFieldErrors() {
    loginEmail.classList.remove("input-error");
    loginPassword.classList.remove("input-error");

    emailError.textContent = "";
    passwordError.textContent = "";
}


/* =========================================================
   Remove Error While Typing
========================================================= */

loginEmail.addEventListener(
    "input",
    () => {
        loginEmail.classList.remove("input-error");
        emailError.textContent = "";
        hideLoginMessage();
    }
);


loginPassword.addEventListener(
    "input",
    () => {
        loginPassword.classList.remove("input-error");
        passwordError.textContent = "";
        hideLoginMessage();
    }
);


/* =========================================================
   Login Submission
========================================================= */

loginForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        if (!validateLoginForm()) {
            return;
        }

        const email = loginEmail.value
            .trim()
            .toLowerCase();

        const password = loginPassword.value;

        setLoginLoading(true);
        hideLoginMessage();

        try {
            const response = await fetch(
                LOGIN_ENDPOINT,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email,
                        password
                    })
                }
            );

            const responseData =
                await readResponseData(response);

            if (!response.ok) {
                throw new Error(
                    extractErrorMessage(
                        responseData,
                        response.status
                    )
                );
            }

            if (!responseData.access_token) {
                throw new Error(
                    "The server did not return an access token."
                );
            }

            saveSession(responseData);

            saveRememberedEmail(email);

            showLoginMessage(
                "Login successful. Redirecting...",
                "success"
            );

            window.setTimeout(
                () => {
                    window.location.replace(
                        "/dashboard.html"
                    );
                },
                500
            );

        } catch (error) {
            showLoginMessage(
                error.message ||
                    "Unable to sign in.",
                "error"
            );

        } finally {
            setLoginLoading(false);
        }
    }
);


/* =========================================================
   Save Authentication Session
========================================================= */

function saveSession(responseData) {
    localStorage.setItem(
        TOKEN_STORAGE_KEY,
        responseData.access_token
    );

    localStorage.setItem(
        ADMIN_STORAGE_KEY,
        JSON.stringify(
            responseData.admin || null
        )
    );
}


/* =========================================================
   Response Processing
========================================================= */

async function readResponseData(response) {
    const responseText = await response.text();

    if (!responseText) {
        return {};
    }

    try {
        return JSON.parse(responseText);
    } catch (error) {
        return {
            detail: responseText
        };
    }
}


function extractErrorMessage(
    responseData,
    statusCode
) {
    if (
        responseData &&
        typeof responseData.detail === "string"
    ) {
        return responseData.detail;
    }

    if (
        responseData &&
        Array.isArray(responseData.detail)
    ) {
        return responseData.detail
            .map((errorItem) => {
                const field = Array.isArray(
                    errorItem.loc
                )
                    ? errorItem.loc
                        .filter(
                            (location) =>
                                location !== "body"
                        )
                        .join(" → ")
                    : "field";

                return `${field}: ${errorItem.msg}`;
            })
            .join(", ");
    }

    if (statusCode === 401) {
        return "Incorrect email or password.";
    }

    if (statusCode === 422) {
        return "The submitted login information is invalid.";
    }

    if (statusCode >= 500) {
        return "The server encountered an error.";
    }

    return `Login failed with status ${statusCode}.`;
}


/* =========================================================
   Loading State
========================================================= */

function setLoginLoading(isLoading) {
    loginButton.disabled = isLoading;

    loginButtonText.textContent = isLoading
        ? "Signing in..."
        : "Sign in";

    loginSpinner.classList.toggle(
        "hidden",
        !isLoading
    );

    loginEmail.disabled = isLoading;
    loginPassword.disabled = isLoading;
    rememberEmail.disabled = isLoading;
    togglePasswordButton.disabled = isLoading;
}


/* =========================================================
   Login Message
========================================================= */

function showLoginMessage(
    message,
    type
) {
    loginMessage.textContent = message;

    loginMessage.className =
        `login-message ${type}`;

    loginMessage.classList.remove("hidden");
}


function hideLoginMessage() {
    loginMessage.textContent = "";
    loginMessage.className =
        "login-message hidden";
}
