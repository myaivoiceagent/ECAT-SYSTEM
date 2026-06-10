import os
import json
import datetime
import random
import uuid
import re
import streamlit as st
import streamlit.components.v1 as components

# --------------------------------------------------
# CONFIGURATION & STATE INITIALIZATION
# --------------------------------------------------
st.set_page_config(page_title="UET-ECAT Test Portal", page_icon="📝", layout="centered")

# Initialize persistent session variables
if "page" not in st.session_state:
    st.session_state.page = "Main Menu"
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None  # Holds user data dict
if "active_quiz" not in st.session_state:
    st.session_state.active_quiz = None  # Holds shuffled questions list
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}  # Tracks user options selected
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

# Helper to automatically verify file structures exist
def init_json_file(filename):
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        with open(filename, "w") as f:
            json.dump([], f, indent=4)

init_json_file("Admin.json")
init_json_file("Login.json")
init_json_file("Quizz.json")
init_json_file("Result.json")

# Ensure Default Admin exists
with open("Admin.json", "r") as f:
    admins = json.load(f)
if not any(a.get("Admin Name") == "Zargham - Ullah" for a in admins):
    admins.append({
        "Admin Id": str(uuid.uuid4()),
        "Admin Name": "Zargham - Ullah",
        "Password": "1234_qwe@"
    })
    with open("Admin.json", "w") as f:
        json.dump(admins, f, indent=4)

# Helper functions for data management
def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# --------------------------------------------------
# WEB VIEWS & UI
# --------------------------------------------------

# Header Logo/Title
st.title("🎓 UET-ECAT Test Management Portal")
st.write("---")

# Main Application Router
if st.session_state.page == "Main Menu":
    st.subheader("Select a Section to Begin:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛡️ Admin Portal", use_container_width=True):
            st.session_state.page = "Admin Key Verification"
            st.rerun()
    with col2:
        if st.button("🧑 Student Portal", use_container_width=True):
            st.session_state.page = "Student Auth Menu"
            st.rerun()
    with col3:
        if st.button("✍️ Take ECAT Test", use_container_width=True):
            st.session_state.page = "ECAT Test Login"
            st.rerun()

# --- ADMIN FLOW ---
elif st.session_state.page == "Admin Key Verification":
    st.subheader("🛡️ Admin Security Check")
    secret_key = st.text_input("Enter Admin Secret Key:", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Verify Key"):
            if secret_key == "UET-ECAT-ADMIN":
                st.session_state.page = "Admin Login"
                st.rerun()
            else:
                st.error("Access Denied: Incorrect Secret Key.")
    with col2:
        if st.button("Back to Main Menu"):
            st.session_state.page = "Main Menu"
            st.rerun()

elif st.session_state.page == "Admin Login":
    st.subheader("🛡️ Admin Account Login")
    admin_name = st.text_input("Admin Username:")
    admin_pass = st.text_input("Admin Password:", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            admins = load_json("Admin.json")
            found = False
            for a in admins:
                if a["Admin Name"].lower() == admin_name.lower() and a["Password"] == admin_pass:
                    found = True
                    st.session_state.logged_in_user = "Admin"
                    st.session_state.page = "Admin Dashboard"
                    st.success("Admin Login Successful!")
                    st.rerun()
            if not found:
                st.error("Invalid Admin Username or Password.")
    with col2:
        if st.button("Cancel"):
            st.session_state.page = "Main Menu"
            st.rerun()

elif st.session_state.page == "Admin Dashboard":
    st.subheader("🎛️ Admin Control Dashboard")
    st.write(f"Logged in as: **Zargham - Ullah**")
    
    if st.button("🚪 Logout Admin", type="primary"):
        st.session_state.logged_in_user = None
        st.session_state.page = "Main Menu"
        st.rerun()
        
    st.write("---")
    
    # Tab Layout for options 1 through 6
    t1, t2, t3, t4, t5 = st.tabs([
        "➕ Add/Manage Sections", 
        "📝 Add/Edit Questions", 
        "❌ Remove Questions", 
        "👥 Registered Users", 
        "📊 User Results"
    ])
    
    with t1:
        st.markdown("### Create New Quiz Section")
        new_sec = st.text_input("Section/Subject Name (e.g., Mathematics):")
        if st.button("Add Section"):
            if new_sec:
                quizz_data = load_json("Quizz.json")
                if any(s["Section"].lower() == new_sec.lower() for s in quizz_data):
                    st.warning("Section already exists!")
                else:
                    quizz_data.append({"Section": new_sec, "Questions": []})
                    save_json("Quizz.json", quizz_data)
                    st.success(f"Section '{new_sec}' added successfully!")
            else:
                st.error("Please provide a name.")
                
    with t2:
        st.markdown("### Add Question to Existing Section")
        quizz_data = load_json("Quizz.json")
        sections = [s["Section"] for s in quizz_data]
        
        if not sections:
            st.info("No quiz sections found. Add a section first.")
        else:
            sel_sec = st.selectbox("Select Target Section:", sections, key="add_q_sec")
            q_text = st.text_area("Question Text:")
            op_a = st.text_input("Option A:")
            op_b = st.text_input("Option B:")
            op_c = st.text_input("Option C:")
            op_d = st.text_input("Option D:")
            cor_ans = st.selectbox("Correct Answer Option:", ["A", "B", "C", "D"])
            
            if st.button("Save Question"):
                if q_text and op_a and op_b and op_c and op_d:
                    for s in quizz_data:
                        if s["Section"] == sel_sec:
                            s["Questions"].append({
                                "Question No": len(s["Questions"]) + 1,
                                "Question": q_text,
                                "Options": {"A": op_a, "B": op_b, "C": op_c, "D": op_d},
                                "Correct Answer": cor_ans
                            })
                            break
                    save_json("Quizz.json", quizz_data)
                    st.success("Question successfully added to section!")
                else:
                    st.error("All input fields are mandatory to save a question.")
                    
    with t3:
        st.markdown("### Remove Questions")
        quizz_data = load_json("Quizz.json")
        sections = [s["Section"] for s in quizz_data]
        if sections:
            sel_sec_rem = st.selectbox("Select Section to Clean:", sections, key="rem_q_sec")
            target_sec = next(s for s in quizz_data if s["Section"] == sel_sec_rem)
            
            if not target_sec["Questions"]:
                st.info("No questions present inside this section.")
            else:
                q_list = [f"{q['Question No']}: {q['Question'][:40]}..." for q in target_sec["Questions"]]
                selected_q_str = st.selectbox("Choose Question to Drop:", q_list)
                q_no = int(selected_q_str.split(":")[0])
                
                if st.button("Delete Question", type="primary"):
                    target_sec["Questions"] = [q for q in target_sec["Questions"] if q["Question No"] != q_no]
                    # Renumber remaining questions
                    for idx, q in enumerate(target_sec["Questions"], start=1):
                        q["Question No"] = idx
                    save_json("Quizz.json", quizz_data)
                    st.success("Question dropped successfully!")
                    st.rerun()
                    
    with t4:
        st.markdown("### Registered Users Registry")
        users = load_json("Login.json")
        if not users:
            st.info("No student sign-ups found.")
        else:
            for u in users:
                with st.expander(f"👤 {u['User Name']} ({u['Email']})"):
                    st.text(f"User ID: {u['User ID']}\nPassword: {u['Password']}")
                    if u.get("Login"):
                        st.text(f"Last Login: {u['Login'][-1]['Login Date & Time']['Login Date']} at {u['Login'][-1]['Login Date & Time']['Login Time']}")
                    else:
                        st.text("Login Metrics: Never Logged In")
                        
    with t5:
        st.markdown("### Student ECAT Score Cards")
        results = load_json("Result.json")
        if not results:
            st.info("No score sheets saved yet.")
        else:
            for r in results:
                st.markdown(f"**Student:** {r['User Name']} (`{r['User Email']}`)")
                st.json(r['User Result'][0])
                st.write("---")

# --- USER AUTHENTICATION FLOW ---
elif st.session_state.page == "Student Auth Menu":
    st.subheader("🧑 Student Registration & Login Portal")
    mode = st.radio("Choose Action:", ["User Login", "Create New Account"])
    
    if mode == "User Login":
        login_email = st.text_input("Registered Email:")
        login_user = st.text_input("Username:")
        login_pass = st.text_input("Password:", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Log In"):
                users = load_json("Login.json")
                found = False
                for u in users:
                    if u["Email"].lower() == login_email.lower() and u["User Name"].lower() == login_user.lower() and u["Password"] == login_pass:
                        found = True
                        u["Login"].append({
                            "Login Date & Time": {
                                "Login Date": datetime.datetime.now().strftime("%d-%m-%Y"),
                                "Login Time": datetime.datetime.now().strftime("%H:%M:%S")
                            }
                        })
                        save_json("Login.json", users)
                        st.success(f"Welcome back, {u['User Name']}! Use the Main Menu to initiate your ECAT evaluation.")
                        break
                if not found:
                    st.error("Authentication credentials unmatched.")
        with col2:
            if st.button("Return Main Menu"):
                st.session_state.page = "Main Menu"
                st.rerun()
                
    else:
        reg_email = st.text_input("Enter Email Address:")
        reg_name = st.text_input("Enter Full Name:")
        reg_pass = st.text_input("Create Password (min 6 characters):", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Register Account"):
                pattern = r"^[a-zA-Z0-9._]+@[a-zA-Z]+\.[a-zA-Z]+$"
                users = load_json("Login.json")
                
                if not re.search(pattern, reg_email):
                    st.error("Incorrect email format scheme.")
                elif len(reg_pass) < 6:
                    st.error("Password condition unmet (minimum 6 variables).")
                elif any(u["Email"].lower() == reg_email.lower() for u in users):
                    st.error("This email infrastructure is already taken.")
                else:
                    users.append({
                        "User ID": str(uuid.uuid4()),
                        "User Name": reg_name,
                        "Email": reg_email,
                        "Password": reg_pass,
                        "Login": []
                    })
                    save_json("Login.json", users)
                    st.success("Account setup successful! You can now log in.")
        with col2:
            if st.button("Return Main Menu"):
                st.session_state.page = "Main Menu"
                st.rerun()

# --- EXAM LOGISTICS FLOW ---
elif st.session_state.page == "ECAT Test Login":
    st.subheader("✍️ Verification Prior to ECAT Initialization")
    test_email = st.text_input("Registered Student Email:")
    test_user = st.text_input("Username:")
    test_pass = st.text_input("Password:", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Verify Identity & Proceed"):
            users = load_json("Login.json")
            matched_student = None
            for u in users:
                if u["Email"].lower() == test_email.lower() and u["User Name"].lower() == test_user.lower() and u["Password"] == test_pass:
                    matched_student = u
                    break
            if matched_student:
                st.session_state.logged_in_user = matched_student
                st.session_state.page = "ECAT Subject Selection"
                st.rerun()
            else:
                st.error("No record matches those inputs.")
    with col2:
        if st.button("Back"):
            st.session_state.page = "Main Menu"
            st.rerun()

elif st.session_state.page == "ECAT Subject Selection":
    st.subheader("📚 Subject Selection Criteria")
    st.info("English is a mandatory system requirement. Choose 3 supplementary subjects below:")
    
    quizz_data = load_json("Quizz.json")
    available_subjects = [s["Section"] for s in quizz_data if s["Section"].lower() != "english"]
    
    if len(available_subjects) < 3:
        st.error(f"Insufficient custom tracks created in database. Requires 3 alternative disciplines. Current non-English count: {len(available_subjects)}")
        if st.button("Main Menu"):
            st.session_state.page = "Main Menu"
            st.rerun()
    else:
        chosen_tracks = st.multiselect("Pick exactly 3 evaluation branches:", available_subjects)
        
        if st.button("Assemble Test Matrix"):
            if len(chosen_tracks) != 3:
                st.error("Constraint Violation: You must select exactly 3 items.")
            else:
                all_questions = []
                # Compile English core requirements (Max 10 sample)
                eng_sec = next((s for s in quizz_data if s["Section"].lower() == "english"), None)
                if eng_sec and eng_sec["Questions"]:
                    all_questions.extend(random.sample(eng_sec["Questions"], min(10, len(eng_sec["Questions"]))))
                    
                # Compile custom branch requirements (Max 30 sample each)
                for track in chosen_tracks:
                    t_sec = next(s for s in quizz_data if s["Section"] == track)
                    if t_sec["Questions"]:
                        all_questions.extend(random.sample(t_sec["Questions"], min(30, len(t_sec["Questions"]))))
                        
                if not all_questions:
                    st.error("No questions were found inside the selected sections.")
                else:
                    random.shuffle(all_questions)
                    st.session_state.active_quiz = all_questions
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.session_state.page = "Live Examination"
                    st.rerun()
                    st.session_state.start_time = datetime.datetime.now().timestamp()
                    st.session_state.page = "Live Examination"
                    st.rerun()

elif st.session_state.page == "Live Examination":
    student = st.session_state.logged_in_user
    
    # ------------------------------------------------------------------------
    # ⏱️ 100-MINUTE TIMER CODE (YAHAN PASTE KAREIN)
    # ------------------------------------------------------------------------
    total_allowed_seconds = 100 * 60  # 100 minutes = 6000 seconds
    current_time_stamp = datetime.datetime.now().timestamp()
    elapsed_seconds = int(current_time_stamp - st.session_state.start_time)
    remaining_seconds = max(0, total_allowed_seconds - elapsed_seconds)
    
    st.markdown(f"### 📝 Live Examination Environment (Candidate: **{student['User Name']}**)")
    
    timer_html = f"""
    <div style="background-color: #ffebee; padding: 15px; border-radius: 8px; border: 2px solid #ef5350; text-align: center; margin-bottom: 20px;">
        <span style="font-size: 16px; color: #c62828; font-weight: bold; font-family: sans-serif;">🚨 TIME REMAINING: </span>
        <span id="countdown-clock" style="font-size: 24px; color: #b71c1c; font-weight: bold; font-family: monospace;">--:--</span>
    </div>

    <script>
        var timeLeft = {remaining_seconds};
        var timerDisplay = document.getElementById('countdown-clock');
        
        function updateTimer() {{
            if (timeLeft <= 0) {{
                timerDisplay.innerHTML = "00:00 - TIME OVER!";
                window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'timeout'}}, '*');
                clearInterval(intervalInstance);
            }} else {{
                var minutes = Math.floor(timeLeft / 60);
                var seconds = timeLeft % 60;
                if (minutes < 10) minutes = "0" + minutes;
                if (seconds < 10) seconds = "0" + seconds;
                timerDisplay.innerHTML = minutes + ":" + seconds;
                timeLeft--;
            }}
        }}
        updateTimer();
        var intervalInstance = setInterval(updateTimer, 1000);
    </script>
    """
    
    timer_signal = components.html(timer_html, height=100, scroller=False)
    
    if timer_signal == "timeout" or remaining_seconds <= 0:
        st.error("⏰ Time's Up! Auto-submitting your paper...")
        st.session_state.page = "Grade Evaluation Processing"
        st.rerun()
        
    st.write("---")
    # ------------------------------------------------------------------------
    # TIMER CODE KHATAM (Iske niche aapka baki ka questions wala code waise hi chalega)
    # ------------------------------------------------------------------------

    # Aapka purana code jo questions display karta hai...
    questions = st.session_state.active_quiz
    # (Baki saara code niche chalne dein)

elif st.session_state.page == "Grade Evaluation Processing":
    st.subheader("📊 Output Metric Breakdown")
    
    questions = st.session_state.active_quiz
    answers = st.session_state.quiz_answers
    student = st.session_state.logged_in_user
    
    correct_count = 0
    wrong_count = 0
    
    for idx, q in enumerate(questions, start=1):
        user_choice = answers.get(idx, "Unanswered")
        if user_choice == q["Correct Answer"]:
            correct_count += 1
        else:
            wrong_count += 1
            
    total_q = len(questions)
    total_marks = total_q * 4
    calculated_marks = (correct_count * 4) - (wrong_count * 1) # Applied standard engineering negative weighting layout logic adjustments
    final_score = max(0, calculated_marks)
    
    # Append to Result.json database layout structure
    results_db = load_json("Result.json")
    results_db.append({
        "USER ID": student["User ID"],
        "User Name": student["User Name"],
        "User Email": student["Email"],
        "User Result": [{
            "Total Questions": total_q,
            "Total Marks": total_marks,
            "Obtained Marks": final_score
        }]
    })
    save_json("Result.json", results_db)
    
    # Display Result Dashboard UI Card component blocks
    st.balloons()
    st.success("Test Logged Safely in Central Registry Ledger Databases.")
    
    st.markdown("### 🏆 Exam Metric Performance Summary")
    st.metric(label="Calculated Scale Output Grade", value=f"{final_score} / {total_marks}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Items Evaluated", total_q)
    col2.metric("True Positives (Correct)", correct_count)
    col3.metric("Falsified Weights (Wrong)", wrong_count)
    
    if st.button("Return Main Portal Home"):
        st.session_state.page = "Main Menu"
        st.session_state.active_quiz = None
        st.session_state.quiz_answers = {}
        st.session_state.logged_in_user = None
        st.rerun()