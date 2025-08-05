// Initialize Mermaid
mermaid.initialize({
  startOnLoad: false,
  theme: "base",
  themeVariables: { primaryColor: "#f4f4f4", primaryTextColor: "#333" },
});

// --- Flowchart Logic ---
(function () {
  function escapeMermaidString(str) {
    if (typeof str !== "string") return str;
    return str.replace(/"/g, "#quot;");
  }

async function renderFlowchart() {
    const flowchartContainer = document.getElementById("programFlowchart");
    const errorContainer = document.getElementById("flowchartError");
    const pageConfigEl = document.getElementById("ctdtPageConfig");
    let PAGE = { ctdtPk: null, urls: {} };
    
    // Reset UI state
    errorContainer.style.display = "none";
    flowchartContainer.style.display = "block";
    flowchartContainer.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="sr-only">Đang tải sơ đồ...</span></div><p>Đang tải sơ đồ...</p></div>';

    if (pageConfigEl) {
        try {
            PAGE = JSON.parse(pageConfigEl.textContent);
        } catch (e) {
            console.error("Invalid ctdtPageConfig JSON", e);
            showError("Lỗi cấu hình trang. Vui lòng tải lại trang.");
            return;
        }
    }

    const ctdtPk = PAGE.ctdtPk;
    const url = PAGE.urls && PAGE.urls.flowchartData ? PAGE.urls.flowchartData : "";

    try {
        if (!url) {
            throw new Error("Không tìm thấy đường dẫn dữ liệu sơ đồ");
        }

        // Show loading state
        const response = await fetch(url, { credentials: "same-origin" });
        
        if (!response.ok) {
            const error = await response.json().catch(() => null);
            throw new Error(error?.message || `Lỗi máy chủ: ${response.status}`);
        }

        const data = await response.json();

        if (!data.nodes || !data.edges) {
            throw new Error("Dữ liệu sơ đồ không hợp lệ");
        }

        let mermaidSyntax = "graph TD;\n";
        
        // Add nodes
        data.nodes.forEach((node) => {
            const displayName = escapeMermaidString(node.name);
            const displayId = escapeMermaidString(node.original_id);
            // Use the prefixed ID from the API response
            mermaidSyntax += `    ${node.id}["${displayId}<br/>${displayName}"];\n`;
            if (node.khoi_kien_thuc) {
                mermaidSyntax += `    style ${node.id} ${getKhoiColor(node.khoi_kien_thuc)}\n`;
            }
        });

        // Add edges
        data.edges.forEach((edge) => {
            const arrow = edge.type === "songhanh" ? "-.->" : "-->";
            mermaidSyntax += `    ${edge.source} ${arrow} ${edge.target};\n`;
        });

        // Initialize Mermaid with error handling
        try {
            flowchartContainer.innerHTML = "";
            const { svg } = await mermaid.render("flowchartSvg", mermaidSyntax);
            flowchartContainer.innerHTML = svg;

            // Add interactivity
            const svgEl = flowchartContainer.querySelector("svg");
            if (svgEl) {
                svgEl.querySelectorAll(".node").forEach((nodeEl) => {
                    const nodeId = nodeEl.id;
                    nodeEl.addEventListener("mouseover", () => 
                        highlightNodes(nodeId, data.edges)
                    );
                    nodeEl.addEventListener("mouseout", unhighlightNodes);
                    nodeEl.addEventListener("click", () => 
                        showNodeTooltip(nodeId, data.nodes)
                    );
                });
            }
        } catch (mermaidError) {
            console.error("Mermaid rendering error:", mermaidError);
            throw new Error("Lỗi khi tạo sơ đồ. Vui lòng kiểm tra dữ liệu học phần.");
        }

    } catch (error) {
        console.error("Flowchart error:", error);
        showError(error.message);
        flowchartContainer.style.display = "none";
    }
}

function showError(message) {
    const errorContainer = document.getElementById("flowchartError");
    errorContainer.innerHTML = `
        <strong>Lỗi khi tải sơ đồ:</strong>
        <p>${message}</p>
        <button class="btn btn-sm btn-primary mt-2" onclick="renderFlowchart()">Thử lại</button>
    `;
    errorContainer.style.display = "block";
}

  function getKhoiColor(khoi) {
    const colors = {
      "Kiến thức giáo dục đại cương": "fill:#f9f9f9,stroke:#333,stroke-width:2px",
      "Kiến thức cơ sở ngành": "fill:#cde4ff,stroke:#333,stroke-width:1px",
      "Kiến thức chuyên ngành": "fill:#a3c9ff,stroke:#333,stroke-width:1px",
      "Tốt nghiệp": "fill:#ffcc80,stroke:#333,stroke-width:1px",
    };
    for (const key in colors) {
      if (khoi.includes(key)) return colors[key];
    }
    return "fill:#e9ecef,stroke:#333,stroke-width:1px";
  }

  function highlightNodes(nodeId, edges) {
    const svg = document.querySelector("#programFlowchart svg");
    if (!svg) return;
    svg.querySelectorAll(".node, .edgePath").forEach((el) => el.classList.add("dimmed"));
    const relatedNodeIds = new Set([nodeId]);
    edges.forEach((edge) => {
      if (edge.target === nodeId) relatedNodeIds.add(edge.source);
      if (edge.source === nodeId) relatedNodeIds.add(edge.target);
    });
    relatedNodeIds.forEach((id) => {
      const nodeEl = svg.querySelector(`#${id}`);
      if (nodeEl) nodeEl.classList.remove("dimmed");
    });
  }

  function unhighlightNodes() {
    const svg = document.querySelector("#programFlowchart svg");
    if (!svg) return;
    svg.querySelectorAll(".dimmed").forEach((el) => el.classList.remove("dimmed"));
  }

  function showNodeTooltip(nodeId, nodes) {
    const nodeData = nodes.find((n) => n.id === nodeId);
    if (!nodeData) return;
    alert(
      `Học phần: ${nodeData.name} (${nodeData.original_id})\nSố tín chỉ: ${nodeData.tin_chi}\nKhối kiến thức: ${nodeData.khoi_kien_thuc}`
    );
  }

  // --- Zoom Logic ---
  let currentScale = 1.5;
  const zoomStep = 0.3;

  function applyZoom() {
    const svg = document.querySelector("#programFlowchart svg");
    if (svg) {
      svg.style.transform = `scale(${currentScale})`;
      svg.style.transformOrigin = "top left";
    }
  }

  document.getElementById("zoom-in-btn").addEventListener("click", () => {
    currentScale += zoomStep;
    applyZoom();
  });

  document.getElementById("zoom-out-btn").addEventListener("click", () => {
    currentScale = Math.max(0.2, currentScale - zoomStep);
    applyZoom();
  });

  document.getElementById("reset-zoom-btn").addEventListener("click", () => {
    currentScale = 1.0;
    applyZoom();
  });

  // --- Panning (Drag-to-scroll) Logic ---
  const wrapper = document.querySelector(".flowchart-wrapper");
  if (wrapper) {
    let isDown = false;
    let startX;
    let scrollLeft;

    wrapper.addEventListener("mousedown", (e) => {
      isDown = true;
      wrapper.style.cursor = "grabbing";
      wrapper.style.userSelect = "none";
      startX = e.pageX - wrapper.offsetLeft;
      scrollLeft = wrapper.scrollLeft;
    });
    wrapper.addEventListener("mouseleave", () => {
      isDown = false;
      wrapper.style.cursor = "grab";
      wrapper.style.removeProperty("user-select");
    });
    wrapper.addEventListener("mouseup", () => {
      isDown = false;
      wrapper.style.cursor = "grab";
      wrapper.style.removeProperty("user-select");
    });
    wrapper.addEventListener("mousemove", (e) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - wrapper.offsetLeft;
      const walk = (x - startX) * 2;
      wrapper.scrollLeft = scrollLeft - walk;
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    const mapTab = document.getElementById("map-tab");
    if (mapTab) {
      $('[data-toggle="tab"]').on("shown.bs.tab", function (e) {
        if (e.target.id === "map-tab") {
          if ($("#programFlowchart").find("svg").length === 0) {
            renderFlowchart();
          }
        }
      });

      if (mapTab.classList.contains("active")) {
        renderFlowchart();
      }
    }
  });
})();

$(document).ready(function () {
  // Use the global PAGE_CONFIG that was initialized in the template
  const PAGE2 = window.PAGE_CONFIG || { ctdtPk: null, isDraft: false, csrfToken: "", urls: {} };
  var isDraft = !!PAGE2.isDraft;
  var ctdt_pk = PAGE2.ctdtPk;

  // --- Chart.js Pie Chart ---
  var pieChartCanvas = $("#creditsPieChart").get(0).getContext("2d");

  var labelsData;
  var chartData;

  // Read from the global PAGE_CONFIG
  labelsData = PAGE2.pieChart?.labels || [];
  chartData = PAGE2.pieChart?.data || [];
  
  // Filter out any null or "None" values in labels and data
  labelsData = labelsData.map((label) =>
    label === null || label === "None" ? "" : label
  );
  chartData = chartData.map((value) =>
    value === null || value === "None" || isNaN(value) ? 0 : value
  );

  var pieData = {
    labels: labelsData,
    datasets: [
      {
        data: chartData,
        backgroundColor: [
          "#f56954",
          "#00a65a",
          "#f39c12",
          "#00c0ef",
          "#3c8dbc",
          "#d2d6de",
          "#a481d0",
          "#ff851b",
          "#01ff70",
          "#39cccc",
        ],
      },
    ],
  };
  var pieOptions = {
    maintainAspectRatio: false,
    responsive: true,
    legend: {
      position: "top",
      labels: {
        padding: 10,
        boxWidth: 12,
      },
    },
  };
  new Chart(pieChartCanvas, {
    type: "pie",
    data: pieData,
    options: pieOptions,
  });

  // PO Modal Logic for adding new PO
  $('[data-target="#poModal"][data-action="add"]').on("click", function () {
    var modal = $("#poModal");
    var form = modal.find("#poForm");
    var action = $(this).data("action");

    form.attr("data-action", action);
    form[0].reset();
    modal.find(".modal-title").text("Thêm mới Mục tiêu Đào tạo");
    form.attr("action", PAGE2.urls.po.add);
    form.attr("data-pk", "");
    modal.modal("show");
  });

  $("#poForm").on("submit", function (e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr("action");
    var data = form.serialize();

    $.ajax({
      url: url,
      type: "POST",
      data: data,
      success: function (response) {
        if (response.status === "success") {
          $("#poModal").modal("hide");
          location.reload(); // Simple reload for now
        } else {
          var errorMessages = [];
          if (response.errors) {
            for (var field in response.errors) {
              errorMessages.push(`${field}: ${response.errors[field].join(", ")}`);
            }
          } else {
            errorMessages.push(response.message || "Đã có lỗi xảy ra.");
          }
          alert("Lỗi: \n" + errorMessages.join("\n"));
        }
      },
      error: function (jqXHR) {
        var errorMessage = "Lỗi kết nối hoặc lỗi máy chủ.";
        if (jqXHR.responseJSON && jqXHR.responseJSON.message) {
          errorMessage = jqXHR.responseJSON.message;
        }
        alert(errorMessage);
      },
    });
  });

  // Edit PO button click handler
  $("#poTable").on("click", ".btn-edit-po", function () {
    var pk = $(this).data("pk");
    var modal = $("#poModal");
    var form = modal.find("#poForm");

    // Set attributes for edit action
    modal.find(".modal-title").text("Cập nhật Mục tiêu Đào tạo");
    form.attr("data-action", "edit");
    form.attr("data-pk", pk);
    form.attr("action", PAGE2.urls.po.edit.replace("0", pk));
    form[0].reset();

    // Fetch PO details and populate form
    $.ajax({
      url: PAGE2.urls.po.details.replace("0", pk),
      type: "GET",
      success: function (data) {
        // Populate form with fetched data
        form.find("#id_ma_muc_tieu").val(data.ma_muc_tieu);
        form.find("#id_noi_dung").val(data.noi_dung);

        // Show the modal
        modal.modal("show");
      },
      error: function () {
        alert("Không thể tải dữ liệu Mục tiêu Đào tạo.");
      },
    });
  });

  // PLO Modal Logic
  $("#ploModal").on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget);
    var action = button ? button.data("action") : $(this).find("#ploForm").attr("data-action");
    var modal = $(this);
    var form = modal.find("#ploForm");
    form.attr("data-action", action || "add");
    form[0].reset(); // Clear form fields

    if (action === "add") {
      modal.find(".modal-title").text("Thêm mới Chuẩn Đầu ra");
      form.attr("action", PAGE2.urls.plo.add);
      form.attr("data-pk", ""); // Clear PK for add
      // Ensure checkboxes for dap_ung_muc_tieu are unchecked
      form.find('input[name="dap_ung_muc_tieu"]').prop("checked", false);
    } else if (action === "edit") {
      var pk = button ? button.data("pk") : form.attr("data-pk");
      modal.find(".modal-title").text("Cập nhật Chuẩn Đầu ra");
      form.attr("action", PAGE2.urls.plo.edit.replace("0", pk));
      form.attr("data-pk", pk);

      // Fetch PLO details and populate the form
      $.ajax({
        url: PAGE2.urls.plo.details.replace("0", pk),
        type: "GET",
        success: function (data) {
          $("#id_ma_cdr").val(data.ma_cdr);
          $("#id_noi_dung").val(data.noi_dung);
          $("#id_loai_cdr").val(data.loai_cdr);
          // Handle ManyToMany field (dap_ung_muc_tieu)
          form.find('input[name="dap_ung_muc_tieu"]').prop("checked", false); // Uncheck all first
          if (data.dap_ung_muc_tieu) {
            data.dap_ung_muc_tieu.forEach(function (po_pk) {
              form
                .find(`input[name="dap_ung_muc_tieu"][value="${po_pk}"]`)
                .prop("checked", true);
            });
          }
        },
        error: function () {
          alert("Không thể tải dữ liệu Chuẩn Đầu ra.");
        },
      });
    }
  });

  $("#ploForm").on("submit", function (e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr("action");
    var data = form.serialize();

    $.ajax({
      url: url,
      type: "POST",
      data: data,
      success: function (response) {
        if (response.status === "success") {
          $("#ploModal").modal("hide");
          location.reload(); // Simple reload for now
        } else {
          var errorMessages = [];
          if (response.errors) {
            for (var field in response.errors) {
              errorMessages.push(`${field}: ${response.errors[field].join(", ")}`);
            }
          } else {
            errorMessages.push(response.message || "Đã có lỗi xảy ra.");
          }
          alert("Lỗi: \n" + errorMessages.join("\n"));
        }
      },
      error: function (jqXHR) {
        var errorMessage = "Lỗi kết nối hoặc lỗi máy chủ.";
        if (jqXHR.responseJSON && jqXHR.responseJSON.message) {
          errorMessage = jqXHR.responseJSON.message;
        }
        alert(errorMessage);
      },
    });
  });

  // Edit PLO button click handler
  $("#plo-sub-pane").on("click", ".btn-edit-plo", function () {
    var pk = $(this).data("pk");
    var modal = $("#ploModal");
    var form = modal.find("#ploForm");

    modal.find(".modal-title").text("Cập nhật Chuẩn Đầu ra");
    form.attr("data-action", "edit");
    form.attr("data-pk", pk);
    // Manually trigger the show event logic
    modal.trigger("show.bs.modal");
    modal.modal("show");
  });

  // Delete PO
  $("#poTable").on("click", ".btn-delete-po", function () {
    var pk = $(this).data("pk");
    if (confirm("Bạn có chắc chắn muốn xóa mục tiêu này?")) {
      $.ajax({
        url: PAGE2.urls.po.delete.replace("0", pk),
        type: "POST",
        data: { csrfmiddlewaretoken: PAGE2.csrfToken },
        success: function (response) {
          if (response.status === "success") {
            location.reload();
          } else {
            alert("Lỗi: " + response.message);
          }
        },
      });
    }
  });

  // Delete PLO
  $("#plo-sub-pane").on("click", ".btn-delete-plo", function () {
    var pk = $(this).data("pk");
    if (confirm("Bạn có chắc chắn muốn xóa chuẩn đầu ra này?")) {
      $.ajax({
        url: PAGE2.urls.plo.delete.replace("0", pk),
        type: "POST",
        data: { csrfmiddlewaretoken: PAGE2.csrfToken },
        success: function (response) {
          if (response.status === "success") {
            location.reload();
          } else {
            alert("Lỗi: " + response.message);
          }
        },
      });
    }
  });

  // Activate tab based on URL hash and save tab state in localStorage
  var hash = window.location.hash;
  var activeTab = localStorage.getItem("activeCtdtTab");

  function activateTab(tabId) {
    var tabButton = $('.nav-tabs button[data-target="' + tabId + '"]');
    if (tabButton.length) {
      tabButton.tab("show");
    }
  }

  if (hash) {
    setTimeout(function () {
      activateTab(hash);
    }, 100);
  } else if (activeTab) {
    setTimeout(function () {
      activateTab(activeTab);
    }, 100);
  } else {
    // Default to first tab if none saved
    setTimeout(function () {
      $(".nav-tabs button").first().tab("show");
    }, 100);
  }

  // Save tab state on tab change
  $('[data-toggle="tab"]').on("shown.bs.tab", function (e) {
    var target = $(e.target).data("target");
    if (target) {
      localStorage.setItem("activeCtdtTab", target);
    }
  });

  // --- Staff Tab Logic ---
  function loadAvailableLecturers(searchTerm = "") {
    if (!PAGE2 || !PAGE2.urls || !PAGE2.urls.staff || !PAGE2.urls.staff.searchAvailable) {
      console.warn("PAGE2.urls.staff.searchAvailable is not defined");
      return;
    }
    const url = `${PAGE2.urls.staff.searchAvailable}?q=${encodeURIComponent(searchTerm)}`;
    $("#available-lecturers").html(
      '<p class="text-center"><i class="fas fa-spinner fa-spin"></i> Đang tải...</p>'
    );
    $.get(url, function (data) {
      $("#available-lecturers").html(data);
    }).fail(function (jqXHR) {
      const snippet = (jqXHR.responseText || "").slice(0, 200);
      $("#available-lecturers").html(
        `<p class="text-danger">Không thể tải danh sách GV chưa tham gia. HTTP ${jqXHR.status}. ${snippet}</p>`
      );
    });
  }

  function loadAssignedLecturers(searchTerm = "") {
    if (!PAGE2 || !PAGE2.urls || !PAGE2.urls.staff || !PAGE2.urls.staff.assigned) {
      console.warn("PAGE2.urls.staff.assigned is not defined");
      return;
    }
    const url = `${PAGE2.urls.staff.assigned}?q=${encodeURIComponent(searchTerm)}`;
    $("#assigned-lecturers").html(
      '<p class="text-center"><i class="fas fa-spinner fa-spin"></i> Đang tải...</p>'
    );
    $.get(url, function (data) {
      $("#assigned-lecturers").html(data);
    }).fail(function (jqXHR) {
      const snippet = (jqXHR.responseText || "").slice(0, 200);
      $("#assigned-lecturers").html(
        `<p class="text-danger">Không thể tải danh sách GV đã tham gia. HTTP ${jqXHR.status}. ${snippet}</p>`
      );
    });
  }

  // Initial load when tab is shown
  $('button[data-target="#staff-pane"]').on("shown.bs.tab", function () {
    loadAvailableLecturers();
    loadAssignedLecturers();
  });

  // Handle search for available lecturers
  let availableSearchTimeout;
  $("#staff-pane").on("keyup", "#giangvien-search-available", function () {
    clearTimeout(availableSearchTimeout);
    const searchTerm = $(this).val();
    availableSearchTimeout = setTimeout(
      () => loadAvailableLecturers(searchTerm),
      300
    );
  });

  // Handle search for assigned lecturers
  let assignedSearchTimeout;
  $("#staff-pane").on("keyup", "#giangvien-search-assigned", function () {
    clearTimeout(assignedSearchTimeout);
    const searchTerm = $(this).val();
    assignedSearchTimeout = setTimeout(
      () => loadAssignedLecturers(searchTerm),
      300
    );
  });

  // --- Staff Tab Logic (Consolidated Event Handler) ---
  $("#staff-pane").on("click", ".btn-add-gv, .btn-remove-gv, .btn-phan-cong", function (e) {
    e.preventDefault();
    const button = $(this);

    if (button.hasClass("btn-add-gv") || button.hasClass("btn-remove-gv")) {
      const gvPk = button.data("gv-pk");
      const action = button.hasClass("btn-add-gv") ? "add" : "remove";
      const url = PAGE2.urls.staff.update;
      const csrfToken = PAGE2.csrfToken;

      $.ajax({
        url: url,
        type: "POST",
        data: {
          giang_vien_pk: gvPk,
          action: action,
          csrfmiddlewaretoken: csrfToken,
        },
        dataType: "json",
        success: function (response) {
          if (response.status === "success") {
            toastr.success(response.message);
            if (action === "add") {
              button.closest('.list-group-item').remove();
              $("#assigned-lecturers").append(response.lecturer_html);
            } else { // action === "remove"
              // Remove from assigned list by traversing from the button
              button.closest('.list-group-item').remove();
              // Add to available list
              $("#available-lecturers").append(response.lecturer_html);
            }
          } else {
            toastr.error("Lỗi: " + response.message);
          }
        },
        error: function () {
          toastr.error("Đã có lỗi xảy ra khi thực hiện thao tác.");
        },
      });
    } else if (button.hasClass("btn-phan-cong")) {
      const gvPk = button.data("gv-pk");
      const gvName = button.data("gv-name");
      const url = PAGE2.urls.staff.getPhanCongForm.replace("0", gvPk);

      $("#modalGvName").text(gvName);
      $("#phanCongModalBody").html('<p class="text-center"><i class="fas fa-spinner fa-spin"></i> Đang tải...</p>');
      $("#phanCongModal").modal("show");

      $.get(url, function (data) {
        $("#phanCongModalBody").html(data);
      }).fail(function () {
        $("#phanCongModalBody").html('<p class="text-danger">Không thể tải được dữ liệu phân công.</p>');
      });
    }
  });

  // --- Phan Cong Modal Save Logic ---
  $("#savePhanCongBtn").on("click", function () {
    const form = $("#phanCongForm");
    if (!PAGE2 || !PAGE2.urls || !PAGE2.urls.staff || !PAGE2.urls.staff.savePhanCong) {
      toastr.error("Thiếu URL lưu phân công.");
      return;
    }
    const url = PAGE2.urls.staff.savePhanCong;
    const data = form.serialize();

    $.post(url, data)
      .done(function (response) {
        if (response.status === "success") {
          toastr.success(response.message);
          $("#phanCongModal").modal("hide");
          // Dynamically update the assigned courses list
          $(`#assigned-courses-${response.giang_vien_pk}`).html(
            response.updated_courses_html
          );
        } else {
          toastr.error("Lỗi: " + response.message);
        }
      })
      .fail(function () {
        toastr.error("Đã có lỗi xảy ra khi lưu phân công.");
      });
  });

  // --- Syllabus Modal Logic ---
  $("#deCuongChiTietModal").on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget);
    var hocPhanPk = button.data("hoc-phan-pk");
    var modal = $(this);
    var contentArea = modal.find("#modal-content-area");
    var loadingIndicator = modal.find("#modal-loading");
    var errorArea = modal.find("#modal-error");

    // Reset state
    loadingIndicator.show();
    contentArea.hide().empty();
    errorArea.hide();

    var url = PAGE2.urls.syllabus.details.replace("0", hocPhanPk);

    $.ajax({
      url: url,
      type: "GET",
      success: function (data) {
        loadingIndicator.hide();

        var html =
          `
          <h4>${data.ma_hoc_phan} - ${data.ten_hoc_phan}</h4>
          <p class="text-muted">
            <strong>Số tín chỉ:</strong> ${data.so_tin_chi} |
            <strong>Đơn vị quản lý:</strong> ${data.don_vi_quan_ly} |
            <strong>Phiên bản:</strong> ${data.ten_de_cuong_phien_ban} (${data.ngay_ban_hanh})
          </p>
          <hr>

          <h5>1. Mục tiêu học phần</h5>
          <p>${data.muc_tieu_hoc_phan || "Chưa có"}</p>

          <h5>2. Chuẩn đầu ra học phần (CLO)</h5>
          ` +
          (data.chuan_dau_ra.length > 0
            ? `
            <table class="table table-sm table-bordered">
              <thead><tr><th>Mã CLO</th><th>Nội dung</th><th>Mức độ Bloom</th></tr></thead>
              <tbody>
                ${data.chuan_dau_ra
                  .map(
                    (clo) => `
                  <tr>
                    <td>${clo.ma_clo}</td>
                    <td>${clo.noi_dung}</td>
                    <td>${clo.muc_do_bloom}</td>
                  </tr>
                `
                  )
                  .join("")}
              </tbody>
            </table>
          `
            : "<p>Chưa có chuẩn đầu ra.</p>") +
          `
          <h5>3. Tóm tắt nội dung</h5>
          <p>${data.tom_tat_noi_dung || "Chưa có"}</p>

          <h5>4. Nội dung chi tiết</h5>
          ` +
          (data.noi_dung_chi_tiet.length > 0
            ? `
            <table class="table table-sm table-bordered">
              <thead><tr><th>Tuần/Chủ đề</th><th>Nội dung</th><th>Giờ LT</th><th>Giờ TH</th><th>Giờ Tự học</th><th>CLO liên quan</th></tr></thead>
              <tbody>
                ${data.noi_dung_chi_tiet
                  .map(
                    (nd) => `
                  <tr>
                    <td>${nd.tuan_hoc_hoac_chu_de}</td>
                    <td>${nd.noi_dung_giang_day}</td>
                    <td>${nd.so_gio_ly_thuyet}</td>
                    <td>${nd.so_gio_thuc_hanh}</td>
                    <td>${nd.so_gio_tu_hoc}</td>
                    <td>${nd.chuan_dau_ra_lien_quan.join(", ")}</td>
                  </tr>
                `
                  )
                  .join("")}
              </tbody>
            </table>
          `
            : "<p>Chưa có nội dung chi tiết.</p>") +
          `
          <h5>5. Đánh giá học phần</h5>
          ` +
          (data.hinh_thuc_danh_gia.length > 0
            ? `
            <table class="table table-sm table-bordered">
              <thead><tr><th>Hình thức</th><th>Loại</th><th>Tỷ lệ (%)</th><th>CLO được đánh giá</th></tr></thead>
              <tbody>
                ${data.hinh_thuc_danh_gia
                  .map(
                    (dg) => `
                  <tr>
                    <td>${dg.ten_hinh_thuc}</td>
                    <td>${dg.loai_danh_gia}</td>
                    <td>${dg.ty_le_diem}</td>
                    <td>${dg.chuan_dau_ra_danh_gia.join(", ")}</td>
                  </tr>
                `
                  )
                  .join("")}
              </tbody>
            </table>
          `
            : "<p>Chưa có hình thức đánh giá.</p>") +
          `
          <h5>6. Tài liệu học tập</h5>
          <p>${data.tai_lieu_hoc_tap || "Chưa có"}</p>
        `;

        contentArea.html(html).show();
      },
      error: function (jqXHR, textStatus, errorThrown) {
        loadingIndicator.hide();
        var errorMessage = "Không thể tải được đề cương chi tiết. ";
        if (jqXHR.status == 404) {
          errorMessage += "Không tìm thấy phiên bản đề cương hiện hành cho học phần này.";
        } else {
          errorMessage += "Lỗi máy chủ: " + errorThrown;
        }
        errorArea.text(errorMessage).show();
      },
    });
  });
});
