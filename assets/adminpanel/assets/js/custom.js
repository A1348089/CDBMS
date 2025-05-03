// State and Subject Combination Script
$(document).ready(function(){
    $('#id_state').change(function(){
        var state_id = $(this).val();
        var entityType = "{{ entity_type }}";  // Get entity type dynamically

        if (state_id) {
            $.ajax({
              url: "/ajax/get-districts/",
              type: "GET",
              data: { state_id: state_id },
              dataType: "json",
              success: function (response) {
                console.log("Response received:", response);

                var districtDropdown = $("#id_district");
                districtDropdown.empty();
                districtDropdown.append(
                  '<option value="">Select District</option>'
                );

                if (response.districts && response.districts.length > 0) {
                  $.each(response.districts, function (index, district) {
                    let option = `<option value="${district.id}">${district.district}</option>`;
                    districtDropdown.append(option);
                  });
                } else {
                  districtDropdown.append(
                    '<option value="">No districts available</option>'
                  );
                }

                districtDropdown.trigger("change");
              },
              error: function (xhr, status, error) {
                console.error("Error fetching districts:", error);
              },
            });
        } else {
            $('#id_district').empty().append('<option value="">Select District</option>').trigger("change");
        }
    });
});

    /* Fetch group based on Program ID */
    
$(document).ready(function () {
  $("#id_program").change(function () {
    var program_id = $(this).val(); // Get selected program ID
    console.log("Selected Program ID:", program_id);

    let groupDropdown = $("#group");
    let subjectCombination = $("#id_subject_combination");

    groupDropdown.empty().append('<option value="">Select</option>');
    subjectCombination.empty().append('<option value="">Select</option>');

    if (program_id) {
      $.ajax({
        url: "/api/subject-combinations/",
        type: "GET",
        data: { program_id: program_id },
        dataType: "json",
        success: function (response) {

          if (
            response &&
            response.combinations &&
            response.combinations.length > 0
          ) {
            $.each(response.combinations, function (index, combination) {
              let option = `<option value="${combination.id}">${combination.combination_short_form} (${combination.combination_full_form})</option>`;
              groupDropdown.append(option);
              subjectCombination.append(option);
            });
          } else {
            groupDropdown.append(
              '<option value="">No subject combination available</option>'
            );
            subjectCombination.append(
              '<option value="">No subject combination available</option>'
            );
          }
        },
        error: function (xhr, status, error) {
          console.error(
            "Error fetching subject combinations:",
            xhr.responseText
          );
        },
      });
    }
  });
});

$(document).ready(function () {
  // Stydent Search
  $("#search_student").keypress(function (event) {
    if (event.which === 13) {
      // Check if Enter key is pressed
      var query = $(this).val().trim();

      if (query.length > 0) {
        $.ajax({
          url: "/student/api/search-students/",
          data: { query: query },
          dataType: "json",
          success: function (response) {
            var tbody = $("#student-body");
            tbody.empty();

            if (response.students.length > 0) {
              response.students.forEach(function (student) {
                tbody.append(`
                                    <tr>
                                        <td>${student.OAMDC_NO}</td>
                                        <td>${student.first_name}</td>
                                        <td>${student.last_name}</td>
                                        <td>${student.mobile_no}</td>
                                        <td>${student.email}</td>
                                        <td>${student.gender}</td>
                                        <td>${student.date_of_birth}</td>
                                        <td>${student.program_short_name} (${student.subject_combination_short_name})</td>
                                        <td>${student.status}</td>
                                        <td>
                                            <a href="/student/${student.id}/" class="btn btn-info btn-sm">View</a>
                                            <a href="/student/delete/${student.id}/" class="btn btn-danger btn-sm">Delete</a>
                                        </td>
                                    </tr>
                                `);
              });
            } else {
              tbody.append('<tr><td colspan="8">No students found</td></tr>');
            }
          },
          error: function () {
            alert("Error fetching data.");
          },
        });
      } else {
        location.reload();
      }
    }
  });

  // Staff Search
  $("#search_staff").keypress(function (event) {
    if (event.which === 13) {
      // Check if Enter key is pressed
      var query = $(this).val().trim();

      if (query.length > 0) {
        $.ajax({
          url: "/staff/api/search-staffs/",
          data: { query: query },
          dataType: "json",
          success: function (response) {
            var tbody = $("#staff-body"); // Correct tbody id
            tbody.empty();
            if (response.staffs.length > 0) {
              response.staffs.forEach(function (staff) {
                tbody.append(`
                                    <tr>
                                        <td>${staff.staff_id}</td>
                                        <td>${staff.staff_type}</td>
                                        <td>${staff.first_name} ${staff.last_name}</td>
                                        <td>${staff.mobile_no}</td>
                                        <td>${staff.gender}</td>
                                        <td>${staff.department}</td>
                                        <td>${staff.doj_in_college}</td>
                                        <td>${staff.status}</td>
                                        <td>${staff.doj_in_govt_service}</td>
                                        <td>${staff.experience}</td>
                                        <td>
                                            <a href="/staff/${staff.id}/" class="btn btn-info btn-sm">View</a>
                                            <a href="/staff/delete/${staff.id}/" class="btn btn-danger btn-sm">Delete</a>
                                        </td>
                                    </tr>
                                `);
              });
            } else {
              tbody.append('<tr><td colspan="10">No staff found</td></tr>');
            }
          },
          error: function () {
            alert("Error fetching data.");
          },
        });
      } else {
        location.reload();
      }
    }
  });
});
///////////////////////////////////////////////////////////////////////

document.addEventListener("DOMContentLoaded", function () {
  var downloadBtn = document.getElementById("download-staff-excel");

  if (downloadBtn) {
    downloadBtn.addEventListener("click", function () {
      var form = document.getElementById("filter-form");

      if (!form) {
        console.error("Filter form not found!");
        return;
      }
      var queryParams = new URLSearchParams(new FormData(form)).toString();

      var columnParams = Array.from(
        document.querySelectorAll("input[name='columns']:checked")
      )
        .map((checkbox) => "columns=" + encodeURIComponent(checkbox.value))
        .join("&");

      var finalUrl = "/staff/staff_list/download?" + queryParams;
      if (columnParams) {
        finalUrl += "&" + columnParams;
      }

      console.log("Generated Download URL:", finalUrl); // Debugging
      window.location.href = finalUrl;
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  var downloadBtn = document.getElementById("download-student-excel");

  if (downloadBtn) {
    downloadBtn.addEventListener("click", function () {
      var form = document.getElementById("filter-form");

      if (!form) {
        console.error("Filter form not found!");
        return;
      }
      var queryParams = new URLSearchParams(new FormData(form)).toString();

      var columnParams = Array.from(
        document.querySelectorAll("input[name='columns']:checked")
      )
        .map((checkbox) => "columns=" + encodeURIComponent(checkbox.value))
        .join("&");

      var finalUrl = "/student/student_list/download?" + queryParams;
      if (columnParams) {
        finalUrl += "&" + columnParams;
      }

      console.log("Generated Download URL:", finalUrl); // Debugging
      window.location.href = finalUrl;
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const staffType = document.querySelector('[name="staff_type"]');
  const deptContainer = document.getElementById("dept_container");

  if (staffType) {
    staffType.addEventListener("change", function () {
      deptContainer.style.display =
        staffType.value === "Teaching" ? "flex" : "none";
    });
  } else {
    console.error("Element with name 'staff_type' not found.");
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const staffStatusDiv = document.getElementById("staffstatus");
  const staffStatus = document.querySelector('[name="status"]');

  if (staffStatus && staffStatusDiv) {
    staffStatus.addEventListener("change", function () {
      // Clear any existing dynamic fields before adding new ones
      staffStatusDiv.innerHTML = "";

      if (staffStatus.value === "Working") {
        staffStatusDiv.innerHTML = `
                    <div class="col-md-3">
                        <label for="salary">Salary</label>
                        <input type="text" name="salary" id="salary">
                    </div>`;
      } else if (staffStatus.value === "Departed") {
        staffStatusDiv.innerHTML = `
                    <div class="col-md-3">
                        <label for="date_of_exit">Date of Exit</label>
                        <input type="date" name="date_of_exit" id="date_of_exit">
                    </div>`;
      } else if (staffStatus.value === "Transferred") {
        staffStatusDiv.innerHTML = `
                    <div class="col-md-3">
                        <label for="date_of_exit">Date of Exit</label>
                        <input type="date" name="date_of_exit" id="date_of_exit">
                    </div>
                    <div class="col-md-3">
                        <label for="transferred_college_name">Transferred College Name</label>
                        <input type="text" name="transferred_college_name" id="transferred_college_name">
                    </div>`;
      }
    });
  } else {
    console.error("Element with ID 'staffstatus' or name 'status' not found.");
  }
});