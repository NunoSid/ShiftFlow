# ShiftFlow Manual (EN)

## 1) Overview
ShiftFlow is a web platform for planning, distributing, and publishing schedules. Professional groups (roles) are configurable for each hospital. It includes professional management, requirements, availability, monthly rules, automatic scheduling, swaps, chat, and exports.

## 2) Roles and permissions

### ADMIN
- Create, edit, and delete users.
- Define platform and clinic/hospital name.
- Upload and toggle logos (ShiftFlow and organization).
- Change UI colors.
- Configure PDF footer text.
- Create/edit/remove professional categories and their roles.
- Create/edit/remove teams, services, shifts, and service-shift associations.
- Create/edit/remove professionals.
- Generate schedules, publish, edit/lock, clear schedules.
- Approve/reject availability requests.
- Approve/reject swaps.
- Export schedule, availability, and swaps.

### COORDINATOR
- Create/edit/remove teams, services, shifts, and associations.
- Create/edit/remove professionals.
- Generate schedules, publish, edit/lock, clear schedules.
- Approve/reject availability requests.
- Approve/reject swaps (with reason).
- Export schedule, availability, and swaps.

### NURSE
- View schedule, requirements, and notices.
- Submit availability/unavailability (for approval).
- Request shift swaps.
- Chat with other users.
- Export schedule, availability, and swaps.

### OPERATIONAL ASSISTANT
- View schedule, requirements, and notices.
- Submit availability/unavailability (for approval).
- Request shift swaps.
- Chat with other users.
- Export schedule, availability, and swaps.

## 3) Login and language
- Language can be changed on the login screen and in the top bar.
- The choice is saved in the browser.
- All UI texts switch between PT and EN.
- The **Team** selector on the top bar lists all configured roles.

## 4) Menu structure

### Dashboard
- **Generate schedule** (Admin/Coordinator).
- **Export schedule** (all roles).
- **Export availability** (all roles).
- Indicators: requirements, assigned shifts, locks, alerts.

### Professionals
- List of professionals (name, user, allowed services, weekly hours, balance).
- Add/edit/remove professional.
- Link user to professional.
- Set category, allowed services, weekly hours, night permission, max nights/month.

### Requirements
- Monthly grid by **Service/Shift** and by day.
- Quick fill (1 in all cells) or clear.
- Save to persist for the current month.

### Availability / Requests
- Monthly grid by professional/day (Admin/Coordinator).
- **My availability**: each user fills their own map and submits for approval.
- Approve/reject pending requests.

### Month rules
- Define weekly hour limits and target average.
- Define minimum rest rules.
- Solver penalties.
- Month holidays (auto) and manual holidays.
- Manual adjustments (worked holidays, extra hours, reductions).
- Shift catalog (start/end per code).

### Monthly schedule
- Monthly grid by professional/day.
- Edit cell with floating editor.
- Quick lock/unlock (L key).
- Clear cell (Delete).
- Publish schedule per team.
- Stats: hours per professional and count of mornings/afternoons/nights/off/rest/vacation.
- Lists of uncovered requirements and alerts.

### Teams
- Create teams per configured role (any role defined in categories).
- Associate service and team members.

### Services and shifts
- Create/edit services (with color) for any role.
- Create shifts (code, label, type, start/end).
- Associate services to shifts.

### Swap requests
- Request swap (date, current/desired shift, reason and notes).
- Participants accept/reject.
- Coordinator approves/rejects (optional reason).
- Export swap list.

### Chat
- User list by role.
- Organized conversations.
- Archive/Delete only for the user who clicks.
- Visual alerts for unread messages.

### Admin
- Configure platform/organization names.
- Logos (upload and visibility).
- Colors.
- PDF footer text (editable, empty by default).
- Professional categories.
- Users (create, edit, delete).
- Create/Delete demos.

## 5) Exports
- **Schedule**: Excel or PDF.
- **Availability**: Excel or PDF.
- **Swaps**: Excel.
- In PDF: logos (if enabled), shift legend, configurable footer.

## 6) Seed and demo data
- `SHIFTFLOW_SEED_MODE=demo` creates:
  - Demo users
  - Linked professionals
  - Demo services and shifts
  - Demo requirements for current month
- Admin buttons **Create demos** and **Delete demos**.

## 7) Install and start
- `./start.sh` creates `.env` from `.env.example`, prepares the environment, and starts the server.
- Access `http://localhost:8010/`.

## 8) Tips
- For remote access: run with `--host 0.0.0.0` and open port 8010.
- PDF footer text is empty by default and can be edited in Admin.
