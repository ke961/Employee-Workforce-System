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

const onboardingTaskTitle = document.getElementById("onboardingTaskTitle");
const onboardingTaskDueDate = document.getElementById("onboardingTaskDueDate");

const onboardingTaskDescription = document.getElementById(
    "onboardingTaskDescription"
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
        requestOptions.headers.Authorization = `Bearer ${accessToken}`;
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
        tasksSection: "Tasks & Projects",
        announcementsSection: "Company Announcements",
        payrollSection: "Payroll & Expenses",
        employeesSection: "Staff Directory",
        reviewsSection: "Performance & Peer Recognition",
        documentsSection: "Document Center",
        analyticsSection: "Analytics & Reports",
        shiftsSection: "Work Shift Roster",
        assetsSection: "IT Asset & Hardware Inventory",
        calendarSection: "Team Calendar & Events",
        trainingSection: "Training Courses & Certifications",
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

            case "employeesSection":
                await loadEmployees();
                break;

            case "reviewsSection":
                await loadReviews();
                await loadKudos();
                await populateReviewEmployeeDropdown();
                break;

            case "documentsSection":
                await loadDocuments();
                break;

            case "analyticsSection":
                await loadAnalytics();
                break;

            case "shiftsSection":
                await loadShifts();
                await populateDropdown("shiftEmployeeSelect");
                break;

            case "assetsSection":
                await loadAssets();
                await populateDropdown("assetEmployeeSelect", true);
                break;

            case "calendarSection":
                await loadCalendar();
                break;

            case "trainingSection":
                await loadTrainings();
                await populateDropdown("trainingEmployeeSelect");
                break;

            case "payslipsSection":
                await loadPayslips();
                await populateDropdown("payslipEmployeeSelect");
                await populateDropdown("payslipEmployeeFilter", true);
                break;

            case "recruitmentSection":
                await loadRecruitment();
                await populateRecruitmentJobDropdown();
                break;

            case "chatSection":
                await loadChatChannels();
                await loadChatMessages();
                break;

            case "surveysSection":
                await loadSurveysAndIdeas();
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

    await loadLandingAttendanceWorkstation();
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
   Landing Page Time Clock Workstation Module
========================================================= */

let digitalClockTimer = null;
let shiftDurationTimer = null;

function startDigitalClock() {
    if (digitalClockTimer) return;
    const timeEl = document.getElementById("digitalClockTime");
    const dateEl = document.getElementById("digitalClockDate");

    function update() {
        const now = new Date();
        if (timeEl) {
            timeEl.textContent = now.toLocaleTimeString("en-US", {
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
                hour12: true
            });
        }
        if (dateEl) {
            dateEl.textContent = now.toLocaleDateString("en-US", {
                weekday: "long",
                month: "long",
                day: "numeric",
                year: "numeric"
            });
        }
    }
    update();
    digitalClockTimer = setInterval(update, 1000);
}

function updateShiftDurationCounter(clockInIso) {
    if (shiftDurationTimer) {
        clearInterval(shiftDurationTimer);
        shiftDurationTimer = null;
    }
    const shiftTimerEl = document.getElementById("shiftTimerValue");

    if (!clockInIso) {
        if (shiftTimerEl) shiftTimerEl.textContent = "00:00:00";
        return;
    }

    const clockInDate = new Date(clockInIso);

    function tick() {
        const now = new Date();
        const diffMs = Math.max(0, now - clockInDate);
        const hours = Math.floor(diffMs / (1000 * 60 * 60));
        const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diffMs % (1000 * 60)) / 1000);

        const formatted =
            String(hours).padStart(2, "0") + ":" +
            String(minutes).padStart(2, "0") + ":" +
            String(seconds).padStart(2, "0");

        if (shiftTimerEl) shiftTimerEl.textContent = formatted;
    }
    tick();
    shiftDurationTimer = setInterval(tick, 1000);
}

async function loadLandingAttendanceWorkstation() {
    startDigitalClock();

    const badgeEl = document.getElementById("clockStationBadge");
    const badgeTextEl = document.getElementById("clockStationBadgeText");
    const landingClockInBtn = document.getElementById("landingClockInBtn");
    const landingClockOutBtn = document.getElementById("landingClockOutBtn");
    const clockInTimeEl = document.getElementById("landingClockInTime");
    const clockOutTimeEl = document.getElementById("landingClockOutTime");
    const workTimeNoteEl = document.getElementById("landingWorkTimeNote");
    const landingTableBody = document.getElementById("landingAttendanceTableBody");

    try {
        const statusData = await apiRequest("/attendance/status");
        const isClockedIn = Boolean(statusData.is_clocked_in ?? statusData.clocked_in);

        if (badgeEl && badgeTextEl) {
            if (isClockedIn) {
                badgeEl.className = "status-chip working";
                badgeTextEl.textContent = "CLOCKED IN & WORKING";
            } else {
                badgeEl.className = "status-chip offline";
                badgeTextEl.textContent = "NOT CLOCKED IN";
            }
        }

        if (landingClockInBtn) landingClockInBtn.disabled = isClockedIn;
        if (landingClockOutBtn) landingClockOutBtn.disabled = !isClockedIn;

        if (clockInButton) clockInButton.disabled = isClockedIn;
        if (clockOutButton) clockOutButton.disabled = !isClockedIn;
        if (attendanceStatus) attendanceStatus.textContent = isClockedIn ? "Clocked in" : "Not clocked in";

        const response = await apiRequest("/attendance");
        const records = normalizeListResponse(response, ["records", "attendance", "items", "data"]);

        const latestRecord = records[0];
        if (latestRecord) {
            if (clockInTimeEl) clockInTimeEl.textContent = latestRecord.clock_in ? formatTime(latestRecord.clock_in) : "--:--";
            if (clockOutTimeEl) clockOutTimeEl.textContent = latestRecord.clock_out ? formatTime(latestRecord.clock_out) : "--:--";
            if (workTimeNoteEl) workTimeNoteEl.textContent = `${latestRecord.total_work_minutes || 0} minutes worked today`;

            if (isClockedIn && latestRecord.clock_in) {
                updateShiftDurationCounter(latestRecord.clock_in);
            } else {
                updateShiftDurationCounter(null);
            }
        } else {
            if (clockInTimeEl) clockInTimeEl.textContent = "--:--";
            if (clockOutTimeEl) clockOutTimeEl.textContent = "--:--";
            if (workTimeNoteEl) workTimeNoteEl.textContent = "0 minutes worked";
            updateShiftDurationCounter(null);
        }

        if (landingTableBody) {
            if (!records.length) {
                landingTableBody.innerHTML = `
                    <tr>
                        <td colspan="5" style="text-align: center; color: var(--muted); padding: 20px;">
                            No attendance records found for today.
                        </td>
                    </tr>
                `;
            } else {
                landingTableBody.innerHTML = records.slice(0, 5).map(record => `
                    <tr>
                        <td>${escapeHtml(formatDate(record.attendance_date))}</td>
                        <td><strong>${escapeHtml(formatTime(record.clock_in))}</strong></td>
                        <td>${record.clock_out ? formatTime(record.clock_out) : '<span style="color: var(--brand); font-weight: 700;">Active Shift...</span>'}</td>
                        <td>${Number(record.total_work_minutes || 0)} mins</td>
                        <td>${createStatusBadge(record.status || "present")}</td>
                    </tr>
                `).join("");
            }
        }

    } catch (err) {
        console.warn("Failed to load landing attendance workstation", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const landingClockInBtn = document.getElementById("landingClockInBtn");
    const landingClockOutBtn = document.getElementById("landingClockOutBtn");

    if (landingClockInBtn) {
        landingClockInBtn.addEventListener("click", async () => {
            landingClockInBtn.disabled = true;
            try {
                await apiRequest("/attendance/clock-in", { method: "POST", body: {} });
                showNotification("Clocked in successfully!", "success");
                await loadLandingAttendanceWorkstation();
                await loadDashboard();
            } catch (err) {
                landingClockInBtn.disabled = false;
                showNotification(err.message, "error");
            }
        });
    }

    if (landingClockOutBtn) {
        landingClockOutBtn.addEventListener("click", async () => {
            landingClockOutBtn.disabled = true;
            try {
                await apiRequest("/attendance/clock-out", { method: "PATCH", body: {} });
                showNotification("Clocked out successfully!", "success");
                await loadLandingAttendanceWorkstation();
                await loadDashboard();
            } catch (err) {
                landingClockOutBtn.disabled = false;
                showNotification(err.message, "error");
            }
        });
    }
});


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
            title: onboardingTaskTitle.value.trim(),
            description:
                onboardingTaskDescription.value.trim() || null,
            due_date:
                onboardingTaskDueDate.value || null
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

    // Sub-tabs switcher (scoped to current section)
    document.querySelectorAll(".sub-tab").forEach(tab => {
        tab.addEventListener("click", () => {
            const section = tab.closest(".content-section") || document;
            section.querySelectorAll(".sub-tab").forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
            const targetId = tab.dataset.tab;
            section.querySelectorAll(".sub-tab-content").forEach(c => c.classList.add("hidden"));
            document.getElementById(targetId)?.classList.remove("hidden");
        });
    });

    // Star rating picker for Performance Form
    const starPicker = document.getElementById("starRatingPicker");
    if (starPicker) {
        starPicker.querySelectorAll("span").forEach(star => {
            star.addEventListener("click", () => {
                const rating = parseInt(star.dataset.star);
                document.getElementById("reviewRatingInput").value = rating;
                starPicker.querySelectorAll("span").forEach(s => {
                    const sVal = parseInt(s.dataset.star);
                    s.classList.toggle("active", sVal <= rating);
                });
            });
        });
    }

    // Add Employee Modal handlers
    const openModalBtn = document.getElementById("openAddEmployeeBtn");
    const closeModalBtn = document.getElementById("closeAddEmployeeBtn");
    const cancelModalBtn = document.getElementById("cancelAddEmployeeBtn");
    const addEmpModal = document.getElementById("addEmployeeModal");

    if (openModalBtn && addEmpModal) {
        openModalBtn.addEventListener("click", () => addEmpModal.classList.remove("hidden"));
    }
    [closeModalBtn, cancelModalBtn].forEach(btn => {
        if (btn && addEmpModal) {
            btn.addEventListener("click", () => addEmpModal.classList.add("hidden"));
        }
    });

    // Add Employee Form submit
    const addEmpForm = document.getElementById("addEmployeeForm");
    if (addEmpForm) {
        addEmpForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            try {
                const full_name = document.getElementById("newEmpName").value.trim();
                const email = document.getElementById("newEmpEmail").value.trim();
                const password = document.getElementById("newEmpPassword").value;
                const job_title = document.getElementById("newEmpTitle").value.trim();
                const department = document.getElementById("newEmpDept").value;
                const phone = document.getElementById("newEmpPhone").value.trim();
                const leave_balance = parseInt(document.getElementById("newEmpLeave").value);

                await apiRequest("/employees", {
                    method: "POST",
                    body: { full_name, email, password, job_title, department, phone, leave_balance }
                });

                addEmpForm.reset();
                if (addEmpModal) addEmpModal.classList.add("hidden");
                showNotification("Employee profile created successfully!", "success");
                await loadEmployees();
            } catch (err) {
                showNotification(err.message, "error");
            }
        });
    }

    // Search and Dept Filter input listeners for Staff Directory
    document.getElementById("employeeSearchInput")?.addEventListener("input", () => loadEmployees());
    document.getElementById("employeeDeptFilter")?.addEventListener("change", () => loadEmployees());

    // Performance Form submit
    const perfForm = document.getElementById("performanceForm");
    if (perfForm) {
        perfForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            try {
                const employee_id = parseInt(document.getElementById("reviewEmployeeSelect").value);
                const review_cycle = document.getElementById("reviewCycle").value.trim();
                const rating = parseInt(document.getElementById("reviewRatingInput").value);
                const strengths = document.getElementById("reviewStrengths").value.trim();
                const growth_areas = document.getElementById("reviewGrowth").value.trim();

                await apiRequest("/reviews/performance", {
                    method: "POST",
                    body: { employee_id, review_cycle, rating, strengths, growth_areas, status: "completed" }
                });

                perfForm.reset();
                showNotification("Performance review submitted!", "success");
                await loadReviews();
            } catch (err) {
                showNotification(err.message, "error");
            }
        });
    }

    // Kudos Form submit
    const kudosForm = document.getElementById("kudosForm");
    if (kudosForm) {
        kudosForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            try {
                const receiver_name = document.getElementById("kudosReceiver").value.trim();
                const category = document.getElementById("kudosCategory").value;
                const message = document.getElementById("kudosMessage").value.trim();

                await apiRequest("/reviews/kudos", {
                    method: "POST",
                    body: { receiver_name, category, message }
                });

                kudosForm.reset();
                showNotification("Peer shoutout posted!", "success");
                await loadKudos();
            } catch (err) {
                showNotification(err.message, "error");
            }
        });
    }

        // Export CSV button listeners
    document.getElementById("exportAttendanceBtn")?.addEventListener("click", () => {
        window.open(`${API_BASE_URL}/analytics/export/attendance`, "_blank");
    });
    document.getElementById("exportLeaveBtn")?.addEventListener("click", () => {
        window.open(`${API_BASE_URL}/analytics/export/leave`, "_blank");
    });
    document.getElementById("exportExpenseBtn")?.addEventListener("click", () => {
        window.open(`${API_BASE_URL}/analytics/export/expenses`, "_blank");
    });

    // Phase 2 Modal triggers
    setupModalTrigger("openAddShiftBtn", "closeAddShiftBtn", "cancelAddShiftBtn", "addShiftModal");
    setupModalTrigger("openAddAssetBtn", "closeAddAssetBtn", "cancelAddAssetBtn", "addAssetModal");
    setupModalTrigger("openAddEventBtn", "closeAddEventBtn", "cancelAddEventBtn", "addEventModal");
    setupModalTrigger("openAddTrainingBtn", "closeAddTrainingBtn", "cancelAddTrainingBtn", "addTrainingModal");

    // Add Shift Form submit
    document.getElementById("addShiftForm")?.addEventListener("submit", async (e) => {
        e.preventDefault();
        try {
            const admin_id = parseInt(document.getElementById("shiftEmployeeSelect").value);
            const shift_name = document.getElementById("shiftName").value.trim();
            const start_time = document.getElementById("shiftStartTime").value.trim();
            const end_time = document.getElementById("shiftEndTime").value.trim();
            const work_days = document.getElementById("shiftDays").value.trim();
            const location = document.getElementById("shiftLocation").value;

            await apiRequest("/shifts", {
                method: "POST",
                body: { admin_id, shift_name, shift_type: "Morning", start_time, end_time, work_days, location }
            });

            document.getElementById("addShiftForm").reset();
            document.getElementById("addShiftModal")?.classList.add("hidden");
            showNotification("Work shift schedule assigned!", "success");
            await loadShifts();
        } catch (err) {
            showNotification(err.message, "error");
        }
    });

    // Add Asset Form submit
    document.getElementById("addAssetForm")?.addEventListener("submit", async (e) => {
        e.preventDefault();
        try {
            const asset_tag = document.getElementById("assetTag").value.trim();
            const asset_name = document.getElementById("assetName").value.trim();
            const category = document.getElementById("assetCategory").value;
            const serial_number = document.getElementById("assetSerial").value.trim() || null;
            const empVal = document.getElementById("assetEmployeeSelect").value;
            const admin_id = empVal ? parseInt(empVal) : null;
            const status = admin_id ? "assigned" : "available";

            await apiRequest("/assets", {
                method: "POST",
                body: { asset_tag, asset_name, category, serial_number, admin_id, status }
            });

            document.getElementById("addAssetForm").reset();
            document.getElementById("addAssetModal")?.classList.add("hidden");
            showNotification("IT asset registered successfully!", "success");
            await loadAssets();
        } catch (err) {
            showNotification(err.message, "error");
        }
    });

    // Filter listeners for IT Assets
    document.getElementById("assetCategoryFilter")?.addEventListener("change", () => loadAssets());
    document.getElementById("assetStatusFilter")?.addEventListener("change", () => loadAssets());

    // Add Event Form submit
    document.getElementById("addEventForm")?.addEventListener("submit", async (e) => {
        e.preventDefault();
        try {
            const title = document.getElementById("eventTitle").value.trim();
            const event_type = document.getElementById("eventType").value;
            const event_date = document.getElementById("eventDate").value;
            const location = document.getElementById("eventLocation").value.trim();
            const description = document.getElementById("eventDescription").value.trim();

            await apiRequest("/calendar/events", {
                method: "POST",
                body: { title, event_type, event_date, location, description: description || null }
            });

            document.getElementById("addEventForm").reset();
            document.getElementById("addEventModal")?.classList.add("hidden");
            showNotification("Company event added!", "success");
            await loadCalendar();
        } catch (err) {
            showNotification(err.message, "error");
        }
    });

    // Add Training Form submit
    document.getElementById("addTrainingForm")?.addEventListener("submit", async (e) => {
        e.preventDefault();
        try {
            const admin_id = parseInt(document.getElementById("trainingEmployeeSelect").value);
            const title = document.getElementById("trainingTitle").value.trim();
            const category = document.getElementById("trainingCategory").value;
            const duration_hours = parseInt(document.getElementById("trainingHours").value);
            const description = document.getElementById("trainingDescription").value.trim();

            await apiRequest("/trainings", {
                method: "POST",
                body: { admin_id, title, category, duration_hours, description: description || null }
            });

            document.getElementById("addTrainingForm").reset();
            document.getElementById("addTrainingModal")?.classList.add("hidden");
            showNotification("Training course assigned!", "success");
            await loadTrainings();
        } catch (err) {
            showNotification(err.message, "error");
        }
    });

    // Phase 3 Modal triggers
    setupModalTrigger("openGeneratePayslipBtn", "closeGeneratePayslipBtn", "cancelGeneratePayslipBtn", "generatePayslipModal");
    setupModalTrigger("openAddJobBtn", "closeAddJobBtn", "cancelAddJobBtn", "addJobModal");
    setupModalTrigger("openAddCandidateBtn", "closeAddCandidateBtn", "cancelAddCandidateBtn", "addCandidateModal");
    setupModalTrigger("openAddSurveyBtn", "closeAddSurveyBtn", "cancelAddSurveyBtn", "addSurveyModal");
    setupModalTrigger("openAddIdeaBtn", "closeAddIdeaBtn", "cancelAddIdeaBtn", "addIdeaModal");

    // Close Payslip Invoice Modal listener
    document.getElementById("closePayslipInvoiceBtn")?.addEventListener("click", () => {
        document.getElementById("payslipInvoiceModal")?.classList.add("hidden");
    });

    // Generate Payslip Form submit
    document.getElementById("generatePayslipForm")?.addEventListener("submit", async (e) => {
        e.preventDefault();
        try {
            const admin_id = parseInt(document.getElementById("payslipEmployeeSelect").value);
            const month = document.getElementById("payslipMonthSelect").value;
            const year = parseInt(document.getElementById("payslipYearInput").value);
            const basic_salary = parseFloat(document.getElementById("payslipBasicSalary").value);
            const allowances = parseFloat(document.getElementById("payslipAllowances").value || "0");
            const bonus = parseFloat(document.getElementById("payslipBonus").value || "0");
            const tax_deduction = parseFloat(document.getElementById("payslipTax").value || "0");
            const insurance_deduction = parseFloat(document.getElementById("payslipInsurance").value || "0");
            const provident_fund_deduction = parseFloat(document.getElementById("payslipProvidentFund").value || "0");
            const payment_method = document.getElementById("payslipPaymentMethod").value;
            const payment_status = document.getElementById("payslipPaymentStatus").value;
            const notes = document.getElementById("payslipNotes").value.trim() || null;

            await apiRequest("/payslips", {
                method: "POST",
                body: {
                    admin_id,
                    month,
                    year,
                    basic_salary,
                    allowances,
                    bonus,
                    tax_deduction,
                    insurance_deduction,
                    provident_fund_deduction,
                    payment_method,
                    payment_status,
                    notes
                }
            });

            document.getElementById("generatePayslipForm").reset();
            document.getElementById("generatePayslipModal")?.classList.add("hidden");
            showNotification("Employee payslip issued successfully!", "success");
            await loadPayslips();
        } catch (err) {
            showNotification(err.message, "error");
        }
    });

    // Payslip Filter listeners
    document.getElementById("payslipMonthFilter")?.addEventListener("change", () => loadPayslips());
    document.getElementById("payslipStatusFilter")?.addEventListener("change", () => loadPayslips());
    document.getElementById("payslipEmployeeFilter")?.addEventListener("change", () => loadPayslips());

    // Add Job Form submit
    document.getElementById("addJobForm")?.addEventListener("submit", async (e) => {
        e.preventDefault();
        try {
            const title = document.getElementById("jobTitle").value.trim();
            const department = document.getElementById("jobDepartment").value;
            const job_type = document.getElementById("jobType").value;
            const experience_level = document.getElementById("jobExpLevel").value;
            const salary_range = document.getElementById("jobSalary").value.trim();
            const location = document.getElementById("jobLocation").value.trim();
            const description = document.getElementById("jobDescription").value.trim();
            const requirements = document.getElementById("jobRequirements").value.trim() || null;

            await apiRequest("/recruitment/jobs", {
                method: "POST",
                body: { title, department, job_type, experience_level, salary_range, location, status: "active", description, requirements }
            });

            document.getElementById("addJobForm").reset();
            document.getElementById("addJobModal")?.classList.add("hidden");
            showNotification("Job requisition published!", "success");
            await loadJobs();
            await populateRecruitmentJobDropdown();
        } catch (err) {
            showNotification(err.message, "error");
        }
    });

    // Add Candidate Form submit
    document.getElementById("addCandidateForm")?.addEventListener("submit", async (e) => {
        e.preventDefault();
        try {
            const job_id = parseInt(document.getElementById("candidateJobSelect").value);
            const full_name = document.getElementById("candidateName").value.trim();
            const email = document.getElementById("candidateEmail").value.trim();
            const phone = document.getElementById("candidatePhone").value.trim() || null;
            const stage = document.getElementById("candidateStage").value;
            const rating = parseInt(document.getElementById("candidateRating").value);
            const resume_link = document.getElementById("candidateResume").value.trim() || null;
            const notes = document.getElementById("candidateNotes").value.trim() || null;

            await apiRequest("/recruitment/candidates", {
                method: "POST",
                body: { job_id, full_name, email, phone, stage, rating, resume_link, notes }
            });

            document.getElementById("addCandidateForm").reset();
            document.getElementById("addCandidateModal")?.classList.add("hidden");
            showNotification("Candidate application registered!", "success");
            await loadCandidates();
            await loadJobs();
        } catch (err) {
            showNotification(err.message, "error");
        }
    });

    // Candidate Stage Filter listener
    document.getElementById("candidateStageFilter")?.addEventListener("change", () => loadCandidates());

    // Chat Composer Form submit
    document.getElementById("chatComposerForm")?.addEventListener("submit", async (e) => {
        e.preventDefault();
        const input = document.getElementById("chatInput");
        if (!input) return;
        const msg = input.value.trim();
        if (!msg) return;

        try {
            input.value = "";
            await apiRequest("/chat/messages", {
                method: "POST",
                body: { channel: activeChatChannel, message: msg, message_type: "channel" }
            });
            await loadChatMessages();
        } catch (err) {
            showNotification(err.message, "error");
        }
    });

    // Add Pulse Survey Form submit
    document.getElementById("addSurveyForm")?.addEventListener("submit", async (e) => {
        e.preventDefault();
        try {
            const title = document.getElementById("surveyTitle").value.trim();
            const category = document.getElementById("surveyCategory").value;
            const question = document.getElementById("surveyQuestion").value.trim();
            const optionsStr = document.getElementById("surveyOptionsInput").value.trim();
            const options = optionsStr.split(",").map(o => o.trim()).filter(o => o.length > 0);

            if (options.length < 2) {
                showNotification("Please provide at least 2 comma-separated options.", "error");
                return;
            }

            await apiRequest("/surveys", {
                method: "POST",
                body: { title, category, question, options }
            });

            document.getElementById("addSurveyForm").reset();
            document.getElementById("addSurveyModal")?.classList.add("hidden");
            showNotification("Company pulse poll launched!", "success");
            await loadSurveys();
        } catch (err) {
            showNotification(err.message, "error");
        }
    });

    // Add Innovation Idea Form submit
    document.getElementById("addIdeaForm")?.addEventListener("submit", async (e) => {
        e.preventDefault();
        try {
            const title = document.getElementById("ideaTitle").value.trim();
            const category = document.getElementById("ideaCategory").value;
            const description = document.getElementById("ideaDescription").value.trim();

            await apiRequest("/surveys/ideas", {
                method: "POST",
                body: { title, category, description }
            });

            document.getElementById("addIdeaForm").reset();
            document.getElementById("addIdeaModal")?.classList.add("hidden");
            showNotification("Innovation idea submitted to team board!", "success");
            await loadIdeas();
        } catch (err) {
            showNotification(err.message, "error");
        }
    });

    // Notification bell handlers
    const notifBtn = document.getElementById("notifBellBtn");
    const notifDropdown = document.getElementById("notifDropdown");
    const clearNotifBtn = document.getElementById("clearNotifBtn");

    if (notifBtn && notifDropdown) {
        notifBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            notifDropdown.classList.toggle("hidden");
        });

        document.addEventListener("click", () => {
            notifDropdown.classList.add("hidden");
        });
    }

    if (clearNotifBtn) {
        clearNotifBtn.addEventListener("click", () => {
            const list = document.getElementById("notifList");
            const badge = document.getElementById("notifBadge");
            if (list) list.innerHTML = `<div class="notif-item"><p class="muted">No unread notifications.</p></div>`;
            if (badge) badge.style.display = "none";
        });
    }

    // Employee Detail modal close handlers
    const closeEmpDetailBtn = document.getElementById("closeEmpDetailBtn");
    const closeEmpDetailBtn2 = document.getElementById("closeEmpDetailBtn2");
    const empDetailModal = document.getElementById("employeeDetailModal");
    [closeEmpDetailBtn, closeEmpDetailBtn2].forEach(btn => {
        if (btn && empDetailModal) btn.addEventListener("click", () => empDetailModal.classList.add("hidden"));
    });

    // Command Palette Open & Close Handlers
    const cmdBtn = document.getElementById("cmdPaletteBtn");
    const cmdModal = document.getElementById("cmdPaletteModal");
    const closeCmdBtn = document.getElementById("closeCmdPaletteBtn");
    const cmdSearch = document.getElementById("cmdSearchInput");

    if (cmdBtn && cmdModal) {
        cmdBtn.addEventListener("click", () => {
            cmdModal.classList.remove("hidden");
            if (cmdSearch) {
                cmdSearch.value = "";
                cmdSearch.focus();
            }
        });
    }
    if (closeCmdBtn && cmdModal) {
        closeCmdBtn.addEventListener("click", () => cmdModal.classList.add("hidden"));
    }

    // Ctrl+K or Cmd+K Global Shortcut Listener
    document.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
            e.preventDefault();
            if (cmdModal) {
                cmdModal.classList.toggle("hidden");
                if (!cmdModal.classList.contains("hidden") && cmdSearch) {
                    cmdSearch.value = "";
                    cmdSearch.focus();
                }
            }
        }
    });

    // Filter Command Items in Palette
    if (cmdSearch) {
        cmdSearch.addEventListener("input", () => {
            const query = cmdSearch.value.toLowerCase().trim();
            document.querySelectorAll(".cmd-item").forEach(item => {
                const text = item.textContent.toLowerCase();
                item.style.display = text.includes(query) ? "flex" : "none";
            });
        });
    }

    // Sign Out / Logout Listener
    const logoutBtn = document.getElementById("logoutButton");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            clearAuthentication();
            showLoginPage();
            showNotification("Signed out successfully.", "info");
        });
    }
});

/* Global Logout / Go To Login Page Helper */
window.logout = function() {
    clearAuthentication();
    showLoginPage();
};

window.goToLogin = function() {
    clearAuthentication();
    showLoginPage();
};


/* One-Click Demo Sign In Handler */
async function demoLogin(email, password) {
    const emailField = document.getElementById("email");
    const passField = document.getElementById("password");
    if (emailField && passField) {
        emailField.value = email;
        passField.value = password;
        const form = document.getElementById("loginForm");
        if (form) {
            form.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
        }
    }
}

/* Command Palette Executive Command Runner */
function execCmd(sectionId) {
    const cmdModal = document.getElementById("cmdPaletteModal");
    if (cmdModal) cmdModal.classList.add("hidden");
    showSection(sectionId);
}


function setupModalTrigger(openId, closeId, cancelId, modalId) {
    const openBtn = document.getElementById(openId);
    const closeBtn = document.getElementById(closeId);
    const cancelBtn = document.getElementById(cancelId);
    const modal = document.getElementById(modalId);

    if (openBtn && modal) openBtn.addEventListener("click", () => modal.classList.remove("hidden"));
    [closeBtn, cancelBtn].forEach(btn => {
        if (btn && modal) btn.addEventListener("click", () => modal.classList.add("hidden"));
    });
}

async function populateDropdown(elementId, allowUnassigned = false) {
    const select = document.getElementById(elementId);
    if (!select) return;
    try {
        const employees = await apiRequest("/employees");
        select.innerHTML = (allowUnassigned ? `<option value="">Unassigned (Available)</option>` : `<option value="">Select Employee...</option>`) +
            employees.map(e => `<option value="${e.id}">${escapeHtml(e.full_name)} (${escapeHtml(e.department)})</option>`).join("");
    } catch (e) {
        console.error(`Failed to populate dropdown #${elementId}`, e);
    }
}


/* =========================================================
   Work Shift Schedules Module
========================================================= */

async function loadShifts() {
    const grid = document.getElementById("shiftsGrid");
    if (!grid) return;
    grid.innerHTML = `<div class="empty-state">Loading shift schedules...</div>`;

    try {
        const shifts = await apiRequest("/shifts");
        if (!shifts || shifts.length === 0) {
            grid.innerHTML = `<div class="empty-state" style="grid-column: 1 / -1;">No work shifts assigned yet.</div>`;
            return;
        }

        grid.innerHTML = shifts.map(s => `
            <div class="shift-card">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <span class="shift-pill">⏰ ${escapeHtml(s.shift_type)} Shift</span>
                        <span class="badge approved" style="font-size: 11px;">${escapeHtml(s.location)}</span>
                    </div>
                    <h3 style="font-size: 16px; margin: 0 0 6px;">${escapeHtml(s.shift_name)}</h3>
                    <div class="muted" style="font-size: 13px;">📅 <strong>Days:</strong> ${escapeHtml(s.work_days)}</div>
                    <div class="muted" style="font-size: 13px; margin-top: 2px;">🕒 <strong>Hours:</strong> ${escapeHtml(s.start_time)} – ${escapeHtml(s.end_time)}</div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px; padding-top: 10px; border-top: 1px solid var(--border);">
                    <small class="muted">Employee #${s.admin_id}</small>
                    <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 12px;" onclick="deleteShiftSchedule(${s.id})">Delete</button>
                </div>
            </div>
        `).join("");
    } catch (err) {
        grid.innerHTML = `<div class="empty-state error" style="grid-column: 1 / -1;">Failed to load shifts: ${err.message}</div>`;
    }
}

async function deleteShiftSchedule(id) {
    if (!confirm("Are you sure you want to delete this shift schedule?")) return;
    try {
        await apiRequest(`/shifts/${id}`, { method: "DELETE" });
        showNotification("Shift schedule deleted.", "success");
        await loadShifts();
    } catch (err) {
        showNotification(err.message, "error");
    }
}


/* =========================================================
   IT Hardware & Asset Inventory Module
========================================================= */

async function loadAssets() {
    const body = document.getElementById("assetTableBody");
    if (!body) return;
    body.innerHTML = `<tr><td colspan="7" class="empty">Loading IT assets...</td></tr>`;

    try {
        const catVal = document.getElementById("assetCategoryFilter")?.value || "All";
        const statusVal = document.getElementById("assetStatusFilter")?.value || "All";

        let url = "/assets?";
        if (catVal !== "All") url += `category=${encodeURIComponent(catVal)}&`;
        if (statusVal !== "All") url += `status=${encodeURIComponent(statusVal)}&`;

        const assets = await apiRequest(url);
        if (!assets || assets.length === 0) {
            body.innerHTML = `<tr><td colspan="7" class="empty">No IT assets found.</td></tr>`;
            return;
        }

        body.innerHTML = assets.map(a => `
            <tr>
                <td><span class="asset-tag-badge">${escapeHtml(a.asset_tag)}</span></td>
                <td><strong>${escapeHtml(a.asset_name)}</strong></td>
                <td>${escapeHtml(a.category)}</td>
                <td class="muted">${escapeHtml(a.serial_number || 'N/A')}</td>
                <td>${a.admin_id ? `Employee #${a.admin_id}` : '<span class="muted">Unassigned</span>'}</td>
                <td><span class="badge ${a.status === 'assigned' ? 'approved' : a.status === 'available' ? 'pending' : 'rejected'}">${a.status.toUpperCase()}</span></td>
                <td><button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="deleteITAsset(${a.id})">Delete</button></td>
            </tr>
        `).join("");
    } catch (err) {
        body.innerHTML = `<tr><td colspan="7" class="empty error">Failed to load IT assets: ${err.message}</td></tr>`;
    }
}

async function deleteITAsset(id) {
    if (!confirm("Are you sure you want to delete this IT asset record?")) return;
    try {
        await apiRequest(`/assets/${id}`, { method: "DELETE" });
        showNotification("IT asset item deleted.", "success");
        await loadAssets();
    } catch (err) {
        showNotification(err.message, "error");
    }
}


/* =========================================================
   Team Calendar & Events Module
========================================================= */

async function loadCalendar() {
    const list = document.getElementById("eventsList");
    if (!list) return;
    list.innerHTML = `<div class="empty-state">Loading company events...</div>`;

    try {
        const events = await apiRequest("/calendar/events");
        if (!events || events.length === 0) {
            list.innerHTML = `<div class="empty-state">No upcoming company events scheduled.</div>`;
            return;
        }

        list.innerHTML = events.map(e => `
            <div class="event-card">
                <div style="display: flex; gap: 16px; align-items: center;">
                    <div class="event-date-badge">
                        ${new Date(e.event_date).toLocaleDateString("en-US", { month: "short", day: "numeric" }).toUpperCase()}
                    </div>
                    <div style="flex: 1;">
                        <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 4px;">
                            <span class="badge pending" style="font-size: 11px;">${escapeHtml(e.event_type)}</span>
                            <small class="muted">📍 ${escapeHtml(e.location)}</small>
                        </div>
                        <h3 style="margin: 0 0 4px; font-size: 16px;">${escapeHtml(e.title)}</h3>
                        ${e.description ? `<p class="muted" style="margin: 0; font-size: 13px;">${escapeHtml(e.description)}</p>` : ''}
                    </div>
                </div>
                <div style="display: flex; justify-content: flex-end; padding-top: 8px; border-top: 1px solid var(--border);">
                    <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="deleteCalendarEvent(${e.id})">Delete</button>
                </div>
            </div>
        `).join("");
    } catch (err) {
        list.innerHTML = `<div class="empty-state error">Failed to load calendar events: ${err.message}</div>`;
    }
}

async function deleteCalendarEvent(id) {
    if (!confirm("Are you sure you want to delete this event?")) return;
    try {
        await apiRequest(`/calendar/events/${id}`, { method: "DELETE" });
        showNotification("Calendar event deleted.", "success");
        await loadCalendar();
    } catch (err) {
        showNotification(err.message, "error");
    }
}


/* =========================================================
   Training Courses & Skills Module
========================================================= */

async function loadTrainings() {
    const grid = document.getElementById("trainingGrid");
    if (!grid) return;
    grid.innerHTML = `<div class="empty-state">Loading training courses...</div>`;

    try {
        const trainings = await apiRequest("/trainings");
        if (!trainings || trainings.length === 0) {
            grid.innerHTML = `<div class="empty-state" style="grid-column: 1 / -1;">No training courses assigned.</div>`;
            return;
        }

        grid.innerHTML = trainings.map(t => {
            const isDone = t.status === "completed";
            return `
                <div class="training-card">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                            <span class="doc-badge policy">${escapeHtml(t.category)}</span>
                            <span class="muted" style="font-size: 12px; font-weight: 700;">⏳ ${t.duration_hours} Hours</span>
                        </div>
                        <h3 style="font-size: 16px; margin: 0 0 6px;">${escapeHtml(t.title)}</h3>
                        ${t.description ? `<p class="muted" style="font-size: 13px; margin: 0 0 10px;">${escapeHtml(t.description)}</p>` : ''}
                        <div class="progress-track">
                            <div class="progress-fill" style="width: ${isDone ? 100 : 35}%;"></div>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; padding-top: 10px; border-top: 1px solid var(--border);">
                        <span class="badge ${isDone ? 'approved' : 'pending'}">${isDone ? '✓ Completed' : 'In Progress'}</span>
                        <div>
                            ${!isDone ? `<button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;" onclick="completeTrainingCourse(${t.id})">Mark Complete</button>` : ''}
                            <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 12px;" onclick="deleteTrainingCourse(${t.id})">Remove</button>
                        </div>
                    </div>
                </div>
            `;
        }).join("");
    } catch (err) {
        grid.innerHTML = `<div class="empty-state error" style="grid-column: 1 / -1;">Failed to load trainings: ${err.message}</div>`;
    }
}

async function completeTrainingCourse(id) {
    try {
        await apiRequest(`/trainings/${id}/status`, {
            method: "PATCH",
            body: { status: "completed" }
        });
        showNotification("Training course completed!", "success");
        await loadTrainings();
    } catch (err) {
        showNotification(err.message, "error");
    }
}

async function deleteTrainingCourse(id) {
    if (!confirm("Are you sure you want to delete this training course assignment?")) return;
    try {
        await apiRequest(`/trainings/${id}`, { method: "DELETE" });
        showNotification("Training assignment removed.", "success");
        await loadTrainings();
    } catch (err) {
        showNotification(err.message, "error");
    }
}


/* =========================================================
   Staff Directory Module
========================================================= */

let currentEmployeesCache = [];

async function loadEmployees() {
    const grid = document.getElementById("employeeGrid");
    if (!grid) return;
    grid.innerHTML = `<div class="empty-state">Loading staff directory...</div>`;

    try {
        const searchVal = document.getElementById("employeeSearchInput")?.value.trim() || "";
        const deptVal = document.getElementById("employeeDeptFilter")?.value || "All";

        let url = "/employees?";
        if (searchVal) url += `search=${encodeURIComponent(searchVal)}&`;
        if (deptVal !== "All") url += `department=${encodeURIComponent(deptVal)}&`;

        const employees = await apiRequest(url);
        currentEmployeesCache = employees || [];

        if (!employees || employees.length === 0) {
            grid.innerHTML = `<div class="empty-state" style="grid-column: 1 / -1;">No employees match the specified filters.</div>`;
            return;
        }

        grid.innerHTML = employees.map(emp => {
            const initials = emp.full_name ? emp.full_name.split(" ").map(n => n[0]).join("").toUpperCase().slice(0, 2) : "EM";
            return `
                <div class="employee-card">
                    <div class="employee-header">
                        <div class="employee-avatar">${initials}</div>
                        <div>
                            <strong style="font-size: 16px; display: block;">${escapeHtml(emp.full_name)}</strong>
                            <small class="muted" style="font-weight: 600;">${escapeHtml(emp.job_title)}</small>
                        </div>
                    </div>
                    <div class="employee-details-list">
                        <div>🏢 <strong>Department:</strong> ${escapeHtml(emp.department)}</div>
                        <div>✉️ <strong>Email:</strong> ${escapeHtml(emp.email)}</div>
                        <div>📞 <strong>Phone:</strong> ${escapeHtml(emp.phone)}</div>
                        <div>🏖️ <strong>Leave Balance:</strong> ${emp.leave_balance} Days Available</div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px; padding-top: 10px; border-top: 1px solid var(--border);">
                        <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 12px;" onclick="viewEmployeeDetail(${emp.id})">🔍 Inspect Profile</button>
                        <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 12px;" onclick="deleteEmployeeProfile(${emp.id})">Remove</button>
                    </div>
                </div>
            `;
        }).join("");
    } catch (error) {
        grid.innerHTML = `<div class="empty-state error" style="grid-column: 1 / -1;">Failed to load staff directory: ${error.message}</div>`;
    }
}

function viewEmployeeDetail(empId) {
    const emp = currentEmployeesCache.find(e => e.id === empId);
    if (!emp) return;

    const modal = document.getElementById("employeeDetailModal");
    if (!modal) return;

    const initials = emp.full_name ? emp.full_name.split(" ").map(n => n[0]).join("").toUpperCase().slice(0, 2) : "EM";
    document.getElementById("empDetailAvatar").textContent = initials;
    document.getElementById("empDetailName").textContent = emp.full_name;
    document.getElementById("empDetailTitle").textContent = emp.job_title || "Team Member";
    document.getElementById("empDetailEmail").textContent = emp.email;
    document.getElementById("empDetailDept").textContent = emp.department || "General";
    document.getElementById("empDetailPhone").textContent = emp.phone || "N/A";
    document.getElementById("empDetailLeave").textContent = `${emp.leave_balance} Days Available`;

    modal.classList.remove("hidden");
}

async function deleteEmployeeProfile(empId) {
    if (!confirm("Are you sure you want to remove this employee profile?")) return;
    try {
        await apiRequest(`/employees/${empId}`, { method: "DELETE" });
        showNotification("Employee profile removed.", "success");
        await loadEmployees();
    } catch (err) {
        showNotification(err.message, "error");
    }
}


/* =========================================================
   Performance Reviews & Kudos Module
========================================================= */

async function populateReviewEmployeeDropdown() {
    const select = document.getElementById("reviewEmployeeSelect");
    if (!select) return;
    try {
        const employees = await apiRequest("/employees");
        select.innerHTML = `<option value="">Select Employee...</option>` + employees.map(e => `
            <option value="${e.id}">${escapeHtml(e.full_name)} (${escapeHtml(e.department)})</option>
        `).join("");
    } catch (e) {
        console.error("Failed to load employee list for reviews", e);
    }
}

async function loadReviews() {
    const list = document.getElementById("reviewsList");
    if (!list) return;
    list.innerHTML = `<div class="empty-state">Loading reviews...</div>`;

    try {
        const reviews = await apiRequest("/reviews/performance");
        if (!reviews || reviews.length === 0) {
            list.innerHTML = `<div class="empty-state">No performance reviews recorded yet.</div>`;
            return;
        }

        list.innerHTML = reviews.map(rev => {
            const stars = "★".repeat(rev.rating) + "☆".repeat(5 - rev.rating);
            return `
                <div class="review-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="font-size: 15px;">Cycle: ${escapeHtml(rev.review_cycle)}</strong>
                        <span style="color: #f59e0b; font-size: 18px; font-weight: bold;">${stars}</span>
                    </div>
                    <p style="margin: 4px 0 0; font-size: 13px; color: var(--ink);">
                        <strong>Strengths:</strong> ${escapeHtml(rev.strengths || "None documented")}
                    </p>
                    ${rev.growth_areas ? `<p style="margin: 4px 0 0; font-size: 13px; color: var(--muted);"><strong>Growth Areas:</strong> ${escapeHtml(rev.growth_areas)}</p>` : ''}
                    <div style="font-size: 11px; color: var(--muted); margin-top: 4px; display: flex; justify-content: space-between;">
                        <span>Review ID #${rev.id}</span>
                        <span class="badge approved">${rev.status.toUpperCase()}</span>
                    </div>
                </div>
            `;
        }).join("");
    } catch (err) {
        list.innerHTML = `<div class="empty-state error">Failed to load performance reviews: ${err.message}</div>`;
    }
}

async function loadKudos() {
    const feed = document.getElementById("kudosFeed");
    if (!feed) return;
    feed.innerHTML = `<div class="empty-state">Loading peer shoutouts...</div>`;

    try {
        const kudos = await apiRequest("/reviews/kudos");
        if (!kudos || kudos.length === 0) {
            feed.innerHTML = `<div class="empty-state">No peer shoutouts posted yet. Be the first!</div>`;
            return;
        }

        feed.innerHTML = kudos.map(k => `
            <div class="kudos-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: var(--brand); font-size: 14px;">${escapeHtml(k.sender_name)}</strong>
                        <span class="muted" style="font-size: 13px;"> recognized </span>
                        <strong style="font-size: 14px;">${escapeHtml(k.receiver_name)}</strong>
                    </div>
                    <span class="badge pending" style="font-size: 11px;">${escapeHtml(k.category)}</span>
                </div>
                <p style="margin: 6px 0 0; font-size: 13px; line-height: 1.4; color: var(--ink);">"${escapeHtml(k.message)}"</p>
            </div>
        `).join("");
    } catch (err) {
        feed.innerHTML = `<div class="empty-state error">Failed to load kudos feed: ${err.message}</div>`;
    }
}


/* =========================================================
   Document Center Module
========================================================= */

async function loadDocuments() {
    const grid = document.getElementById("documentGrid");
    if (!grid) return;
    grid.innerHTML = `<div class="empty-state">Loading company policies...</div>`;

    try {
        const docs = await apiRequest("/documents");
        if (!docs || docs.length === 0) {
            grid.innerHTML = `<div class="empty-state" style="grid-column: 1 / -1;">No company policy documents available.</div>`;
            return;
        }

        grid.innerHTML = docs.map(doc => {
            const catClass = (doc.category || "policy").toLowerCase();
            return `
                <div class="doc-card">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                            <span class="doc-badge ${catClass}">${escapeHtml(doc.category)}</span>
                            <span class="muted" style="font-size: 12px; font-weight: 700;">${escapeHtml(doc.version)}</span>
                        </div>
                        <h3 style="font-size: 16px; margin: 0 0 8px;">${escapeHtml(doc.title)}</h3>
                        <p class="muted" style="font-size: 13px; line-height: 1.5; margin: 0;">${escapeHtml(doc.summary)}</p>
                    </div>
                    <div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
                        ${doc.is_acknowledged 
                            ? `<span class="badge approved">✓ Acknowledged</span>` 
                            : `<button class="btn btn-primary" style="padding: 6px 12px; font-size: 12px;" onclick="acknowledgeDoc(${doc.id})">Mark as Read & Acknowledge</button>`
                        }
                    </div>
                </div>
            `;
        }).join("");
    } catch (err) {
        grid.innerHTML = `<div class="empty-state error" style="grid-column: 1 / -1;">Failed to load documents: ${err.message}</div>`;
    }
}

async function acknowledgeDoc(docId) {
    try {
        await apiRequest(`/documents/${docId}/acknowledge`, { method: "POST" });
        showNotification("Policy document acknowledged!", "success");
        await loadDocuments();
    } catch (err) {
        showNotification(err.message, "error");
    }
}


/* =========================================================
   Analytics & Reports Module
========================================================= */

async function loadAnalytics() {
    try {
        const metrics = await apiRequest("/analytics/metrics");
        const s = metrics.summary;

        const activeStaffEl = document.getElementById("statActiveStaff");
        if (activeStaffEl) activeStaffEl.textContent = s.active_staff || 0;
        
        const clockedInEl = document.getElementById("statClockedIn");
        if (clockedInEl) clockedInEl.textContent = s.clocked_in_now || 0;
        
        const taskRateEl = document.getElementById("statTaskRate");
        if (taskRateEl) taskRateEl.textContent = `${s.task_completion_rate || 0}%`;
        
        const avgRatingEl = document.getElementById("statAvgRating");
        if (avgRatingEl) avgRatingEl.textContent = `${s.average_performance_rating || 5.0} / 5.0`;

        // Render Expense Categories Chart
        const expenseChart = document.getElementById("chartExpenseCategories");
        if (expenseChart && metrics.expense_breakdown) {
            const maxVal = Math.max(...metrics.expense_breakdown.map(b => b.total), 1);
            expenseChart.innerHTML = metrics.expense_breakdown.map(b => {
                const pct = Math.min(100, Math.round((b.total / maxVal) * 100));
                return `
                    <div class="bar-item">
                        <div class="bar-label-row">
                            <span>${escapeHtml(b.category)}</span>
                            <strong>$${b.total.toLocaleString()}</strong>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: ${pct}%;"></div>
                        </div>
                    </div>
                `;
            }).join("");
        }

        // Render Department Headcount Chart
        const deptChart = document.getElementById("chartDepartments");
        if (deptChart && metrics.department_breakdown) {
            const maxVal = Math.max(...metrics.department_breakdown.map(b => b.count), 1);
            deptChart.innerHTML = metrics.department_breakdown.map(b => {
                const pct = Math.min(100, Math.round((b.count / maxVal) * 100));
                return `
                    <div class="bar-item">
                        <div class="bar-label-row">
                            <span>${escapeHtml(b.department)}</span>
                            <strong>${b.count} Members</strong>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: ${pct}%; background: linear-gradient(90deg, #10b981, #3b82f6);"></div>
                        </div>
                    </div>
                `;
            }).join("");
        }
    } catch (err) {
        showNotification(`Failed to load analytics metrics: ${err.message}`, "error");
    }
}


/* =========================================================
   Module 18: Salary, Compensation & Payslips
========================================================= */

let currentPayslipsCache = [];

async function loadPayslips() {
    const tbody = document.getElementById("payslipsTableBody");
    if (!tbody) return;
    tbody.innerHTML = `<tr><td colspan="9" class="empty">Loading compensation records...</td></tr>`;

    try {
        const monthVal = document.getElementById("payslipMonthFilter")?.value || "All";
        const statusVal = document.getElementById("payslipStatusFilter")?.value || "All";
        const empVal = document.getElementById("payslipEmployeeFilter")?.value || "";

        let url = "/payslips?";
        if (monthVal !== "All") url += `month=${encodeURIComponent(monthVal)}&`;
        if (statusVal !== "All") url += `status=${encodeURIComponent(statusVal)}&`;
        if (empVal) url += `admin_id=${encodeURIComponent(empVal)}&`;

        const list = await apiRequest(url);
        currentPayslipsCache = list || [];

        if (!list || list.length === 0) {
            tbody.innerHTML = `<tr><td colspan="9" class="empty">No payslips found for selected filters.</td></tr>`;
            return;
        }

        tbody.innerHTML = list.map(p => {
            const isPaid = p.payment_status === "paid";
            const gross = (p.basic_salary || 0) + (p.allowances || 0) + (p.bonus || 0);
            const totalDeductions = (p.tax_deduction || 0) + (p.insurance_deduction || 0) + (p.provident_fund_deduction || 0);
            return `
                <tr>
                    <td><strong>${escapeHtml(p.employee_name || 'Staff Member')}</strong></td>
                    <td><span class="badge" style="font-size: 11px;">${escapeHtml(p.employee_department || 'General')}</span></td>
                    <td>${escapeHtml(p.month)} ${p.year}</td>
                    <td>$${(p.basic_salary || 0).toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                    <td class="muted">+$${((p.bonus || 0) + (p.allowances || 0)).toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                    <td style="color: var(--danger-color);">-$${totalDeductions.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                    <td><span class="net-pay-pill">$${(p.net_salary || 0).toLocaleString(undefined, {minimumFractionDigits: 2})}</span></td>
                    <td><span class="badge ${isPaid ? 'approved' : 'pending'}">${p.payment_status.toUpperCase()}</span></td>
                    <td>
                        <div style="display: flex; gap: 6px; align-items: center;">
                            <button class="btn btn-primary" style="padding: 2px 8px; font-size: 11px;" onclick="viewPayslipInvoice(${p.id})">📄 View Invoice</button>
                            <button class="btn btn-secondary" style="padding: 2px 6px; font-size: 11px;" onclick="togglePayslipStatus(${p.id}, '${p.payment_status}')">${isPaid ? 'Mark Pending' : 'Mark Paid'}</button>
                            <button class="btn btn-secondary" style="padding: 2px 6px; font-size: 11px;" onclick="deletePayslip(${p.id})">✕</button>
                        </div>
                    </td>
                </tr>
            `;
        }).join("");
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="9" class="empty error">Failed to load payslips: ${err.message}</td></tr>`;
    }
}

async function viewPayslipInvoice(id) {
    const payslip = currentPayslipsCache.find(p => p.id === id);
    if (!payslip) return;

    const modal = document.getElementById("payslipInvoiceModal");
    if (!modal) return;

    const payPeriodEl = document.getElementById("invoicePayPeriod");
    if (payPeriodEl) payPeriodEl.textContent = `${payslip.month} ${payslip.year}`;

    const refEl = document.getElementById("invoiceReferenceNo");
    if (refEl) refEl.textContent = `REF: EMS-PAY-${payslip.year}-${String(payslip.id).padStart(4, "0")}`;

    const empNameEl = document.getElementById("invoiceEmpName");
    if (empNameEl) empNameEl.textContent = payslip.employee_name || "Employee";

    const empTitleEl = document.getElementById("invoiceEmpTitle");
    if (empTitleEl) empTitleEl.textContent = payslip.employee_job_title || "Team Member";

    const empDeptEl = document.getElementById("invoiceEmpDept");
    if (empDeptEl) empDeptEl.textContent = payslip.employee_department || "General";

    const payDateEl = document.getElementById("invoicePayDate");
    if (payDateEl) payDateEl.textContent = payslip.payment_date ? formatDate(payslip.payment_date) : "Pending Disbursal";

    const payMethodEl = document.getElementById("invoicePayMethod");
    if (payMethodEl) payMethodEl.textContent = payslip.payment_method || "Direct Bank Deposit";
    
    const statusBadge = document.getElementById("invoicePayStatus");
    if (statusBadge) {
        statusBadge.textContent = payslip.payment_status.toUpperCase();
        statusBadge.className = `badge ${payslip.payment_status === 'paid' ? 'approved' : 'pending'}`;
    }

    const basic = payslip.basic_salary || 0;
    const allowances = payslip.allowances || 0;
    const bonus = payslip.bonus || 0;
    const gross = basic + allowances + bonus;

    const tax = payslip.tax_deduction || 0;
    const ins = payslip.insurance_deduction || 0;
    const prov = payslip.provident_fund_deduction || 0;
    const totalDeductions = tax + ins + prov;

    const basicEl = document.getElementById("invoiceBasicSalary");
    if (basicEl) basicEl.textContent = `$${basic.toLocaleString(undefined, {minimumFractionDigits: 2})}`;

    const allowEl = document.getElementById("invoiceAllowances");
    if (allowEl) allowEl.textContent = `$${allowances.toLocaleString(undefined, {minimumFractionDigits: 2})}`;

    const bonusEl = document.getElementById("invoiceBonus");
    if (bonusEl) bonusEl.textContent = `$${bonus.toLocaleString(undefined, {minimumFractionDigits: 2})}`;

    const grossEl = document.getElementById("invoiceGrossSalary");
    if (grossEl) grossEl.textContent = `$${gross.toLocaleString(undefined, {minimumFractionDigits: 2})}`;

    const taxEl = document.getElementById("invoiceTax");
    if (taxEl) taxEl.textContent = `$${tax.toLocaleString(undefined, {minimumFractionDigits: 2})}`;

    const insEl = document.getElementById("invoiceInsurance");
    if (insEl) insEl.textContent = `$${ins.toLocaleString(undefined, {minimumFractionDigits: 2})}`;

    const provEl = document.getElementById("invoiceProvident");
    if (provEl) provEl.textContent = `$${prov.toLocaleString(undefined, {minimumFractionDigits: 2})}`;

    const totalDedEl = document.getElementById("invoiceTotalDeductions");
    if (totalDedEl) totalDedEl.textContent = `$${totalDeductions.toLocaleString(undefined, {minimumFractionDigits: 2})}`;

    const netEl = document.getElementById("invoiceNetSalary");
    if (netEl) netEl.textContent = `$${(payslip.net_salary || 0).toLocaleString(undefined, {minimumFractionDigits: 2})}`;

    modal.classList.remove("hidden");
}

async function togglePayslipStatus(id, currentStatus) {
    const newStatus = currentStatus === "paid" ? "pending" : "paid";
    try {
        await apiRequest(`/payslips/${id}/status`, {
            method: "PATCH",
            body: { payment_status: newStatus }
        });
        showNotification(`Payslip marked as ${newStatus}.`, "success");
        await loadPayslips();
    } catch (err) {
        showNotification(err.message, "error");
    }
}

async function deletePayslip(id) {
    if (!confirm("Are you sure you want to delete this payslip record?")) return;
    try {
        await apiRequest(`/payslips/${id}`, { method: "DELETE" });
        showNotification("Payslip deleted.", "success");
        await loadPayslips();
    } catch (err) {
        showNotification(err.message, "error");
    }
}


/* =========================================================
   Module 19: Recruitment & ATS Pipeline
========================================================= */

let currentJobsCache = [];
let currentCandidatesCache = [];

async function populateRecruitmentJobDropdown() {
    const select = document.getElementById("candidateJobSelect");
    if (!select) return;
    try {
        const jobs = await apiRequest("/recruitment/jobs");
        currentJobsCache = jobs || [];
        select.innerHTML = `<option value="">Select Job Opening...</option>` +
            jobs.map(j => `<option value="${j.id}">${escapeHtml(j.title)} (${escapeHtml(j.department)})</option>`).join("");
    } catch (e) {
        console.error("Failed to populate job dropdown", e);
    }
}

async function loadRecruitment() {
    await loadJobs();
    await loadCandidates();
}

async function loadJobs() {
    const grid = document.getElementById("jobsGrid");
    if (!grid) return;
    grid.innerHTML = `<div class="empty-state">Loading job openings...</div>`;

    try {
        const jobs = await apiRequest("/recruitment/jobs");
        currentJobsCache = jobs || [];
        if (!jobs || jobs.length === 0) {
            grid.innerHTML = `<div class="empty-state" style="grid-column: 1 / -1;">No active job requisitions. Click '+ Post Job Opening' to create one.</div>`;
            return;
        }

        grid.innerHTML = jobs.map(j => `
            <div class="job-card">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <span class="doc-badge policy">${escapeHtml(j.department)}</span>
                        <span class="badge approved">${escapeHtml(j.status.toUpperCase())}</span>
                    </div>
                    <h3 style="font-size: 17px; margin: 0 0 6px;">${escapeHtml(j.title)}</h3>
                    <p class="muted" style="font-size: 13px; margin: 0 0 12px;">${escapeHtml(j.description || '')}</p>
                    <div style="display: flex; flex-direction: column; gap: 4px; font-size: 12.5px; color: var(--muted); margin-bottom: 14px;">
                        <div>💼 <strong>Type:</strong> ${escapeHtml(j.job_type)} · ${escapeHtml(j.experience_level)}</div>
                        <div>📍 <strong>Location:</strong> ${escapeHtml(j.location)}</div>
                        <div>💰 <strong>Compensation:</strong> ${escapeHtml(j.salary_range)}</div>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border); padding-top: 12px; margin-top: 12px;">
                    <span style="font-weight: 700; font-size: 13px; color: var(--primary);">👥 ${j.candidates_count || 0} Candidates</span>
                    <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 12px;" onclick="deleteJobRequisition(${j.id})">Remove</button>
                </div>
            </div>
        `).join("");
    } catch (err) {
        grid.innerHTML = `<div class="empty-state error" style="grid-column: 1 / -1;">Failed to load jobs: ${err.message}</div>`;
    }
}

async function loadCandidates() {
    const grid = document.getElementById("candidatesGrid");
    if (!grid) return;
    grid.innerHTML = `<div class="empty-state">Loading candidate applications...</div>`;

    try {
        const stageVal = document.getElementById("candidateStageFilter")?.value || "All";
        let url = "/recruitment/candidates?";
        if (stageVal !== "All") url += `stage=${encodeURIComponent(stageVal)}&`;

        const candidates = await apiRequest(url);
        currentCandidatesCache = candidates || [];

        if (!candidates || candidates.length === 0) {
            grid.innerHTML = `<div class="empty-state" style="grid-column: 1 / -1;">No candidates found matching filters.</div>`;
            return;
        }

        grid.innerHTML = candidates.map(c => {
            const stars = "★".repeat(c.rating || 4) + "☆".repeat(5 - (c.rating || 4));
            const stageClass = `stage-${c.stage || 'applied'}`;
            return `
                <div class="candidate-card">
                    <div class="candidate-header">
                        <div>
                            <strong style="font-size: 16px; display: block;">${escapeHtml(c.full_name)}</strong>
                            <small class="muted" style="font-weight: 600;">${escapeHtml(c.job_title)} · ${escapeHtml(c.job_department)}</small>
                        </div>
                        <span class="stage-badge ${stageClass}">${c.stage.toUpperCase()}</span>
                    </div>
                    <div style="font-size: 13px; display: flex; flex-direction: column; gap: 4px;">
                        <div>✉️ ${escapeHtml(c.email)}</div>
                        ${c.phone ? `<div>📞 ${escapeHtml(c.phone)}</div>` : ''}
                        ${c.resume_link ? `<div>🔗 <a href="${escapeHtml(c.resume_link)}" target="_blank" style="color: var(--primary); text-decoration: underline;">View Portfolio / Profile</a></div>` : ''}
                    </div>
                    ${c.notes ? `<div style="font-size: 12.5px; background: var(--surface-soft); padding: 8px 10px; border-radius: 8px; border: 1px solid var(--border); color: var(--ink);"><strong>Notes:</strong> ${escapeHtml(c.notes)}</div>` : ''}
                    <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 10px; border-top: 1px solid var(--border); margin-top: 6px;">
                        <span style="color: #f59e0b; font-size: 15px;">${stars}</span>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <select onchange="updateCandidateStageItem(${c.id}, this.value)" style="padding: 4px 8px; font-size: 11.5px; border-radius: 6px; border: 1px solid var(--border);">
                                <option value="applied" ${c.stage === 'applied' ? 'selected' : ''}>Applied</option>
                                <option value="screening" ${c.stage === 'screening' ? 'selected' : ''}>Screening</option>
                                <option value="interview" ${c.stage === 'interview' ? 'selected' : ''}>Interview</option>
                                <option value="offered" ${c.stage === 'offered' ? 'selected' : ''}>Offered</option>
                                <option value="hired" ${c.stage === 'hired' ? 'selected' : ''}>Hired</option>
                                <option value="rejected" ${c.stage === 'rejected' ? 'selected' : ''}>Rejected</option>
                            </select>
                            ${c.stage !== 'hired' ? `<button class="btn-hire-action" onclick="hireAndOnboardCandidateItem(${c.id}, '${escapeHtml(c.full_name)}')">🎉 Hire & Onboard</button>` : ''}
                            <button class="btn btn-secondary" style="padding: 3px 8px; font-size: 11px;" onclick="deleteCandidateItem(${c.id})">✕</button>
                        </div>
                    </div>
                </div>
            `;
        }).join("");
    } catch (err) {
        grid.innerHTML = `<div class="empty-state error" style="grid-column: 1 / -1;">Failed to load candidates: ${err.message}</div>`;
    }
}

async function updateCandidateStageItem(id, newStage) {
    try {
        await apiRequest(`/recruitment/candidates/${id}/stage`, {
            method: "PATCH",
            body: { stage: newStage }
        });
        showNotification(`Candidate stage updated to ${newStage.toUpperCase()}.`, "success");
        await loadCandidates();
        await loadJobs();
    } catch (err) {
        showNotification(err.message, "error");
    }
}

async function hireAndOnboardCandidateItem(id, name) {
    if (!confirm(`Are you ready to hire ${name} and create their employee account with onboarding tasks?`)) return;
    try {
        const res = await apiRequest(`/recruitment/candidates/${id}/convert-to-employee`, { method: "POST" });
        showNotification(res.message || "Candidate hired successfully!", "success");
        await loadCandidates();
        await loadJobs();
        await loadEmployees();
    } catch (err) {
        showNotification(err.message, "error");
    }
}

async function deleteCandidateItem(id) {
    if (!confirm("Are you sure you want to delete this candidate application?")) return;
    try {
        await apiRequest(`/recruitment/candidates/${id}`, { method: "DELETE" });
        showNotification("Candidate removed.", "success");
        await loadCandidates();
        await loadJobs();
    } catch (err) {
        showNotification(err.message, "error");
    }
}

async function deleteJobRequisition(id) {
    if (!confirm("Are you sure you want to delete this job requisition?")) return;
    try {
        await apiRequest(`/recruitment/jobs/${id}`, { method: "DELETE" });
        showNotification("Job requisition removed.", "success");
        await loadJobs();
    } catch (err) {
        showNotification(err.message, "error");
    }
}


/* =========================================================
   Module 20: Workforce Team Messenger
========================================================= */

let activeChatChannel = "general";

async function loadChatChannels() {
    const list = document.getElementById("chatChannelsList");
    if (!list) return;

    try {
        const channels = await apiRequest("/chat/channels");
        if (!channels || channels.length === 0) return;

        list.innerHTML = channels.map(ch => `
            <button class="channel-btn ${ch.name === activeChatChannel ? 'active' : ''}" onclick="switchChatChannel('${ch.name}', '${escapeHtml(ch.label)}', '${escapeHtml(ch.description)}')">
                <span>${ch.icon} ${escapeHtml(ch.name)}</span>
                <span class="badge" style="font-size: 11px;">👥 ${ch.participant_count}</span>
            </button>
        `).join("");
    } catch (e) {
        console.error("Failed to load chat channels", e);
    }
}

async function switchChatChannel(channelName, channelLabel, channelDesc) {
    activeChatChannel = channelName;
    document.querySelectorAll(".channel-btn").forEach(btn => {
        btn.classList.toggle("active", btn.textContent.includes(channelName));
    });
    const titleEl = document.getElementById("activeChannelTitle");
    const descEl = document.getElementById("activeChannelDesc");
    if (titleEl) titleEl.textContent = channelLabel || `# ${channelName}`;
    if (descEl) descEl.textContent = channelDesc || "Team space discussion";

    await loadChatMessages();
}

async function loadChatMessages() {
    const stream = document.getElementById("chatMessagesStream");
    if (!stream) return;

    try {
        const messages = await apiRequest(`/chat/messages?channel=${encodeURIComponent(activeChatChannel)}`);
        if (!messages || messages.length === 0) {
            stream.innerHTML = `<div class="empty-state">No messages in #${activeChatChannel} yet. Start the conversation!</div>`;
            return;
        }

        stream.innerHTML = messages.map(m => {
            const initials = m.sender_name ? m.sender_name.split(" ").map(n => n[0]).join("").toUpperCase().slice(0, 2) : "EM";
            const timeStr = formatDateTime(m.created_at);
            return `
                <div class="chat-msg-row">
                    <div class="chat-avatar">${initials}</div>
                    <div class="chat-content">
                        <div class="chat-meta">
                            <strong>${escapeHtml(m.sender_name)}</strong>
                            <small>${timeStr}</small>
                        </div>
                        <div class="chat-bubble">${escapeHtml(m.message)}</div>
                    </div>
                </div>
            `;
        }).join("");

        // Scroll to bottom
        stream.scrollTop = stream.scrollHeight;
    } catch (err) {
        stream.innerHTML = `<div class="empty-state error">Failed to load messages: ${err.message}</div>`;
    }
}


/* =========================================================
   Module 21: Pulse Surveys & Employee Ideas
========================================================= */

async function loadSurveysAndIdeas() {
    await loadSurveys();
    await loadIdeas();
}

async function loadSurveys() {
    const grid = document.getElementById("surveysGrid");
    if (!grid) return;
    grid.innerHTML = `<div class="empty-state">Loading pulse surveys...</div>`;

    try {
        const surveys = await apiRequest("/surveys");
        if (!surveys || surveys.length === 0) {
            grid.innerHTML = `<div class="empty-state" style="grid-column: 1 / -1;">No active pulse polls currently open.</div>`;
            return;
        }

        grid.innerHTML = surveys.map(s => {
            const total = s.total_votes || 0;
            const optionsHtml = (s.options || []).map(opt => {
                const votes = (s.vote_breakdown && s.vote_breakdown[opt]) || 0;
                const pct = total > 0 ? Math.round((votes / total) * 100) : 0;
                const isVoted = s.user_voted_option === opt;
                return `
                    <div class="poll-option-btn ${isVoted ? 'voted' : ''}" onclick="voteSurveyOption(${s.id}, '${escapeHtml(opt)}')">
                        <div class="poll-fill-bar" style="width: ${pct}%;"></div>
                        <div class="poll-content-row">
                            <span>${isVoted ? '✓ ' : ''}${escapeHtml(opt)}</span>
                            <span><strong>${pct}%</strong> (${votes} votes)</span>
                        </div>
                    </div>
                `;
            }).join("");

            return `
                <div class="survey-card">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                            <span class="doc-badge policy">${escapeHtml(s.category)}</span>
                            <span class="muted" style="font-size: 12px; font-weight: 700;">🗳️ ${total} Total Votes</span>
                        </div>
                        <h3 style="font-size: 17px; margin: 0 0 6px;">${escapeHtml(s.title)}</h3>
                        <p class="muted" style="font-size: 13.5px; line-height: 1.45; margin: 0 0 16px;">${escapeHtml(s.question)}</p>
                        <div style="display: flex; flex-direction: column; gap: 8px;">
                            ${optionsHtml}
                        </div>
                    </div>
                    ${s.user_voted_option ? `<div style="font-size: 12px; color: var(--success-color); font-weight: 700; margin-top: 4px;">✓ You voted for: "${escapeHtml(s.user_voted_option)}"</div>` : ''}
                </div>
            `;
        }).join("");
    } catch (err) {
        grid.innerHTML = `<div class="empty-state error" style="grid-column: 1 / -1;">Failed to load surveys: ${err.message}</div>`;
    }
}

async function voteSurveyOption(surveyId, option) {
    try {
        await apiRequest(`/surveys/${surveyId}/vote`, {
            method: "POST",
            body: { selected_option: option }
        });
        showNotification("Vote recorded successfully!", "success");
        await loadSurveys();
    } catch (err) {
        showNotification(err.message, "error");
    }
}

async function loadIdeas() {
    const feed = document.getElementById("ideasFeed");
    if (!feed) return;
    feed.innerHTML = `<div class="empty-state">Loading innovation suggestions...</div>`;

    try {
        const ideas = await apiRequest("/surveys/ideas");
        if (!ideas || ideas.length === 0) {
            feed.innerHTML = `<div class="empty-state">No suggestions posted yet. Share your ideas with the team!</div>`;
            return;
        }

        feed.innerHTML = ideas.map(idea => {
            const statusClass = `idea-status-${idea.status || 'under_review'}`;
            const statusLabel = (idea.status || 'under_review').replace('_', ' ').toUpperCase();
            return `
                <div class="idea-card">
                    <div class="upvote-box" onclick="upvoteIdeaItem(${idea.id})">
                        <span>▲</span>
                        <strong>${idea.upvotes_count || 1}</strong>
                        <small style="font-size: 10px;">VOTES</small>
                    </div>
                    <div class="idea-body">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                            <div>
                                <h3 style="margin: 0 0 4px; font-size: 16px;">${escapeHtml(idea.title)}</h3>
                                <small class="muted">Proposed by <strong>${escapeHtml(idea.author_name)}</strong> · ${escapeHtml(idea.category)}</small>
                            </div>
                            <span class="idea-status-tag ${statusClass}">${statusLabel}</span>
                        </div>
                        <p style="margin: 6px 0 12px; font-size: 13.5px; line-height: 1.5; color: var(--ink);">${escapeHtml(idea.description)}</p>
                        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border); padding-top: 8px;">
                            <div style="display: flex; gap: 8px; align-items: center;">
                                <label style="font-size: 11.5px; color: var(--muted); font-weight: 700;">ADMIN STATUS:</label>
                                <select onchange="updateIdeaStatusItem(${idea.id}, this.value)" style="padding: 2px 6px; font-size: 11px; border-radius: 6px; border: 1px solid var(--border);">
                                    <option value="under_review" ${idea.status === 'under_review' ? 'selected' : ''}>Under Review</option>
                                    <option value="planned" ${idea.status === 'planned' ? 'selected' : ''}>Planned</option>
                                    <option value="in_progress" ${idea.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
                                    <option value="implemented" ${idea.status === 'implemented' ? 'selected' : ''}>Implemented</option>
                                </select>
                            </div>
                            <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;" onclick="deleteIdeaItem(${idea.id})">Delete</button>
                        </div>
                    </div>
                </div>
            `;
        }).join("");
    } catch (err) {
        feed.innerHTML = `<div class="empty-state error">Failed to load ideas: ${err.message}</div>`;
    }
}

async function upvoteIdeaItem(id) {
    try {
        await apiRequest(`/surveys/ideas/${id}/upvote`, { method: "POST" });
        showNotification("Upvoted idea! 👍", "success");
        await loadIdeas();
    } catch (err) {
        showNotification(err.message, "error");
    }
}

async function updateIdeaStatusItem(id, status) {
    try {
        await apiRequest(`/surveys/ideas/${id}/status`, {
            method: "PATCH",
            body: { status }
        });
        showNotification(`Idea status updated to ${status.replace('_', ' ').toUpperCase()}.`, "success");
        await loadIdeas();
    } catch (err) {
        showNotification(err.message, "error");
    }
}

async function deleteIdeaItem(id) {
    if (!confirm("Are you sure you want to delete this idea?")) return;
    try {
        await apiRequest(`/surveys/ideas/${id}`, { method: "DELETE" });
        showNotification("Idea deleted.", "success");
        await loadIdeas();
    } catch (err) {
        showNotification(err.message, "error");
    }
}


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


function initTheme() {
    const savedTheme = localStorage.getItem("ems_theme") || "light";
    document.documentElement.setAttribute("data-theme", savedTheme);
    const themeBtn = document.getElementById("themeToggleBtn");
    if (themeBtn) {
        themeBtn.textContent = savedTheme === "dark" ? "☀️" : "🌙";
    }
}

function startLiveDigitalClock() {
    function tick() {
        const now = new Date();
        const timeEl = document.getElementById("digitalClockTime");
        const dateEl = document.getElementById("digitalClockDate");
        if (timeEl) {
            timeEl.textContent = now.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
        }
        if (dateEl) {
            dateEl.textContent = now.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
        }
    }
    tick();
    setInterval(tick, 1000);
}

document.addEventListener(
    "DOMContentLoaded",
    () => {
        initTheme();
        startLiveDigitalClock();
        const themeBtn = document.getElementById("themeToggleBtn");
        if (themeBtn) {
            themeBtn.addEventListener("click", () => {
                const currentTheme = document.documentElement.getAttribute("data-theme") || "light";
                const newTheme = currentTheme === "dark" ? "light" : "dark";
                document.documentElement.setAttribute("data-theme", newTheme);
                localStorage.setItem("ems_theme", newTheme);
                themeBtn.textContent = newTheme === "dark" ? "☀️" : "🌙";
            });
        }
        initializeApplication();
    }
);