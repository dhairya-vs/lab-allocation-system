from flask import Flask, request
from collections import deque

app = Flask(__name__)

# ================= LAB GENERATION =================
def generate_labs():
    labs = []
    for f in range(5):
        for i in range(1, 11):
            labs.append({"name": f"B{f}{i:02}", "capacity": 50})
    return labs


# ================= HOME =================
@app.route("/", methods=["GET"])
def home():
    return """
    <h2>Lab Allocation System</h2>

    <form method="POST" action="/allocate">

    <h3>Classes</h3>
    <div id="classes">
        <input name="class_name" placeholder="Class Name">
        <input name="students" placeholder="Students">
    </div>
    <button type="button" onclick="addClass()">Add Class</button>

    <h3>Time Slots</h3>
    <div id="slots">
        <input name="time_slot" placeholder="9-11">
    </div>
    <button type="button" onclick="addSlot()">Add Slot</button>

    <h3>Faculty</h3>
    <div id="faculties">
        <input name="faculty" placeholder="Faculty Name">
    </div>
    <button type="button" onclick="addFaculty()">Add Faculty</button>

    <br><br>
    <button type="submit">Allocate</button>

    </form>

    <script>
    function addClass() {
        document.getElementById('classes').innerHTML += `
            <br><input name="class_name" placeholder="Class Name">
            <input name="students" placeholder="Students">
        `;
    }

    function addSlot() {
        document.getElementById('slots').innerHTML += `
            <br><input name="time_slot" placeholder="Time Slot">
        `;
    }

    function addFaculty() {
        document.getElementById('faculties').innerHTML += `
            <br><input name="faculty" placeholder="Faculty Name">
        `;
    }
    </script>
    """


# ================= ALLOCATION =================
@app.route("/allocate", methods=["POST"])
def allocate():

    class_names = request.form.getlist("class_name")
    students_list = request.form.getlist("students")
    time_slots = request.form.getlist("time_slot")
    faculties = request.form.getlist("faculty")

    # Clean inputs
    classes = []
    for i in range(len(class_names)):
        if class_names[i] and students_list[i]:
            classes.append({
                "name": class_names[i],
                "students": int(students_list[i])
            })

    time_slots = [t for t in time_slots if t]
    faculties = [f for f in faculties if f]

    if not classes or not time_slots:
        return "<h3>Enter proper data</h3>"

    # ================= FACULTY SCHEDULE (DSA: Dictionary) =================
    faculty_schedule = {f: [] for f in faculties}

    def parse_time(slot):
        start, end = slot.split('-')
        return int(start), int(end)

    def is_available(faculty, slot):
        s1, e1 = parse_time(slot)

        for (s2, e2) in faculty_schedule[faculty]:
            # overlap condition
            if not (e1 <= s2 or s1 >= e2):
                return False
        return True

    # ================= SORT (GREEDY) =================
    classes.sort(key=lambda x: x["students"], reverse=True)

    # ================= SLOT DISTRIBUTION =================
    slot_map = {t: [] for t in time_slots}

    for i, c in enumerate(classes):
        slot = time_slots[i % len(time_slots)]
        slot_map[slot].append(c)

    labs = generate_labs()

    html = "<h2>Final Allocation</h2>"

    # ================= ALLOCATION =================
    for slot in time_slots:
        html += f"<h3>Time Slot: {slot}</h3>"

        available_labs = labs.copy()

        for c in slot_map[slot]:

            # ===== FACULTY ASSIGNMENT WITH CLASH CHECK =====
            assigned_faculty = None

            for f in faculties:
                if is_available(f, slot):
                    assigned_faculty = f
                    faculty_schedule[f].append(parse_time(slot))
                    break

            if assigned_faculty is None:
                html += f"<b>Class {c['name']}</b><br>"
                html += "<span style='color:orange'>→ No Faculty Available (Time Clash)</span><br><br>"
                continue

            # ===== STUDENT ALLOCATION (DSA: Queue) =====
            student_queue = deque(range(c["students"]))

            html += f"<b>Class {c['name']} (Faculty: {assigned_faculty})</b><br>"

            while student_queue and available_labs:
                lab = available_labs.pop(0)

                assigned = min(len(student_queue), lab["capacity"])

                for _ in range(assigned):
                    student_queue.popleft()

                html += f"→ {lab['name']} | {assigned}/50 students<br>"

            if student_queue:
                html += f"<span style='color:red'>Remaining: {len(student_queue)}</span><br>"

            html += "<br>"

    return html

# ================= VERCEL =================
handler = app
