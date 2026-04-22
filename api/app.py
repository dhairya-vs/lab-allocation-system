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
    <input name="class_name">
    <input name="students"><br><br>

    <h3>Time Slots</h3>
    <input name="time_slot"><br><br>

    <h3>Faculty</h3>
    <input name="faculty"><br><br>

    <button type="submit">Allocate</button>
    </form>
    """


# ================= ALLOCATION =================
@app.route("/allocate", methods=["POST"])
def allocate():

    # get inputs (multiple allowed)
    class_names = request.form.getlist("class_name")
    students_list = request.form.getlist("students")
    time_slots = request.form.getlist("time_slot")
    faculties = request.form.getlist("faculty")

    # clean inputs
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
            student_queue = deque(range(c["students"]))

            html += f"<b>Class {c['name']}</b><br>"

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


app = Flask(__name__)

# THIS IS REQUIRED FOR VERCEL
handler = app
