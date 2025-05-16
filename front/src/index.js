// "use strict";
var oDT_table1 = {}
var oDT_jobs = {}
var oDT_employees = {}

$(function () {
  const routes = {
    home: renderHome,
    form: renderForm,
    datatable_1: renderDataTable_1,
    datatable_2: renderDataTable_2,
    restore: renderRestore,

  };

  function renderHome() {
    $("#app").html(`
      <div class="text-center">
        <h1>Bienvenido a la plataforma de migración</h1>
        <p>Selecciona "Form" en el menú para migrar datos.</p>
      </div>
    `);
  }

  function renderForm() {
  const formHtml = `
      <form id="migrationForm" class="needs-validation" novalidate>
        <div class="col-lg-12">
          <div class="row align-items-center">
            <div class="mb-3 col-md-3">
              <label class="form-label">Choose a file</label>
              <input type="file" class="form-control" id="file_input" required />
              <div class="invalid-feedback">Archivo requerido.</div>
            </div>
            <div class="mb-3 col-md-3">
              <div><label class="form-label col-lg-12">Entity</label></div>
              <div class="form-check form-check-inline">
                <input id="option-employees" class="form-check-input" type="radio" name="entityOption" value="employees">
                <label for="option-employees" class="form-check-label">Employees</label>
              </div>
              <div class="form-check form-check-inline">
                <input id="option-jobs" class="form-check-input" type="radio" name="entityOption" value="jobs">
                <label for="option-jobs" class="form-check-label">Jobs</label>
              </div>
              <div class="form-check form-check-inline">
                <input id="option-departments" class="form-check-input" type="radio" name="entityOption" value="departments" checked>
                <label for="option-departments" class="form-check-label">Departments</label>
              </div>
            </div>
            <div class="mb-3 col-md-3 align-self-end"><button id="send_btn" type="submit" class="btn btn-primary">Send</button></div>
          </div>
        </div>
      </form>
      <div id="output_result" class="mt-4"></div>
    `;
  
    $("#app").html(formHtml);
  
    // Desasociar cualquier evento previo para evitar duplicados
    $("#migrationForm").off("submit");
  
    // Asociar evento
    $(document).off("submit", "#migrationForm");
    $(document).on("submit", "#migrationForm", async function (e) {
      e.preventDefault();
      e.stopPropagation();

      const form = this;
      if (!form.checkValidity()) {
        form.classList.add("was-validated");
        return;
      }

      const file = $("#file_input")[0].files[0];
      const entity = $("input[name='entityOption']:checked").val();

      const formData = new FormData();
      formData.append("file", file);
      formData.append("data", JSON.stringify({ entity }));

      try {
        const res = await fetch("http://localhost:8000/migrate", {
          method: "POST",
          body: formData
        });
        const data = await res.json();

        $("#output_result").html(`<div class="alert alert-success">${data.message}</div>`);



      } catch (error) {
        console.error(error);
        $("#output_result").html(`<div class="alert alert-danger">Error</div>`);
      }
    });
  }
  

  function renderDataTable_1() {
    const tableHtml = `

    <div class="accordion" id="accordionExample-editar-table_1">
      <div class="accordion-item">
        <div class="accordion-header p-0" id="heading-editar-ticket">
          <button class="accordion-button" type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapse-editar-table_1"
            aria-expanded="false"
            aria-controls="collapse-editar-table_1">
            <div style="font-weight: 600; font-size: 1rem;"><i
                class="fa-sharp fa-solid fa-filter me-2"></i>Filters
            </div>
          </button>
        </div>
        <div id="collapse-editar-table_1"
          class="accordion-collapse collapse show"
          aria-labelledby="heading-editar-ticket"
          data-bs-parent="#accordionExample-editar-table_1">
          <div class="accordion-body mb-1">
            <div class="cm-content-body form excerpt">
              <div class="row">
                <div class="col-xl-3 col-sm-3">
                  <label class="form-label"
                    for="year-filter">Year</label>
                  <select class="form-control"
                    id="year-filter">
                    <option value="">Select a year</option>
                    <option value="2020">2020</option>
                    <option value="2021">2021</option>
                    <option value="2022">2022</option>
                    <option value="2023">2023</option>
                    <option value="2024">2024</option>
                    <option value="2025">2025</option>
                  </select>
                </div>
                <div class="col-xl-3 col-sm-3 align-self-end">
                  <div>
                    <button
                      class="btn btn-primary filter-requests"
                      title="Search"
                      id="filtro-search">
                      <i
                        class="fa fa-search me-1"></i></button>
                    <button class="btn btn-dark light"
                      title="Click to remove filters"
                      id="clear-filter">
                        <i class="fa-solid fa-eraser"></i>
                      </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="table-responsive mt-5" id="tableResponseContainer_1">
        <table id="tableResponse_1" class="display datatable">
          <thead>
            <tr>
              <th>Department</th>
              <th>Job</th>
              <th>Q1</th>
              <th>Q2</th>
              <th>Q3</th>
              <th>Q4</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>
    `

    $("#app").html(tableHtml)

    $("#filtro-search").on("click", function () {
      getAllTable_1()
    })

    $("#clear-filter").on("click", function () {
      $("#year-filter").val("2021").trigger("change")
      getAllTable_1(2021)
    })

    const getAllTable_1 = (year = null) => {
      const yearFilter = year || $("#year-filter").val() || "2021";

      $("#tableResponse_1 tbody").html("")
      oDT_table1 = $("#tableResponse_1").DataTable({
        searching: false,
        paging: false,
        lengthChange: false, 
        info: false, 
        ajax: {
          url: `http://localhost:8000/employeesbyquarter/${yearFilter}`,
          type: "GET",
        },
        destroy: true,
        processing: true,
        serverSide: true,
        sorting: [[1, "DESC"]],
        columns: [
          {
            data: "department",
            sortable: false,
          },
          {
            data: "job",
            sortable: false,
          },
          {
            data: "q1",
            sortable: false,
          },
          {
            data: "q2",
            sortable: false,
          },
          {
            data: "q3",
            sortable: false,
          },
          {
            data: "q4",
            sortable: false,
          }
        ],
        drawCallback: function () {
          $("div.dataTables_filter input").unbind();
          oDT_table1
            .rows(".selected")
            .nodes()
            .each((row) => row.classList.remove("selected"));
        },
      })
    }

    getAllTable_1(2021)

  }


  function renderDataTable_2() {
    const tableHtml = `

    <div class="accordion" id="accordionExample-editar-table_1">
      <div class="accordion-item">
        <div class="accordion-header p-0" id="heading-editar-ticket">
          <button class="accordion-button" type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapse-editar-table_1"
            aria-expanded="false"
            aria-controls="collapse-editar-table_1">
            <div style="font-weight: 600; font-size: 1rem;"><i
                class="fa-sharp fa-solid fa-filter me-2"></i>Filters
            </div>
          </button>
        </div>
        <div id="collapse-editar-table_1"
          class="accordion-collapse collapse show"
          aria-labelledby="heading-editar-ticket"
          data-bs-parent="#accordionExample-editar-table_1">
          <div class="accordion-body mb-1">
            <div class="cm-content-body form excerpt">
              <div class="row">
                <div class="col-xl-3 col-sm-3">
                  <label class="form-label"
                    for="year-filter">Year</label>
                  <select class="form-control"
                    id="year-filter">
                    <option value="">Select a year</option>
                    <option value="2020">2020</option>
                    <option value="2021">2021</option>
                    <option value="2022">2022</option>
                    <option value="2023">2023</option>
                    <option value="2024">2024</option>
                    <option value="2025">2025</option>
                  </select>
                </div>
                <div class="col-xl-3 col-sm-3 align-self-end">
                  <div>
                    <button
                      class="btn btn-primary filter-requests"
                      title="Search"
                      id="filtro-search_2">
                      <i
                        class="fa fa-search me-1"></i></button>
                    <button class="btn btn-dark light"
                      title="Click to remove filters"
                      id="clear-filter_2">
                        <i class="fa-solid fa-eraser"></i>
                      </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="table-responsive mt-5" id="tableResponseContainer_2">
        <table id="tableResponse_2" class="display datatable">
          <thead>
            <tr>
              <th>Id</th>
              <th>Department</th>
              <th>Hired</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>
    `

    $("#app").html(tableHtml)



    $("#filtro-search_2").on("click", function () {
      getAllTable_2()
    })

    $("#clear-filter_2").on("click", function () {
      $("#year-filter_2").val("2021").trigger("change")
      getAllTable_2(2021)
    })

    const getAllTable_2 = (year = null) => {
      const yearFilter = year || $("#year-filter").val() || "2021";

      $("#tableResponse_2 tbody").html("")
      oDT_table1 = $("#tableResponse_2").DataTable({
        searching: false,
        paging: false,
        lengthChange: false, 
        info: false, 
        ajax: {
          url: `http://localhost:8000/morethanthemean/${yearFilter}`,
          type: "GET",
        },
        destroy: true,
        processing: true,
        serverSide: true,
        sorting: [[1, "DESC"]],
        columns: [
          {
            data: "department_id",
            sortable: false,
          },
          {
            data: "department_name",
            sortable: false,
          },
          {
            data: "total_hires",
            sortable: false,
          },
        ],
        drawCallback: function () {
          $("div.dataTables_filter input").unbind();
          oDT_table1
            .rows(".selected")
            .nodes()
            .each((row) => row.classList.remove("selected"));
        },
      })
    }

    getAllTable_2(2021)

  }
  

  function router() {
    const hash = location.hash.replace("#", "") || "home";
    const render = routes[hash] || renderHome;
    render();
  }

  $(window).on("hashchange", router);
  router(); // carga inicial

  // const fileInput = document.querySelector('#file_input')
  // const entity = $('input[name="entityOption"]').val()

  $('input[name="entityOption"]').on('change', function() {
    const selectedOption = $(this).val();
    console.log(selectedOption)
    if (selectedOption == 'departments') {
      $("#tableResponseDepartmentsContainer").removeClass("d-none").addClass("d-block")
      $("#tableResponseJobsContainer").removeClass("d-block").addClass("d-none")
      $("#tableResponseEmployeesContainer").removeClass("d-block").addClass("d-none")
    } else if (selectedOption == 'jobs') {
      $("#tableResponseDepartmentsContainer").removeClass("d-block").addClass("d-none")
      $("#tableResponseJobsContainer").removeClass("d-none").addClass("d-block")
      $("#tableResponseEmployeesContainer").removeClass("d-block").addClass("d-none")
      
    } else if (selectedOption == 'employees') {
      $("#tableResponseDepartmentsContainer").removeClass("d-block").addClass("d-none")
      $("#tableResponseJobsContainer").removeClass("d-block").addClass("d-none")
      $("#tableResponseEmployeesContainer").removeClass("d-none").addClass("d-block")

    }
  })

function renderRestore() {
  const formHtml = `
      <div class="alert alert-primary" role="alert">
        Use this option to restore a table from an AVRO file.
      </div>
      <form id="restoreForm" class="needs-validation" novalidate>
        <div class="col-lg-12">
          <div class="row align-items-center">
            <div class="mb-3 col-md-3">
              <label class="form-label">Choose a file</label>
              <input type="file" class="form-control" id="file_input" required />
              <div class="invalid-feedback">Archivo requerido.</div>
            </div>
            <div class="mb-3 col-md-3">
              <div><label class="form-label col-lg-12">Entity</label></div>
              <div class="form-check form-check-inline">
                <input id="option-employees" class="form-check-input" type="radio" name="entityOption" value="employees">
                <label for="option-employees" class="form-check-label">Employees</label>
              </div>
              <div class="form-check form-check-inline">
                <input id="option-jobs" class="form-check-input" type="radio" name="entityOption" value="jobs">
                <label for="option-jobs" class="form-check-label">Jobs</label>
              </div>
              <div class="form-check form-check-inline">
                <input id="option-departments" class="form-check-input" type="radio" name="entityOption" value="departments" checked>
                <label for="option-departments" class="form-check-label">Departments</label>
              </div>
            </div>
            <div class="mb-3 col-md-3 align-self-end"><button id="send_btn" type="submit" class="btn btn-primary">Send</button></div>
          </div>
        </div>
      </form>
      <div id="output_result" class="mt-4"></div>
    `;
  
    $("#app").html(formHtml);
  
    // Desasociar cualquier evento previo para evitar duplicados
    $("#restoreForm").off("submit");
  
    // Asociar evento
    $(document).off("submit", "#restoreForm");
    $(document).on("submit", "#restoreForm", async function (e) {
      e.preventDefault();
      e.stopPropagation();

      const form = this;
      if (!form.checkValidity()) {
        form.classList.add("was-validated");
        return;
      }

      const file = $("#file_input")[0].files[0];
      const entity = $("input[name='entityOption']:checked").val();

      const formData = new FormData();
      formData.append("file", file);
      formData.append("data", JSON.stringify({ entity }));

      try {
        const res = await fetch("http://localhost:8000/restore", {
          method: "POST",
          body: formData
        });
        const data = await res.json();

        $("#output_result").html(`<div class="alert alert-success">${data.message}</div>`);



      } catch (error) {
        console.error(error);
        $("#output_result").html(`<div class="alert alert-danger">Error</div>`);
      }
    });
  }

})

