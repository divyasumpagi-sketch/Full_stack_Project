// ============================================================
// main.js - Main JavaScript File
// Features: Form Validation, Navbar Toggle, UI Helpers
// ============================================================

// ---- Wait for DOM to be fully loaded ----
document.addEventListener("DOMContentLoaded", function () {

  // ==================== NAVBAR TOGGLE (Mobile) ====================
  const hamburger = document.querySelector(".hamburger");
  const navLinks  = document.querySelector(".nav-links");

  if (hamburger && navLinks) {
    hamburger.addEventListener("click", function () {
      navLinks.classList.toggle("open");
    });

    // Close menu when a link is clicked
    navLinks.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => navLinks.classList.remove("open"));
    });
  }

  // ==================== AUTO-DISMISS ALERTS ====================
  setTimeout(() => {
    document.querySelectorAll(".alert").forEach(alert => {
      alert.style.transition = "opacity 0.5s";
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 500);
    });
  }, 4000); // Remove after 4 seconds


  // ==================== REGISTRATION FORM VALIDATION ====================
  const registerForm = document.getElementById("registerForm");
  if (registerForm) {
    registerForm.addEventListener("submit", function (e) {
      let isValid = true;

      // Validate Name
      const name = document.getElementById("name");
      if (!name.value.trim() || name.value.trim().length < 2) {
        showError(name, "Name must be at least 2 characters.");
        isValid = false;
      } else {
        showSuccess(name);
      }

      // Validate Email
      const email = document.getElementById("email");
      if (!isValidEmail(email.value)) {
        showError(email, "Please enter a valid email address.");
        isValid = false;
      } else {
        showSuccess(email);
      }

      // Validate Password
      const password = document.getElementById("password");
      if (password.value.length < 6) {
        showError(password, "Password must be at least 6 characters.");
        isValid = false;
      } else {
        showSuccess(password);
      }

      // Validate Confirm Password
      const confirm = document.getElementById("confirm_password");
      if (confirm.value !== password.value) {
        showError(confirm, "Passwords do not match!");
        isValid = false;
      } else if (confirm.value) {
        showSuccess(confirm);
      }

      // If any validation failed, stop form submission
      if (!isValid) {
        e.preventDefault();
      }
    });

    // Live validation on input
    liveValidate("name", val => val.trim().length >= 2, "Name must be at least 2 characters.");
    liveValidate("email", val => isValidEmail(val), "Enter a valid email.");
    liveValidate("password", val => val.length >= 6, "Password must be 6+ characters.");
  }


  // ==================== LOGIN FORM VALIDATION ====================
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
      let isValid = true;

      const email    = document.getElementById("email");
      const password = document.getElementById("password");

      if (!isValidEmail(email.value)) {
        showError(email, "Please enter a valid email.");
        isValid = false;
      } else {
        showSuccess(email);
      }

      if (!password.value.trim()) {
        showError(password, "Password is required.");
        isValid = false;
      } else {
        showSuccess(password);
      }

      if (!isValid) e.preventDefault();
    });
  }


  // ==================== CONTACT FORM VALIDATION ====================
  const contactForm = document.getElementById("contactForm");
  if (contactForm) {
    contactForm.addEventListener("submit", function (e) {
      let isValid = true;

      const name    = document.getElementById("name");
      const email   = document.getElementById("email");
      const message = document.getElementById("message");

      if (!name.value.trim()) {
        showError(name, "Name is required."); isValid = false;
      } else { showSuccess(name); }

      if (!isValidEmail(email.value)) {
        showError(email, "Valid email required."); isValid = false;
      } else { showSuccess(email); }

      if (message.value.trim().length < 10) {
        showError(message, "Message must be at least 10 characters."); isValid = false;
      } else { showSuccess(message); }

      if (!isValid) e.preventDefault();
    });
  }


  // ==================== STUDENT / TASK FORM VALIDATION ====================
  const studentForm = document.getElementById("studentForm");
  if (studentForm) {
    studentForm.addEventListener("submit", function (e) {
      let isValid = true;

      ["name", "email", "course"].forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field && !field.value.trim()) {
          showError(field, "This field is required.");
          isValid = false;
        } else if (field) {
          showSuccess(field);
        }
      });

      const marks = document.getElementById("marks");
      if (marks) {
        const val = parseInt(marks.value);
        if (isNaN(val) || val < 0 || val > 100) {
          showError(marks, "Marks must be between 0 and 100.");
          isValid = false;
        } else {
          showSuccess(marks);
        }
      }

      if (!isValid) e.preventDefault();
    });
  }


  // ==================== CONFIRM DELETE ====================
  document.querySelectorAll(".btn-delete").forEach(btn => {
    btn.addEventListener("click", function (e) {
      if (!confirm("Are you sure you want to delete this record? This cannot be undone.")) {
        e.preventDefault();
      }
    });
  });

});  // END DOMContentLoaded


// ============================================================
// HELPER FUNCTIONS
// ============================================================

/**
 * Show error state on a form field
 * @param {HTMLElement} input - The input element
 * @param {string} message   - Error message to display
 */
function showError(input, message) {
  const group = input.closest(".form-group");
  if (!group) return;
  group.classList.remove("valid");
  group.classList.add("invalid");
  const errMsg = group.querySelector(".error-msg");
  if (errMsg) errMsg.textContent = message;
}

/**
 * Show success state on a form field
 * @param {HTMLElement} input - The input element
 */
function showSuccess(input) {
  const group = input.closest(".form-group");
  if (!group) return;
  group.classList.remove("invalid");
  group.classList.add("valid");
}

/**
 * Check if an email string is valid format
 * @param {string} email
 * @returns {boolean}
 */
function isValidEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email.trim());
}

/**
 * Add live (on-input) validation to a field
 * @param {string}   fieldId   - The ID of the input field
 * @param {Function} validator - Function that returns true if valid
 * @param {string}   errMsg    - Error message to display if invalid
 */
function liveValidate(fieldId, validator, errMsg) {
  const field = document.getElementById(fieldId);
  if (!field) return;
  field.addEventListener("input", function () {
    if (validator(field.value)) {
      showSuccess(field);
    } else {
      showError(field, errMsg);
    }
  });
}
