# Issue Drafts: Calendar & Scheduling Features

This file contains proposed issue drafts for adding calendar and scheduling functionality to the Mergington High School Activities project. Review and convert these drafts into GitHub Issues as needed.

---

1) Title: Add calendar UI (Day/Week/Month views)
Labels: enhancement, frontend
Description:
Replace the current list view with a visual calendar. Integrate a calendar library (recommendation: FullCalendar for MIT license or DHTMLX Scheduler if you accept GPL/commercial terms). Convert `activities.schedule` into structured start/end datetimes and serve events as JSON for the calendar.

---

2) Title: Visual event rendering (multi-day events, stacking, "more" links)
Labels: enhancement, frontend
Description:
Render event bars in calendar grid, support multi-day events, stacking, and "more events" expansion in Month view. Ensure layout and event clipping behave well on mobile.

---

3) Title: Drag & drop / Resize events on calendar
Labels: feature, frontend, backend
Description:
Allow moving and resizing events in the calendar UI and persist changes to the API endpoints (update event start/end). Add server handlers to accept edits and validate conflicts.

---

4) Title: Add event editor modal (lightbox)
Labels: enhancement, frontend
Description:
Add a lightbox/modal to create and edit events with fields: title, start/end, full-day, description, max participants, recurrence options. Hook to signup/unregister flows and use the modal for event creation and edits.

---

5) Title: Recurring events (RRULE) support
Labels: feature, backend
Description:
Add recurrence rules storage (RRULE), render occurrences on frontend, and support edits for "this", "this and following", and full series. Consider using `rrule.js` to manage recurrence logic.

---

6) Title: Import / Export events (iCal / JSON)
Labels: enhancement, backend
Description:
Add endpoints to export events as iCal and JSON and to import iCal files. Useful for sharing schedules with external calendars and for backup/restore.

---

7) Title: Real-time updates (WebSocket) for event changes
Labels: feature, backend, realtime
Description:
Add a WebSocket endpoint to push event updates to connected clients (add/update/delete), so multiple users see live changes without polling.

---

8) Title: Blocked times / availability (markTimespan)
Labels: feature, backend
Description:
Add an API and UI to mark blocked times (e.g., no bookings allowed) and check conflicts when signing up or editing events. Provide admin UI to create and remove blocked times.

---

9) Title: Export to PDF/PNG or integration with export service
Labels: enhancement, backend
Description:
Add an export option for printable calendar views (PDF/PNG). Option: integrate an online export service or implement a server-side headless browser to capture calendar images/PDFs.

---

10) Title: Authentication / permission model for signups
Labels: security, backend
Description:
Replace the current email query param approach with authenticated users and role-based permissions (admins to create/edit events, students to sign up/unregister). Consider integrating a simple OAuth or token-based auth and enforcing rate limits.

---

(If you'd like different labels, assignees, or prioritization, update the drafts before converting to Issues.)
