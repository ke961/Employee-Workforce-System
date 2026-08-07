"use strict";


/* =========================================================
   API Configuration
========================================================= */

const API_BASE_URL = "/api";

const STORAGE_TOKEN_KEY = "ems_access_token";
const STORAGE_ADMIN_KEY = "ems_admin";


/* =========================================================
   Application State
========================================================= */

let accessToken = localStorage.getItem(STORAGE_TOKEN_KEY);

let currentAdmin = JSON.parse(
    localStorage.getItem(STORAGE_ADMIN_KEY) || "null"
);


/* =========================================================
   DOM Elements
========================================================= */

const loginPage = document.getElementById("loginPage");
const dashboardPage = document.getElementById("dashboardPage");

const loginForm = document.getElementById("loginForm");
const loginMessage = document.getElementById("loginMessage");

const logoutButton = document.getElementById("logoutButton");

const menuItems = document.querySelectorAll(".menu-item");
const contentSections = document.querySelectorAll(".content-section");
const pageTitle = document.getElementById("pageTitle");

const headerAdminName = document.getElementById(
    "headerAdminName"
);

const headerAdminEmail = document.getElementById(
    "headerAdminEmail"
);

const welcomeAdminName = document.getElementById(
    "welcomeAdminName"
);


/* =========================================================
   Dashboard Elements
========================================================= */

const dashboardAttendanceStatus = document.getElementById(
    "dashboardAttendanceStatus"
);

const dashboardWorkTime = document.getElementById(
    "dashboardWorkTime"
);

const dashboardLeaveBalance = document.getElementById(
    "dashboardLeaveBalance"
);

const dashboardPendingLeave = document.getElementById(
    "dashboardPendingLeave"
);

const dashboardOnboardingProgress = document.getElementById(
    "dashboardOnboardingProgress"
);

const dashboardOnboardingTasks = document.getElementById(
    "dashboardOnboardingTasks"
);

const dashboardOkrProgress = document.getElementById(
    "dashboardOkrProgress"
);

const dashboardOkrCount = document.getElementById(
    "dashboardOkrCount"
);


/* =========================================================
   Attendance Elements
========================================================= */

const clockInButton = document.getElementById("clockInButton");
const clockOutButton = document.getElementById("clockOutButton");

const attendanceStatus = document.getElementById(
    "attendanceStatus"
);

const attendanceTableBody = document.getElementById(
    "attendanceTableBody"
);


/* =========================================================
   Leave Elements
========================================================= */

const leaveForm = document.getElementById("leaveForm");

const leaveType = document.getElementById("leaveType");
const leaveStartDate = document.getElementById(
    "leaveStartDate"
);

const leaveEndDate = document.getElementById(
    "leaveEndDate"
);

const leaveReason = document.getElementById("leaveReason");

const leaveTableBody = document.getElementById(
    "leaveTableBody"
);


/* =========================================================
   Onboarding Elements
========================================================= */

const onboardingForm = document.getElementById(
    "onboardingForm"
);

const taskTitle = document.getElementById("taskTitle");
const taskDueDate = document.getElementById("taskDueDate");

const taskDescription = document.getElementById(
    "taskDescription"
);

const onboardingTaskList = document.getElementById(
    "onboardingTaskList"
);

const createDefaultTasksButton = document.getElementById(
    "createDefaultTasksButton"
);


/* =========================================================
   OKR Elements
========================================================= */

const okrForm = document.getElementById("okrForm");

const okrObjective = document.getElementById(
    "okrObjective"
);

const okrKeyResult = document.getElementById(
    "okrKeyResult"
);

const okrQuarter = document.getElementById("okrQuarter");
const okrProgress = document.getElementById("okrProgress");

const okrList = document.getElementById("okrList");


/* =========================================================
   Profile Elements
========================================================= */

const profileForm = document.getElementById("profileForm");

const profileName = document.getElementById("profileName");
const profileEmail = document.getElementById("profileEmail");

const profileJobTitle = document.getElementById(
    "profileJobTitle"
);

const profileDepartment = document.getElementById(
    "profileDepartment"
);

const profilePhone = document.getElementById("profilePhone");


/* =========================================================
   API Request Helper
========================================================= */

async function apiRequest(
    endpoint,
    options = {}
) {
    const requestOptions = {
        method: options.method || "GET",
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    };

    if (accessToken) {
        requestOptions.headers.Authorization =
            `Bearer ${accessToken}`;
    }

    if (options.body !== undefined) {
        requestOptions.body = JSON.stringify(options.body);
    }

    let response;

    try {
        response = await fetch(
            `${API_BASE_URL}${endpoint}`,
            requestOptions
        );
    } catch (error) {
        throw new Error(
            "Cannot connect to the backend server."
        );
    }

    let responseData = null;

    const responseText = await response.text();

    if (responseText) {
        try {
            responseData = JSON.parse(responseText);
        } catch (error) {
            responseData = {
                detail: responseText
            };
        }
    }

    if (!response.ok) {
        if (response.status === 401) {
            clearAuthentication();
            showLoginPage();
        }

        throw new Error(
            extractErrorMessage(
                responseData,
                response.status
            )
        );
    }

    return responseData;
}


/* =========================================================
   Error Processing
========================================================= */

function extractErrorMessage(
    responseData,
    statusCode
) {
    if (!responseData) {
        return `Request failed with status ${statusCode}.`;
    }

    if (typeof responseData.detail === "string") {
        return responseData.detail;
    }

    if (Array.isArray(responseData.detail)) {
        return responseData.detail
            .map((item) => {
                const location = Array.isArray(item.loc)
                    ? item.loc.join(" → ")
                    : "field";

                return `${location}: ${item.msg}`;
            })
            .join(", ");
    }

    if (typeof responseData.message === "string") {
        return responseData.message;
    }

    return `Request failed with status ${statusCode}.`;
}


/* =========================================================
   Authentication Storage
========================================================= */

function saveAuthentication(
    token,
    admin
) {
    accessToken = token;
    currentAdmin = admin;

    localStorage.setItem(
        STORAGE_TOKEN_KEY,
        token
    );

    localStorage.setItem(
        STORAGE_ADMIN_KEY,
        JSON.stringify(admin)
    );
}


function clearAuthentication() {
    accessToken = null;
    currentAdmin = null;

    localStorage.removeItem(STORAGE_TOKEN_KEY);
    localStorage.removeItem(STORAGE_ADMIN_KEY);
}


/* =========================================================
   Page Display
========================================================= */

function showLoginPage() {
    loginPage.classList.remove("hidden");
    dashboardPage.classList.add("hidden");
}


function showDashboardPage() {
    loginPage.classList.add("hidden");
    dashboardPage.classList.remove("hidden");
}


function showSection(sectionId) {
    contentSections.forEach((section) => {
        section.classList.add("hidden");
    });

    const selectedSection = document.getElementById(
        sectionId
    );

    if (selectedSection) {
        selectedSection.classList.remove("hidden");
    }

    menuItems.forEach((item) => {
        item.classList.remove("active");

        if (item.dataset.section === sectionId) {
            item.classList.add("active");
        }
    });

    const titleMap = {
        dashboardSection: "Dashboard",
        attendanceSection: "Attendance",
        leaveSection: "Leave",
        onboardingSection: "Onboarding",
        okrSection: "Objectives and Key Results",
        profileSection: "Profile"
    };

    pageTitle.textContent =
        titleMap[sectionId] || "Dashboard";

    loadSectionData(sectionId);
}


/* =========================================================
   Section Data Loader
========================================================= */

async function loadSectionData(sectionId) {
    try {
        switch (sectionId) {
            case "dashboardSection":
                await loadDashboard();
                break;

            case "attendanceSection":
                await loadAttendance();
                break;

            case "leaveSection":
                await loadLeaveRequests();
                break;

            case "onboardingSection":
                await loadOnboardingTasks();
                break;

            case "okrSection":
                await loadOkrs();
                break;

            case "profileSection":
                await loadProfile();
                break;

            case "tasksSection":
                await loadTasks();
                break;

            case "announcementsSection":
                await loadAnnouncements();
                break;

            case "payrollSection":
                await loadPayrollAndExpenses();
                break;

            default:
                break;
        }
    } catch (error) {
        showNotification(
            error.message,
            "error"
        );
    }
}


/* =========================================================
   Login
========================================================= */

loginForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        loginMessage.textContent = "Signing in...";
        loginMessage.className = "message";

        const email = document
            .getElementById("email")
            .value
            .trim()
            .toLowerCase();

        const password = document
            .getElementById("password")
            .value;

        try {
            const response = await apiRequest(
                "/auth/login",
                {
                    method: "POST",
                    body: {
                        email,
                        password
                    }
                }
            );

            saveAuthentication(
                response.access_token,
                response.admin
            );

            loginMessage.textContent =
                "Login successful.";

            loginMessage.className =
                "message success";

            updateAdminInformation(
                response.admin
            );

            showDashboardPage();
            showSection("dashboardSection");

        } catch (error) {
            loginMessage.textContent =
                error.message;

            loginMessage.className =
                "message error";
        }
    }
);


/* =========================================================
   Logout
========================================================= */

logoutButton.addEventListener(
    "click",
    async () => {
        try {
            await apiRequest(
                "/auth/logout",
                {
                    method: "POST"
                }
            );
        } catch (error) {
            console.warn(error.message);
        } finally {
            clearAuthentication();
            showLoginPage();

            loginMessage.textContent =
                "You have logged out.";

            loginMessage.className =
                "message success";
        }
    }
);


/* =========================================================
   Sidebar Navigation
========================================================= */

menuItems.forEach((item) => {
    item.addEventListener(
        "click",
        () => {
            showSection(item.dataset.section);
        }
    );
});


/* =========================================================
   User Profile Information
========================================================= */

function updateAdminInformation(admin) {
    if (!admin) {
        return;
    }

    currentAdmin = admin;

    localStorage.setItem(
        STORAGE_ADMIN_KEY,
        JSON.stringify(admin)
    );

    const initial = (admin.full_name || admin.email || "U").charAt(0).toUpperCase();
    const sidebarAvatar = document.getElementById("sidebarAvatar");
    const topAvatar = document.getElementById("topAvatar");
    const pageEyebrow = document.getElementById("pageEyebrow");

    if (sidebarAvatar) sidebarAvatar.textContent = initial;
    if (topAvatar) topAvatar.textContent = initial;

    if (pageEyebrow) {
        pageEyebrow.textContent = `${(admin.job_title || "User").toUpperCase()} WORKSPACE`;
    }

    if (headerAdminName) {
        headerAdminName.textContent = admin.full_name || "User";
    }

    if (headerAdminEmail) {
        headerAdminEmail.textContent = admin.email || "";
    }

    if (welcomeAdminName) {
        welcomeAdminName.textContent = admin.full_name || "User";
    }

    if (profileName) {
        profileName.value = admin.full_name || "";
    }

    if (profileEmail) {
        profileEmail.value = admin.email || "";
    }

    if (profileJobTitle) {
        profileJobTitle.value = admin.job_title || "";
    }

    if (profileDepartment) {
        profileDepartment.value = admin.department || "";
    }

    if (profilePhone) {
        profilePhone.value = admin.phone || "";
    }
}


/* =========================================================
   Load Current Profile
========================================================= */

async function loadProfile() {
    const admin = await apiRequest("/auth/me");

    updateAdminInformation(admin);
}


/* =========================================================
   Update Profile
========================================================= */

profileForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        const payload = {
            full_name: profileName.value.trim(),
            email: profileEmail.value
                .trim()
                .toLowerCase(),
            job_title:
                profileJobTitle.value.trim() || null,
            department:
                profileDepartment.value.trim() || null,
            phone:
                profilePhone.value.trim() || null
        };

        try {
            const updatedAdmin = await apiRequest(
                "/auth/me",
                {
                    method: "PATCH",
                    body: payload
                }
            );

            updateAdminInformation(updatedAdmin);

            showNotification(
                "Profile updated successfully.",
                "success"
            );

        } catch (error) {
            showNotification(
                error.message,
                "error"
            );
        }
    }
);


/* =========================================================
   Dashboard
========================================================= */

async function loadDashboard() {
    const dashboard = await apiRequest(
        "/dashboard"
    );

    if (dashboard.profile) {
        const updatedAdmin = {
            ...currentAdmin,
            ...dashboard.profile
        };

        updateAdminInformation(updatedAdmin);
    }

    const attendance =
        dashboard.attendance || {};

    dashboardAttendanceStatus.textContent =
        attendance.is_clocked_in
            ? "Clocked in"
            : "Not clocked in";

    dashboardWorkTime.textContent =
        `${attendance.total_work_minutes || 0} minutes worked`;

    const leave = dashboard.leave || {};

    dashboardLeaveBalance.textContent =
        `${leave.available_leave_balance || 0} days`;

    dashboardPendingLeave.textContent =
        `${leave.pending_requests || 0} pending requests`;

    const onboarding =
        dashboard.onboarding || {};

    dashboardOnboardingProgress.textContent =
        `${onboarding.progress_percentage || 0}%`;

    dashboardOnboardingTasks.textContent =
        `${onboarding.completed_tasks || 0} of ` +
        `${onboarding.total_tasks || 0} tasks completed`;

    const okrs = dashboard.okrs || {};

    dashboardOkrProgress.textContent =
        `${okrs.average_progress || 0}%`;

    dashboardOkrCount.textContent =
        `${okrs.in_progress_okrs || 0} active OKRs`;

    try {
        const tasks = await apiRequest("/tasks");
        const activeTasks = tasks.filter(t => t.status !== "completed").length;
        const taskCountEl = document.getElementById("dashboardTaskCount");
        const taskNoteEl = document.getElementById("dashboardTaskNote");
        if (taskCountEl) taskCountEl.textContent = activeTasks;
        if (taskNoteEl) taskNoteEl.textContent = `${activeTasks} tasks pending`;
    } catch (e) {
        console.warn("Failed to load task dashboard stat", e);
    }

    try {
        const expenses = await apiRequest("/expenses");
        const pendingClaims = expenses.filter(e => e.status === "pending");
        const totalPendingAmt = pendingClaims.reduce((sum, e) => sum + e.amount, 0);
        const expCountEl = document.getElementById("dashboardExpenseCount");
        const expNoteEl = document.getElementById("dashboardExpenseNote");
        if (expCountEl) expCountEl.textContent = `$${totalPendingAmt.toLocaleString()}`;
        if (expNoteEl) expNoteEl.textContent = `${pendingClaims.length} pending claims`;
    } catch (e) {
        console.warn("Failed to load expense dashboard stat", e);
    }
}


/* =========================================================
   Attendance Status
========================================================= */

async function loadAttendanceStatus() {
    const statusData = await apiRequest(
        "/attendance/status"
    );

    const isClockedIn =
        Boolean(
            statusData.is_clocked_in ??
            statusData.clocked_in
        );

    attendanceStatus.textContent =
        isClockedIn
            ? "Clocked in"
            : "Not clocked in";

    clockInButton.disabled = isClockedIn;
    clockOutButton.disabled = !isClockedIn;
}


/* =========================================================
   Attendance History
========================================================= */

async function loadAttendance() {
    await loadAttendanceStatus();

    const response = await apiRequest(
        "/attendance"
    );

    const records = normalizeListResponse(
        response,
        [
            "records",
            "attendance",
            "items",
            "data"
        ]
    );

    renderAttendanceRecords(records);
}


function renderAttendanceRecords(records) {
    if (!records.length) {
        attendanceTableBody.innerHTML = `
            <tr>
                <td colspan="5">
                    No attendance records found.
                </td>
            </tr>
        `;

        return;
    }

    attendanceTableBody.innerHTML = records
        .map((record) => {
            return `
                <tr>
                    <td>
                        ${escapeHtml(
                            formatDate(
                                record.attendance_date
                            )
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            formatTime(
                                record.clock_in
                            )
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            formatTime(
                                record.clock_out
                            )
                        )}
                    </td>

                    <td>
                        ${Number(
                            record.total_work_minutes || 0
                        )} minutes
                    </td>

                    <td>
                        ${createStatusBadge(
                            record.status || "present"
                        )}
                    </td>
                </tr>
            `;
        })
        .join("");
}


/* =========================================================
   Clock In
========================================================= */

clockInButton.addEventListener(
    "click",
    async () => {
        clockInButton.disabled = true;

        try {
            await apiRequest(
                "/attendance/clock-in",
                {
                    method: "POST",
                    body: {}
                }
            );

            showNotification(
                "Clocked in successfully.",
                "success"
            );

            await loadAttendance();
            await loadDashboard();

        } catch (error) {
            clockInButton.disabled = false;

            showNotification(
                error.message,
                "error"
            );
        }
    }
);


/* =========================================================
   Clock Out
========================================================= */

clockOutButton.addEventListener(
    "click",
    async () => {
        clockOutButton.disabled = true;

        try {
            await apiRequest(
                "/attendance/clock-out",
                {
                    method: "PATCH",
                    body: {}
                }
            );

            showNotification(
                "Clocked out successfully.",
                "success"
            );

            await loadAttendance();
            await loadDashboard();

        } catch (error) {
            clockOutButton.disabled = false;

            showNotification(
                error.message,
                "error"
            );
        }
    }
);


/* =========================================================
   Leave Request Submission
========================================================= */

leaveForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        if (
            leaveEndDate.value <
            leaveStartDate.value
        ) {
            showNotification(
                "End date cannot be earlier than start date.",
                "error"
            );

            return;
        }

        const payload = {
            leave_type: leaveType.value,
            start_date: leaveStartDate.value,
            end_date: leaveEndDate.value,
            reason: leaveReason.value.trim()
        };

        try {
            await apiRequest(
                "/leave",
                {
                    method: "POST",
                    body: payload
                }
            );

            leaveForm.reset();
            setDefaultFormDates();

            showNotification(
                "Leave request submitted successfully.",
                "success"
            );

            await loadLeaveRequests();
            await loadDashboard();

        } catch (error) {
            showNotification(
                error.message,
                "error"
            );
        }
    }
);


/* =========================================================
   Load Leave Requests
========================================================= */

async function loadLeaveRequests() {
    const response = await apiRequest("/leave");

    const requests = normalizeListResponse(
        response,
        [
            "leave_requests",
            "requests",
            "items",
            "data"
        ]
    );

    renderLeaveRequests(requests);
}


function renderLeaveRequests(requests) {
    if (!requests.length) {
        leaveTableBody.innerHTML = `
            <tr>
                <td colspan="6">
                    No leave requests found.
                </td>
            </tr>
        `;

        return;
    }

    leaveTableBody.innerHTML = requests
        .map((request) => {
            const status =
                request.status || "pending";

            const canCancel =
                status.toLowerCase() === "pending";

            return `
                <tr>
                    <td>
                        ${escapeHtml(
                            formatText(
                                request.leave_type
                            )
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            formatDate(
                                request.start_date
                            )
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            formatDate(
                                request.end_date
                            )
                        )}
                    </td>

                    <td>
                        ${Number(
                            request.total_days || 0
                        )}
                    </td>

                    <td>
                        ${createStatusBadge(status)}
                    </td>

                    <td>
                        ${
                            canCancel
                                ? `
                                    <button
                                        class="small-button edit-button"
                                        data-leave-action="cancel"
                                        data-id="${request.id}"
                                    >
                                        Cancel
                                    </button>
                                `
                                : ""
                        }

                        <button
                            class="small-button delete-button"
                            data-leave-action="delete"
                            data-id="${request.id}"
                        >
                            Delete
                        </button>
                    </td>
                </tr>
            `;
        })
        .join("");
}


/* =========================================================
   Leave Action Handler
========================================================= */

leaveTableBody.addEventListener(
    "click",
    async (event) => {
        const button = event.target.closest(
            "[data-leave-action]"
        );

        if (!button) {
            return;
        }

        const requestId = button.dataset.id;
        const action = button.dataset.leaveAction;

        try {
            if (action === "cancel") {
                await apiRequest(
                    `/leave/${requestId}/cancel`,
                    {
                        method: "PATCH",
                        body: {}
                    }
                );

                showNotification(
                    "Leave request cancelled.",
                    "success"
                );
            }

            if (action === "delete") {
                const confirmed = window.confirm(
                    "Delete this leave request?"
                );

                if (!confirmed) {
                    return;
                }

                await apiRequest(
                    `/leave/${requestId}`,
                    {
                        method: "DELETE"
                    }
                );

                showNotification(
                    "Leave request deleted.",
                    "success"
                );
            }

            await loadLeaveRequests();
            await loadDashboard();

        } catch (error) {
            showNotification(
                error.message,
                "error"
            );
        }
    }
);


/* =========================================================
   Create Onboarding Task
========================================================= */

onboardingForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        const payload = {
            title: taskTitle.value.trim(),
            description:
                taskDescription.value.trim() || null,
            due_date:
                taskDueDate.value || null
        };

        try {
            await apiRequest(
                "/onboarding",
                {
                    method: "POST",
                    body: payload
                }
            );

            onboardingForm.reset();

            showNotification(
                "Onboarding task added.",
                "success"
            );

            await loadOnboardingTasks();
            await loadDashboard();

        } catch (error) {
            showNotification(
                error.message,
                "error"
            );
        }
    }
);


/* =========================================================
   Create Default Onboarding Tasks
========================================================= */

createDefaultTasksButton.addEventListener(
    "click",
    async () => {
        createDefaultTasksButton.disabled = true;

        try {
            await apiRequest(
                "/onboarding/defaults",
                {
                    method: "POST",
                    body: {}
                }
            );

            showNotification(
                "Default onboarding tasks created.",
                "success"
            );

            await loadOnboardingTasks();
            await loadDashboard();

        } catch (error) {
            showNotification(
                error.message,
                "error"
            );
        } finally {
            createDefaultTasksButton.disabled = false;
        }
    }
);


/* =========================================================
   Load Onboarding Tasks
========================================================= */

async function loadOnboardingTasks() {
    const response = await apiRequest(
        "/onboarding"
    );

    const tasks = normalizeListResponse(
        response,
        [
            "tasks",
            "onboarding_tasks",
            "items",
            "data"
        ]
    );

    renderOnboardingTasks(tasks);
}


function renderOnboardingTasks(tasks) {
    if (!tasks.length) {
        onboardingTaskList.innerHTML = `
            <p>No onboarding tasks found.</p>
        `;

        return;
    }

    onboardingTaskList.innerHTML = tasks
        .map((task) => {
            const completed =
                Boolean(task.is_completed);

            return `
                <article class="task-item">

                    <div class="task-item-header">
                        <div>
                            <h3>
                                ${escapeHtml(task.title)}
                            </h3>

                            <p>
                                ${escapeHtml(
                                    task.description ||
                                    "No description provided."
                                )}
                            </p>
                        </div>

                        ${createStatusBadge(
                            completed
                                ? "completed"
                                : "pending"
                        )}
                    </div>

                    <div class="task-meta">
                        <span>
                            Due:
                            ${escapeHtml(
                                formatDate(task.due_date)
                            )}
                        </span>

                        ${
                            task.completed_at
                                ? `
                                    <span>
                                        Completed:
                                        ${escapeHtml(
                                            formatDateTime(
                                                task.completed_at
                                            )
                                        )}
                                    </span>
                                `
                                : ""
                        }
                    </div>

                    <div class="task-actions">

                        <button
                            class="small-button complete-button"
                            data-task-action="toggle"
                            data-id="${task.id}"
                        >
                            ${
                                completed
                                    ? "Mark Pending"
                                    : "Mark Complete"
                            }
                        </button>

                        <button
                            class="small-button delete-button"
                            data-task-action="delete"
                            data-id="${task.id}"
                        >
                            Delete
                        </button>

                    </div>

                </article>
            `;
        })
        .join("");
}


/* =========================================================
   Onboarding Action Handler
========================================================= */

onboardingTaskList.addEventListener(
    "click",
    async (event) => {
        const button = event.target.closest(
            "[data-task-action]"
        );

        if (!button) {
            return;
        }

        const taskId = button.dataset.id;
        const action = button.dataset.taskAction;

        try {
            if (action === "toggle") {
                await apiRequest(
                    `/onboarding/${taskId}/toggle`,
                    {
                        method: "PATCH",
                        body: {}
                    }
                );

                showNotification(
                    "Task status updated.",
                    "success"
                );
            }

            if (action === "delete") {
                const confirmed = window.confirm(
                    "Delete this onboarding task?"
                );

                if (!confirmed) {
                    return;
                }

                await apiRequest(
                    `/onboarding/${taskId}`,
                    {
                        method: "DELETE"
                    }
                );

                showNotification(
                    "Onboarding task deleted.",
                    "success"
                );
            }

            await loadOnboardingTasks();
            await loadDashboard();

        } catch (error) {
            showNotification(
                error.message,
                "error"
            );
        }
    }
);


/* =========================================================
   Create OKR
========================================================= */

okrForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        const progressValue = Number(
            okrProgress.value
        );

        const payload = {
            objective: okrObjective.value.trim(),
            key_result: okrKeyResult.value.trim(),
            quarter: okrQuarter.value,
            progress: progressValue
        };

        try {
            await apiRequest(
                "/okrs",
                {
                    method: "POST",
                    body: payload
                }
            );

            okrForm.reset();
            okrProgress.value = "0";

            showNotification(
                "OKR added successfully.",
                "success"
            );

            await loadOkrs();
            await loadDashboard();

        } catch (error) {
            showNotification(
                error.message,
                "error"
            );
        }
    }
);


/* =========================================================
   Load OKRs
========================================================= */

async function loadOkrs() {
    const response = await apiRequest("/okrs");

    const okrs = normalizeListResponse(
        response,
        [
            "okrs",
            "items",
            "data"
        ]
    );

    renderOkrs(okrs);
}


function renderOkrs(okrs) {
    if (!okrs.length) {
        okrList.innerHTML = `
            <p>No OKRs found.</p>
        `;

        return;
    }

    okrList.innerHTML = okrs
        .map((okr) => {
            const progress = Math.min(
                100,
                Math.max(
                    0,
                    Number(okr.progress || 0)
                )
            );

            const status =
                okr.status ||
                getOkrStatusFromProgress(progress);

            return `
                <article class="okr-item">

                    <div class="okr-item-header">
                        <div>
                            <h3>
                                ${escapeHtml(
                                    okr.objective
                                )}
                            </h3>

                            <p>
                                ${escapeHtml(
                                    okr.key_result
                                )}
                            </p>
                        </div>

                        ${createStatusBadge(status)}
                    </div>

                    <div class="okr-meta">
                        <span>
                            Quarter:
                            ${escapeHtml(
                                okr.quarter || "Not specified"
                            )}
                        </span>
                    </div>

                    <div class="progress-wrapper">

                        <div class="progress-bar">
                            <div
                                class="progress-fill"
                                style="width: ${progress}%"
                            ></div>
                        </div>

                        <span class="progress-label">
                            ${progress}% completed
                        </span>

                    </div>

                    <div class="okr-actions">

                        <input
                            type="number"
                            min="0"
                            max="100"
                            value="${progress}"
                            data-okr-progress-input="${okr.id}"
                            aria-label="OKR progress"
                        >

                        <button
                            class="small-button edit-button"
                            data-okr-action="progress"
                            data-id="${okr.id}"
                        >
                            Update Progress
                        </button>

                        <button
                            class="small-button delete-button"
                            data-okr-action="delete"
                            data-id="${okr.id}"
                        >
                            Delete
                        </button>

                    </div>

                </article>
            `;
        })
        .join("");
}


/* =========================================================
   OKR Action Handler
========================================================= */

okrList.addEventListener(
    "click",
    async (event) => {
        const button = event.target.closest(
            "[data-okr-action]"
        );

        if (!button) {
            return;
        }

        const okrId = button.dataset.id;
        const action = button.dataset.okrAction;

        try {
            if (action === "progress") {
                const progressInput =
                    okrList.querySelector(
                        `[data-okr-progress-input="${okrId}"]`
                    );

                const progress = Number(
                    progressInput.value
                );

                if (
                    Number.isNaN(progress) ||
                    progress < 0 ||
                    progress > 100
                ) {
                    throw new Error(
                        "Progress must be between 0 and 100."
                    );
                }

                await apiRequest(
                    `/okrs/${okrId}/progress`,
                    {
                        method: "PATCH",
                        body: {
                            progress
                        }
                    }
                );

                showNotification(
                    "OKR progress updated.",
                    "success"
                );
            }

            if (action === "delete") {
                const confirmed = window.confirm(
                    "Delete this OKR?"
                );

                if (!confirmed) {
                    return;
                }

                await apiRequest(
                    `/okrs/${okrId}`,
                    {
                        method: "DELETE"
                    }
                );

                showNotification(
                    "OKR deleted.",
                    "success"
                );
            }

            await loadOkrs();
            await loadDashboard();

        } catch (error) {
            showNotification(
                error.message,
                "error"
            );
        }
    }
);


/* =========================================================
   Response List Normalizer
========================================================= */

function normalizeListResponse(
    response,
    possibleKeys = []
) {
    if (Array.isArray(response)) {
        return response;
    }

    if (!response || typeof response !== "object") {
        return [];
    }

    for (const key of possibleKeys) {
        if (Array.isArray(response[key])) {
            return response[key];
        }
    }

    return [];
}


/* =========================================================
   Formatting Helpers
========================================================= */

function formatDate(value) {
    if (!value) {
        return "Not specified";
    }

    const normalizedValue =
        value.length === 10
            ? `${value}T00:00:00`
            : value;

    const date = new Date(normalizedValue);

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return date.toLocaleDateString(
        undefined,
        {
            year: "numeric",
            month: "short",
            day: "numeric"
        }
    );
}


function formatTime(value) {
    if (!value) {
        return "—";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return date.toLocaleTimeString(
        undefined,
        {
            hour: "2-digit",
            minute: "2-digit"
        }
    );
}


function formatDateTime(value) {
    if (!value) {
        return "—";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return date.toLocaleString(
        undefined,
        {
            year: "numeric",
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit"
        }
    );
}


function formatText(value) {
    if (!value) {
        return "Not specified";
    }

    return String(value)
        .replaceAll("_", " ")
        .replace(/\b\w/g, (character) =>
            character.toUpperCase()
        );
}


function getOkrStatusFromProgress(progress) {
    if (progress >= 100) {
        return "completed";
    }

    if (progress > 0) {
        return "in_progress";
    }

    return "not_started";
}


/* =========================================================
   Status Badge
========================================================= */

function createStatusBadge(status) {
    const normalizedStatus = String(
        status || "pending"
    )
        .trim()
        .toLowerCase()
        .replaceAll(" ", "_");

    const cssStatus = normalizedStatus
        .replaceAll("_", "-");

    return `
        <span
            class="status-badge status-${escapeHtml(
                cssStatus
            )}"
        >
            ${escapeHtml(
                formatText(normalizedStatus)
            )}
        </span>
    `;
}


/* =========================================================
   HTML Escaping
========================================================= */

function escapeHtml(value) {
    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


/* =========================================================
   Notification
========================================================= */

function showNotification(
    message,
    type = "success"
) {
    const oldNotification =
        document.querySelector(".notification");

    if (oldNotification) {
        oldNotification.remove();
    }

    const notification =
        document.createElement("div");

    notification.className =
        `notification ${type}`;

    notification.textContent = message;

    document.body.appendChild(notification);

    window.setTimeout(
        () => {
            notification.remove();
        },
        3500
    );
}


/* =========================================================
   Default Form Dates
========================================================= */

function setDefaultFormDates() {
    const today = new Date();

    const year = today.getFullYear();

    const month = String(
        today.getMonth() + 1
    ).padStart(2, "0");

    const day = String(
        today.getDate()
    ).padStart(2, "0");

    const formattedDate =
        `${year}-${month}-${day}`;

    if (!leaveStartDate.value) {
        leaveStartDate.value = formattedDate;
    }

    if (!leaveEndDate.value) {
        leaveEndDate.value = formattedDate;
    }
}


/* =========================================================
   Tasks & Projects Module
========================================================= */

let currentTaskFilter = "all";

async function loadTasks() {
    const taskList = document.getElementById("taskList");
    if (!taskList) return;

    taskList.innerHTML = '<div class="empty">Loading tasks...</div>';

    const tasks = await apiRequest("/tasks");
    
    let filteredTasks = tasks;
    if (currentTaskFilter !== "all") {
        filteredTasks = tasks.filter(t => t.status === currentTaskFilter);
    }

    if (filteredTasks.length === 0) {
        taskList.innerHTML = '<div class="empty">No tasks found for this filter.</div>';
        return;
    }

    taskList.innerHTML = filteredTasks.map(task => {
        const priorityClass = `priority-${task.priority || "medium"}`;
        const dueDateStr = task.due_date ? new Date(task.due_date).toLocaleDateString() : "No due date";
        
        return `
            <div class="task-card">
                <div>
                    <div class="task-header">
                        <span class="priority-tag ${priorityClass}">${escapeHtml(task.priority)}</span>
                        <button class="btn btn-secondary" onclick="deleteTaskItem(${task.id})" style="padding: 2px 8px; font-size: 11px;">✕ Delete</button>
                    </div>
                    <h4 class="task-title">${escapeHtml(task.title)}</h4>
                    <p class="task-desc">${escapeHtml(task.description || "No description provided.")}</p>
                </div>
                <div class="task-footer">
                    <span style="font-size: 12px; color: var(--muted-color);">Due: ${escapeHtml(dueDateStr)}</span>
                    <select class="status-select" onchange="updateTaskStatusItem(${task.id}, this.value)">
                        <option value="todo" ${task.status === "todo" ? "selected" : ""}>To Do</option>
                        <option value="in_progress" ${task.status === "in_progress" ? "selected" : ""}>In Progress</option>
                        <option value="review" ${task.status === "review" ? "selected" : ""}>In Review</option>
                        <option value="completed" ${task.status === "completed" ? "selected" : ""}>Completed</option>
                    </select>
                </div>
            </div>
        `;
    }).join("");
}

async function updateTaskStatusItem(taskId, newStatus) {
    try {
        await apiRequest(`/tasks/${taskId}`, {
            method: "PATCH",
            body: { status: newStatus }
        });
        showNotification("Task status updated.", "success");
        await loadTasks();
    } catch (err) {
        showNotification(err.message, "error");
    }
}

async function deleteTaskItem(taskId) {
    if (!confirm("Are you sure you want to delete this task?")) return;
    try {
        await apiRequest(`/tasks/${taskId}`, { method: "DELETE" });
        showNotification("Task deleted.", "success");
        await loadTasks();
    } catch (err) {
        showNotification(err.message, "error");
    }
}

// Bind Task Form and Filter Tabs
document.addEventListener("DOMContentLoaded", () => {
    const taskForm = document.getElementById("taskForm");
    if (taskForm) {
        taskForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const title = document.getElementById("taskTitle").value.trim();
            const description = document.getElementById("taskDescription").value.trim();
            const priority = document.getElementById("taskPriority").value;
            const due_date = document.getElementById("taskDueDate").value || null;

            try {
                await apiRequest("/tasks", {
                    method: "POST",
                    body: { title, description: description || null, priority, due_date }
                });
                taskForm.reset();
                showNotification("Task created successfully!", "success");
                await loadTasks();
            } catch (err) {
                showNotification(err.message, "error");
            }
        });
    }

    const taskFilterTabs = document.getElementById("taskFilterTabs");
    if (taskFilterTabs) {
        taskFilterTabs.querySelectorAll(".filter-chip").forEach(btn => {
            btn.addEventListener("click", () => {
                taskFilterTabs.querySelectorAll(".filter-chip").forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
                currentTaskFilter = btn.dataset.filter;
                loadTasks();
            });
        });
    }
});


/* =========================================================
   Announcements Module
========================================================= */

async function loadAnnouncements() {
    const feed = document.getElementById("announcementFeed");
    if (!feed) return;

    feed.innerHTML = '<div class="empty">Loading announcements...</div>';

    const announcements = await apiRequest("/announcements");
    if (announcements.length === 0) {
        feed.innerHTML = '<div class="empty">No announcements published yet.</div>';
        return;
    }

    feed.innerHTML = announcements.map(item => {
        const dateStr = new Date(item.created_at).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
        const pinnedClass = item.is_pinned ? "pinned" : "";
        const pinnedBadge = item.is_pinned ? '<span class="pinned-badge">📌 PINNED</span>' : '';

        return `
            <div class="announcement-card ${pinnedClass}">
                <div class="announcement-meta">
                    <span class="category-badge">${escapeHtml(item.category)}</span>
                    ${pinnedBadge}
                    <span>By ${escapeHtml(item.author)}</span>
                    <span>•</span>
                    <span>${escapeHtml(dateStr)}</span>
                    <button class="btn btn-secondary" onclick="deleteAnnouncementItem(${item.id})" style="margin-left: auto; padding: 2px 8px; font-size: 11px;">Delete</button>
                </div>
                <h3 style="margin: 0 0 8px 0; color: var(--ink);">${escapeHtml(item.title)}</h3>
                <p style="margin: 0; color: #475569; line-height: 1.5; font-size: 14px;">${escapeHtml(item.content)}</p>
            </div>
        `;
    }).join("");
}

async function deleteAnnouncementItem(announcementId) {
    if (!confirm("Are you sure you want to remove this announcement?")) return;
    try {
        await apiRequest(`/announcements/${announcementId}`, { method: "DELETE" });
        showNotification("Announcement deleted.", "success");
        await loadAnnouncements();
    } catch (err) {
        showNotification(err.message, "error");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const announcementForm = document.getElementById("announcementForm");
    if (announcementForm) {
        announcementForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const title = document.getElementById("announcementTitle").value.trim();
            const category = document.getElementById("announcementCategory").value;
            const is_pinned = document.getElementById("announcementPinned").checked;
            const content = document.getElementById("announcementContent").value.trim();

            try {
                await apiRequest("/announcements", {
                    method: "POST",
                    body: { title, category, is_pinned, content }
                });
                announcementForm.reset();
                showNotification("Announcement published!", "success");
                await loadAnnouncements();
            } catch (err) {
                showNotification(err.message, "error");
            }
        });
    }
});


/* =========================================================
   Payroll & Expense Reimbursements Module
========================================================= */

async function loadPayrollAndExpenses() {
    const tbody = document.getElementById("expenseTableBody");
    if (!tbody) return;

    tbody.innerHTML = '<tr><td colspan="7" class="empty">Loading expense claims...</td></tr>';

    const expenses = await apiRequest("/expenses");
    if (expenses.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty">No expense claims submitted yet.</td></tr>';
        return;
    }

    tbody.innerHTML = expenses.map(item => {
        const dateStr = new Date(item.expense_date).toLocaleDateString();
        let badgeClass = "pending";
        if (item.status === "approved") badgeClass = "approved";
        if (item.status === "rejected") badgeClass = "rejected";

        return `
            <tr>
                <td>${escapeHtml(dateStr)}</td>
                <td><strong>${escapeHtml(item.category)}</strong></td>
                <td>${escapeHtml(item.merchant)}</td>
                <td style="font-weight: 700; color: var(--ink);">$${item.amount.toLocaleString()}</td>
                <td>${escapeHtml(item.description || "N/A")}</td>
                <td><span class="badge ${badgeClass}">${escapeHtml(item.status.toUpperCase())}</span></td>
                <td>
                    <div style="display: flex; gap: 4px;">
                        ${item.status === "pending" ? `
                            <button class="btn btn-secondary" onclick="updateExpenseStatusItem(${item.id}, 'approved')" style="padding: 2px 8px; font-size: 11px; color: var(--success-color);">Approve</button>
                            <button class="btn btn-secondary" onclick="updateExpenseStatusItem(${item.id}, 'rejected')" style="padding: 2px 8px; font-size: 11px; color: var(--danger-color);">Reject</button>
                        ` : ''}
                        <button class="btn btn-secondary" onclick="deleteExpenseItem(${item.id})" style="padding: 2px 6px; font-size: 11px;">✕</button>
                    </div>
                </td>
            </tr>
        `;
    }).join("");
}

async function updateExpenseStatusItem(claimId, newStatus) {
    try {
        await apiRequest(`/expenses/${claimId}/status`, {
            method: "PATCH",
            body: { status: newStatus }
        });
        showNotification(`Expense claim ${newStatus}.`, "success");
        await loadPayrollAndExpenses();
    } catch (err) {
        showNotification(err.message, "error");
    }
}

async function deleteExpenseItem(claimId) {
    if (!confirm("Are you sure you want to delete this expense claim?")) return;
    try {
        await apiRequest(`/expenses/${claimId}`, { method: "DELETE" });
        showNotification("Expense claim deleted.", "success");
        await loadPayrollAndExpenses();
    } catch (err) {
        showNotification(err.message, "error");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const expenseForm = document.getElementById("expenseForm");
    if (expenseForm) {
        expenseForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const category = document.getElementById("expenseCategory").value;
            const amount = parseInt(document.getElementById("expenseAmount").value, 10);
            const merchant = document.getElementById("expenseMerchant").value.trim();
            const expense_date = document.getElementById("expenseDate").value;
            const description = document.getElementById("expenseDescription").value.trim();

            try {
                await apiRequest("/expenses", {
                    method: "POST",
                    body: { category, amount, merchant, expense_date, description: description || null }
                });
                expenseForm.reset();
                showNotification("Expense claim submitted!", "success");
                await loadPayrollAndExpenses();
            } catch (err) {
                showNotification(err.message, "error");
            }
        });
    }
});


/* =========================================================
   Initial Application Load
========================================================= */

async function initializeApplication() {
    setDefaultFormDates();

    if (!accessToken) {
        showLoginPage();
        return;
    }

    try {
        const admin = await apiRequest("/auth/me");

        updateAdminInformation(admin);
        showDashboardPage();
        showSection("dashboardSection");

    } catch (error) {
        clearAuthentication();
        showLoginPage();

        loginMessage.textContent =
            "Your session has expired. Please log in again.";

        loginMessage.className =
            "message error";
    }
}


document.addEventListener(
    "DOMContentLoaded",
    initializeApplication
);