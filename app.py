import os
import json
import datetime
import random
import uuid
import re
import streamlit as st

# --------------------------------------------------
# CONFIGURATION & STATE INITIALIZATION
# --------------------------------------------------
st.set_page_config(page_title="UET-ECAT Test Portal", page_icon="📝", layout="centered")

# Initialize persistent session variables safely
if "page" not in st.session_state:
    st.session_state.page = "Main Menu"
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None  
if "active_quiz" not in st.session_state:
    st.session_state.active_quiz = None  
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}  
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "result_saved" not in st.session_state:
    st.session_state.result_saved = False

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
# WEB VIEWS & UI ROUTER
# --------------------------------------------------
st.title("🎓 UET-ECAT Test Management Portal")
st.write("---")

# MAIN MENU
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

# ADMIN KEY VERIFICATION
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

# ADMIN LOGIN
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
                    st.rerun()
            if not found:
                st.error("Invalid Admin Username or Password.")
    with col2:
        if st.button("Cancel"):
            st.session_state.page = "Main Menu"
            st.rerun()

# ADMIN DASHBOARD
elif st.session_state.page == "Admin Dashboard":
    st.subheader("🎛️ Admin Control Dashboard")
    st.write("Logged in as: **Zargham - Ullah**")
    
    if st.button("🚪 Logout Admin", type="primary"):
        st.session_state.logged_in_user = None
        st.session_state.page = "Main Menu"
        st.rerun()
        
    st.write("---")
    t1, t2, t3, t4, t5 = st.tabs(["➕ Add Sections", "📝 Add Questions", "❌ Remove Questions", "👥 Users", "📊 Results"])
    
    with t1:
        new_sec = st.text_input("Section Name:")
        if st.button("Add Section"):
            if new_sec:
                quizz_data = load_json("Quizz.json")
                if any(s["Section"].lower() == new_sec.lower() for s in quizz_data):
                    st.warning("Section exists!")
                else:
                    quizz_data.append({"Section": new_sec, "Questions": []})
                    save_json("Quizz.json", quizz_data)
                    st.success("Section Added!")
                    
    with t2:
        quizz_data = load_json("Quizz.json")
        sections = [s["Section"] for s in quizz_data]
        if sections:
            sel_sec = st.selectbox("Select Target Section:", sections)
            q_text = st.text_area("Question Content:")
            op_a = st.text_input("Option A:")
            op_b = st.text_input("Option B:")
            op_c = st.text_input("Option C:")
            op_d = st.text_input("Option D:")
            cor_ans = st.selectbox("Correct Option:", ["A", "B", "C", "D"])
            if st.button("Save Question"):
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
                st.success("Question Saved!")

    with t3:
        quizz_data = load_json("Quizz.json")
        sections = [s["Section"] for s in quizz_data]
        if sections:
            sel_sec_rem = st.selectbox("Select Section:", sections, key="rem_sec")
            target_sec = next(s for s in quizz_data if s["Section"] == sel_sec_rem)
            if target_sec["Questions"]:
                q_list = [f"{q['Question No']}: {q['Question'][:30]}..." for q in target_sec["Questions"]]
                selected_q_str = st.selectbox("Choose Question:", q_list)
                q_no = int(selected_q_str.split(":")[0])
                if st.button("Delete Question"):
                    target_sec["Questions"] = [q for q in target_sec["Questions"] if q["Question No"] != q_no]
                    for idx, q in enumerate(target_sec["Questions"], start=1):
                        q["Question No"] = idx
                    save_json("Quizz.json", quizz_data)
                    st.rerun()

    with t4:
        users = load_json("Login.json")
        for u in users:
            st.write(f"👤 **{u['User Name']}** ({u['Email']})")

    with t5:
        results = load_json("Result.json")
        for r in results:
            st.write(f"🔹 **{r['User Name']}** - Marks: {r['User Result'][0]['Obtained Marks']}")

# STUDENT AUTHENTICATION
elif st.session_state.page == "Student Auth Menu":
    st.subheader("🧑 Student Registration & Login")
    mode = st.radio("Action:", ["User Login", "Create Account"])
    
    if mode == "User Login":
        login_email = st.text_input("Email:")
        login_user = st.text_input("Username:")
        login_pass = st.text_input("Password:", type="password")
        if st.button("Log In"):
            users = load_json("Login.json")
            found = False
            for u in users:
                if u["Email"].lower() == login_email.lower() and u["User Name"].lower() == login_user.lower() and u["Password"] == login_pass:
                    found = True
                    st.session_state.page = "Main Menu"
                    st.success("Login Successful!")
                    st.rerun()
            if not found:
                st.error("Invalid Credentials.")
    else:
        reg_email = st.text_input("Email:")
        reg_name = st.text_input("Full Name:")
        reg_pass = st.text_input("Password:", type="password")
        if st.button("Register"):
            users = load_json("Login.json")
            if len(reg_pass) < 6:
                st.error("Min 6 chars required.")
            elif any(u["Email"].lower() == reg_email.lower() for u in users):
                st.error("Email taken.")
            else:
                users.append({"User ID": str(uuid.uuid4()), "User Name": reg_name, "Email": reg_email, "Password": reg_pass, "Login": []})
                save_json("Login.json", users)
                st.success("Registered Successfully!")
    if st.button("Back"):
        st.session_state.page = "Main Menu"
        st.rerun()

# ECAT TEST LOGIN
elif st.session_state.page == "ECAT Test Login":
    st.subheader("✍️ Verification Prior to ECAT")
    test_email = st.text_input("Student Email:")
    test_user = st.text_input("Username:")
    test_pass = st.text_input("Password:", type="password")
    if st.button("Verify Identity"):
        users = load_json("Login.json")
        matched = None
        for u in users:
            if u["Email"].lower() == test_email.lower() and u["User Name"].lower() == test_user.lower() and u["Password"] == test_pass:
                matched = u
                break
        if matched:
            st.session_state.logged_in_user = matched
            st.session_state.page = "ECAT Subject Selection"
            st.rerun()
        else:
            st.error("No record found.")
    if st.button("Back"):
        st.session_state.page = "Main Menu"
        st.rerun()

# ECAT SUBJECT SELECTION
elif st.session_state.page == "ECAT Subject Selection":
    st.subheader("📚 Subject Selection Criteria")
    quizz_data = load_json("Quizz.json")
    available_subjects = [s["Section"] for s in quizz_data if s["Section"].lower() != "english"]
    
    if len(available_subjects) < 3:
        st.error("Database needs at least 3 subjects alternative to English.")
    else:
        chosen_tracks = st.multiselect("Pick exactly 3 branches:", available_subjects)
        if st.button("Assemble Test Matrix"):
            if len(chosen_tracks) != 3:
                st.error("Select exactly 3 items.")
            else:
                all_questions = []
                eng_sec = next((s for s in quizz_data if s["Section"].lower() == "english"), None)
                if eng_sec and eng_sec["Questions"]:
                    all_questions.extend(random.sample(eng_sec["Questions"], min(10, len(eng_sec["Questions"]))))
                for track in chosen_tracks:
                    t_sec = next(s for s in quizz_data if s["Section"] == track)
                    if t_sec["Questions"]:
                        all_questions.extend(random.sample(t_sec["Questions"], min(30, len(t_sec["Questions"]))))
                
                if not all_questions:
                    st.error("No questions found.")
                else:
                    random.shuffle(all_questions)
                    st.session_state.active_quiz = all_questions
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.session_state.start_time = datetime.datetime.now().timestamp()
                    st.session_state.page = "Live Examination"
                    st.rerun()

# ------------------------------------------------------------------------
# LIVE EXAMINATION (SMOOTH TIMER & UNSELECTED OPTIONS)
# ------------------------------------------------------------------------
elif st.session_state.page == "Live Examination":
    student = st.session_state.logged_in_user
    
    if "start_time" not in st.session_state:
        st.session_state.start_time = datetime.datetime.now().timestamp()
        
    total_allowed_seconds = 100 * 60  
    current_time_stamp = datetime.datetime.now().timestamp()
    elapsed = int(current_time_stamp - st.session_state.start_time)
    remaining = max(0, total_allowed_seconds - elapsed)
    
    st.markdown(f"### 📝 Live Exam Branch (Candidate: **{student['User Name']}**)")
    
    # ⏱️ Smooth Live Timer Section using Streamlit's structural layout
    if remaining <= 0:
        st.error("⏰ Time Limit Reached! Auto-evaluating responses...")
        st.session_state.page = "Grade Evaluation Processing"
        st.rerun()
    else:
        mins, secs = divmod(remaining, 60)
        # Danger alert box showing real-time countdown nicely
        st.error(f"⏱️ **Time Remaining: {int(mins):02d}:{int(secs):02d}**")
        
    st.write("---")
    questions = st.session_state.active_quiz

    if questions:
        for idx, q in enumerate(questions, start=1):
            st.write(f"**Q{idx}. {q['Question']}**")
            
            # Check if user already answered this previously during a rerun
            current_ans = st.session_state.quiz_answers.get(idx, None)
            
            if current_ans in ["A", "B", "C", "D"]:
                default_idx = ["A", "B", "C", "D"].index(current_ans)
            else:
                default_idx = None  # 👈 Yeh line options ko pehle se select hone se rokegi!

            answer = st.radio(
                f"Select option for question {idx}:", 
                ["A", "B", "C", "D"], 
                index=default_idx, # 👈 index=None hoga toh default khali rahega
                format_func=lambda x: f"{x}. {q['Options'][x]}",
                key=f"live_q_{idx}"
            )
            
            # Save the answer only if the user actually clicked something
            if answer is not None:
                st.session_state.quiz_answers[idx] = answer
            st.write("")

        # Add a manual refresh button so they can update the timer anytime, 
        # or it will automatically update whenever they answer any question!
        col_submit, col_ref = st.columns([4, 1])
        with col_submit:
            if st.button("Submit Test", type="primary", use_container_width=True):
                st.session_state.page = "Grade Evaluation Processing"
                st.rerun()
        with col_ref:
            if st.button("🔄 Refresh Timer", use_container_width=True):
                st.rerun()
    else:
        st.warning("No dynamic questions resolved.")

# ------------------------------------------------------------------------
# GRADE EVALUATION PROCESSING (LOCAL PURE CSS FIREWORKS - NO EXTERNAL LINKS)
# ------------------------------------------------------------------------
elif st.session_state.page == "Grade Evaluation Processing":
    st.subheader("📊 Output Metric Breakdown")
    questions = st.session_state.active_quiz
    answers = st.session_state.quiz_answers
    student = st.session_state.logged_in_user
    
    correct_count = 0
    wrong_count = 0
    unanswered_count = 0  
    
    if questions:
        for idx, q in enumerate(questions, start=1):
            user_choice = answers.get(idx, None)
            
            if user_choice is None:
                unanswered_count += 1  
            elif user_choice == q["Correct Answer"]:
                correct_count += 1
            else:
                wrong_count += 1
                
        total_q = len(questions)
        total_marks = total_q * 4
        
        calculated_marks = (correct_count * 4) - (wrong_count * 1) 
        final_score = max(0, calculated_marks)
        
        if not st.session_state.result_saved:
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
            st.session_state.result_saved = True
        
        # 🔥 PURE LOCAL CSS/HTML FIREWORKS (Streamlit Cloud proof!)
        import streamlit.components.v1 as html_components
        html_components.html("""
        <style>
            @keyframes explode {
                0% { transform: translate(-50%, -50%) scale(0); opacity: 1; }
                100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
            }
            .firework-container {
                position: relative;
                width: 100%;
                height: 150px;
                background: #000;
                border-radius: 10px;
                overflow: hidden;
                text-align: center;
                padding-top: 20px;
            }
            .main-title {
                color: #2e7d32;
                font-family: sans-serif;
                font-size: 28px;
                margin: 0;
                position: relative;
                z-index: 10;
            }
            .sub-title {
                color: #a5d6a7;
                font-family: sans-serif;
                margin: 5px 0 0 0;
                position: relative;
                z-index: 10;
            }
            .fw {
                position: absolute;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                opacity: 0;
            }
            /* Firework 1 */
            .fw1 {
                left: 20%; top: 50%; background: radial-gradient(circle, #ff1744 20%, transparent 60%);
                box-shadow: 0 0 30px 20px #ff1744, -40px -40px 0 5px #ffea00, 40px -40px 0 5px #00e676, -40px 40px 0 5px #00e5ff, 40px 40px 0 5px #d500f9;
                animation: explode 2s infinite ease-out;
            }
            /* Firework 2 */
            .fw2 {
                left: 80%; top: 40%; background: radial-gradient(circle, #00e5ff 20%, transparent 60%);
                box-shadow: 0 0 30px 20px #00e5ff, -30px -50px 0 5px #ff1744, 50px -20px 0 5px #ffea00, -50px 30px 0 5px #00e676, 30px 50px 0 5px #ff00ff;
                animation: explode 2.5s infinite ease-out 0.5s;
            }
            /* Firework 3 */
            .fw3 {
                left: 50%; top: 70%; background: radial-gradient(circle, #ffea00 20%, transparent 60%);
                box-shadow: 0 0 30px 20px #ffea00, -50px -10px 0 4px #00e5ff, 20px -50px 0 4px #ff1744, -20px 50px 0 4px #00e676, 50px 20px 0 4px #d500f9;
                animation: explode 1.8s infinite ease-out 0.2s;
            }
        </style>
        
        <div class="firework-container">
            <h1 class="main-title">🎆 CONGRATULATIONS 🎆</h1>
            <h3 class="sub-title">Test Completed Successfully!</h3>
            <div class="fw fw1"></div>
            <div class="fw fw2"></div>
            <div class="fw fw3"></div>
        </div>
        """, height=170)
        
        st.success("Test Logged Safely in Central Registry Ledger Databases.")
        st.write("---")
        
        # Result Dashboard
        st.markdown("### 🏆 Exam Metric Performance Summary")
        st.metric(label="Calculated Scale Output Grade", value=f"{final_score} / {total_marks}")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Items", total_q)
        col2.metric("Correct ✔️", correct_count)
        col3.metric("Wrong ❌", wrong_count)
        col4.metric("Unanswered ⚪", unanswered_count)  
    else:
        st.error("Error generating score logs.")

    if st.button("Return Main Portal Home", type="secondary", use_container_width=True):
        st.session_state.page = "Main Menu"
        st.session_state.active_quiz = None
        st.session_state.quiz_answers = {}
        st.session_state.logged_in_user = None
        st.session_state.result_saved = False
        if "start_time" in st.session_state:
            del st.session_state.start_time
        st.rerun()