// /////////////// Create Staff Script //////////////

// <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>;

// document.addEventListener("DOMContentLoaded", function () {
//   const stateDropdown = document.getElementById("state");
//   const districtDropdown = document.getElementById("district");
//   console.log(stateDropdown);

//   stateDropdown.addEventListener("change", function () {
//     const stateId = stateDropdown.value;

//     // Clear previous districts
//     districtDropdown.innerHTML = '<option value="">Select District</option>';

//     if (stateId) {
//       fetch(`/ajax/get-districts/?state_id=${stateId}`)
//         .then((response) => response.json())
//         .then((data) => {
//           const districts = data.districts;
//           districts.forEach((district) => {
//             const option = document.createElement("option");
//             option.value = district.id;
//             option.textContent = district.district;
//             districtDropdown.appendChild(option);
//           });
//         })
//         .catch((error) => {
//           console.error("Error fetching districts:", error);
//         });
//     }
//   });
// });

// document.addEventListener("DOMContentLoaded", function () {
//   const staffStatusDiv = document.getElementById("staffstatus");
//   const staffStatus = document.querySelector('[name="status"]'); // Ensure it matches your actual field name
//   const staffType = document.querySelector('[name="staff_type"]'); // Ensure it matches your actual field name
//   const deptContainer = document.getElementById("dept_container");

//   if (staffType) {
//     staffType.addEventListener("change", function () {
//       deptContainer.style.display =
//         staffType.value === "Teaching" ? "block" : "none";
//     });
//   } else {
//     console.error("Element with ID 'staff_type' not found.");
//   }

//   if (staffStatusDiv && staffStatus) {
//     staffStatus.addEventListener("change", function () {
//       // Remove existing 'salary' and 'date_of_exite' fields if they exist
//       const salaryField = document.getElementById("salary");
//       const exitDateField = document.getElementById("date_of_exite");

//       if (salaryField) salaryField.parentElement.remove();
//       if (exitDateField) exitDateField.parentElement.remove();

//       if (staffStatus.value === "Working") {
//         const div = document.createElement("div");
//         div.className = "col-md-2";
//         div.innerHTML = `
//                 <label for="salary" class="form-label">Salary</label>
//                 <input type="text" name="salary" id="salary">
//                 `;
//         staffStatusDiv.appendChild(div);
//       } else if (
//         staffStatus.value === "Transferred" ||
//         staffStatus.value === "Departed"
//       ) {
//         const div = document.createElement("div");
//         div.className = "col-md-2";
//         div.innerHTML = `
//                 <label for="date_of_exite" class="form-label">DOE from College</label>
//                 <input type="date" name="date_of_exite" id="date_of_exite">
//                 `;
//         staffStatusDiv.appendChild(div);
//       }
//     });
//   } else {
//     console.error("Element with ID 'staffstatus' or 'status' not found.");
//   }
// });

// document.addEventListener("DOMContentLoaded", function () {
//   const addressToggle = document.getElementById("address_toggle");
//   const bankToggle = document.getElementById("bank_toggle");
//   const addressSection = document.getElementById("address_section");
//   const bankSection = document.getElementById("bank_section");
//   const addressInputs = addressSection.querySelectorAll(
//     "input, select, textarea"
//   );
//   const bankInputs = bankSection.querySelectorAll("input, select, textarea");

//   function toggleSection(section, inputs, isVisible) {
//     section.style.display = isVisible ? "flex" : "none";
//     inputs.forEach((input) => {
//       input.required = isVisible; // Make inputs required when visible
//       if (!isVisible) input.value = ""; // Clear input value when hidden
//     });
//   }

//   if (addressToggle) {
//     addressToggle.addEventListener("change", function () {
//       toggleSection(addressSection, addressInputs, addressToggle.checked);
//     });
//   }

//   if (bankToggle) {
//     bankToggle.addEventListener("change", function () {
//       toggleSection(bankSection, bankInputs, bankToggle.checked);
//     });
//   }
// });
// ////////////////////////////////////////////////////////////

    document.addEventListener("DOMContentLoaded", function () {
      const stateDropdown = document.getElementById("state");
      const districtDropdown = document.getElementById("district");
      console.log(stateDropdown);

      stateDropdown.addEventListener("change", function () {
        const stateId = stateDropdown.value;

        // Clear previous districts
        districtDropdown.innerHTML =
          '<option value="">Select District</option>';

        if (stateId) {
          fetch(`/ajax/get-districts/?state_id=${stateId}`)
            .then((response) => response.json())
            .then((data) => {
              const districts = data.districts;
              districts.forEach((district) => {
                const option = document.createElement("option");
                option.value = district.id;
                option.textContent = district.district;
                districtDropdown.appendChild(option);
              });
            })
            .catch((error) => {
              console.error("Error fetching districts:", error);
            });
        }
      });
    });

    document.addEventListener("DOMContentLoaded", function () {
      const staffStatusDiv = document.getElementById("staffstatus");
      const staffStatus = document.querySelector('[name="status"]'); // Ensure it matches your actual field name
      const staffType = document.querySelector('[name="staff_type"]'); // Ensure it matches your actual field name
      const deptContainer = document.getElementById("dept_container");

      if (staffType) {
        staffType.addEventListener("change", function () {
          deptContainer.style.display =
            staffType.value === "Teaching" ? "block" : "none";
        });
      } else {
        console.error("Element with ID 'staff_type' not found.");
      }

      if (staffStatusDiv && staffStatus) {
        staffStatus.addEventListener("change", function () {
          // Remove existing 'salary' and 'date_of_exite' fields if they exist
          const salaryField = document.getElementById("salary");
          const exitDateField = document.getElementById("date_of_exite");

          if (salaryField) salaryField.parentElement.remove();
          if (exitDateField) exitDateField.parentElement.remove();

          if (staffStatus.value === "Working") {
            const div = document.createElement("div");
            div.className = "col-md-2";
            div.innerHTML = `
                <label for="salary" class="form-label">Salary</label>
                <input type="text" name="salary" id="salary">
                `;
            staffStatusDiv.appendChild(div);
          } else if (
            staffStatus.value === "Transferred" ||
            staffStatus.value === "Departed"
          ) {
            const div = document.createElement("div");
            div.className = "col-md-2";
            div.innerHTML = `
                <label for="date_of_exite" class="form-label">DOE from College</label>
                <input type="date" name="date_of_exite" id="date_of_exite">
                `;
            staffStatusDiv.appendChild(div);
          }
        });
      } else {
        console.error("Element with ID 'staffstatus' or 'status' not found.");
      }
    });

    document.addEventListener("DOMContentLoaded", function () {
      const addressToggle = document.getElementById("address_toggle");
      const bankToggle = document.getElementById("bank_toggle");
      const addressSection = document.getElementById("address_section");
      const bankSection = document.getElementById("bank_section");
      const addressInputs = addressSection.querySelectorAll(
        "input, select, textarea"
      );
      const bankInputs = bankSection.querySelectorAll(
        "input, select, textarea"
      );

      function toggleSection(section, inputs, isVisible) {
        section.style.display = isVisible ? "flex" : "none";
        inputs.forEach((input) => {
          input.required = isVisible; // Make inputs required when visible
          if (!isVisible) input.value = ""; // Clear input value when hidden
        });
      }

      if (addressToggle) {
        addressToggle.addEventListener("change", function () {
          toggleSection(addressSection, addressInputs, addressToggle.checked);
        });
      }

      if (bankToggle) {
        bankToggle.addEventListener("change", function () {
          toggleSection(bankSection, bankInputs, bankToggle.checked);
        });
      }
    });