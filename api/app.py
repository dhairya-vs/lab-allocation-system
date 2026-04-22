from collections import deque

print("=== Lab Resource Allocation System (Time Slot + Parallel) ===\n")

# ================================
# STEP 1: GENERATE LABS
# ================================

labs = []

floors = 5
labs_per_floor = 10
capacity_per_lab = 50

for f in range(floors):
    for i in range(1, labs_per_floor + 1):
        lab_number = f"B{f}{i:02}"
        labs.append({
            "name": lab_number,
            "capacity": capacity_per_lab
        })

print(f"Total labs per slot: {len(labs)}\n")

# ================================
# STEP 2: INPUT CLASSES
# ================================

classes = []

n = int(input("Enter number of classes: "))
for _ in range(n):
    name = input("Class name: ")
    students = int(input("Number of students: "))
    classes.append({"name": name, "students": students})

# ================================
# STEP 3: INPUT TIME SLOTS
# ================================

time_slots = []

n = int(input("\nEnter number of time slots: "))
for _ in range(n):
    t = input("Time slot: ")
    time_slots.append(t)

# ================================
# STEP 4: GREEDY SORT (BIG FIRST)
# ================================

classes.sort(key=lambda x: x["students"], reverse=True)

# ================================
# STEP 5: DISTRIBUTE CLASSES INTO SLOTS
# ================================

slot_map = {t: [] for t in time_slots}

for i, c in enumerate(classes):
    slot = time_slots[i % len(time_slots)]
    slot_map[slot].append(c)

# ================================
# STEP 6: ALLOCATION PER SLOT
# ================================

final_allocation = {}

for slot in time_slots:
    available_labs = labs.copy()  # labs reused per slot
    final_allocation[slot] = {}

    for c in slot_map[slot]:
        student_queue = deque(range(c["students"]))
        final_allocation[slot][c["name"]] = []

        while student_queue and available_labs:
            lab = available_labs.pop(0)

            # ✅ STRICT CAP FIX
            assigned = min(len(student_queue), lab["capacity"])

            for _ in range(assigned):
                student_queue.popleft()

            final_allocation[slot][c["name"]].append({
                "lab": lab["name"],
                "students": assigned
            })

        if student_queue:
            final_allocation[slot][c["name"]].append({
                "lab": "Not Enough Labs",
                "students": len(student_queue)
            })

# ================================
# STEP 7: OUTPUT
# ================================

print("\n" + "="*60)
print(" FINAL LAB ALLOCATION ")
print("="*60)

for slot, classes_data in final_allocation.items():
    print(f"\n⏰ Time Slot: {slot}")
    for cls, entries in classes_data.items():
        print(f"  Class: {cls}")
        for e in entries:
            print(f"    → Lab {e['lab']} | {e['students']}/50 students")

print("\n" + "="*60)