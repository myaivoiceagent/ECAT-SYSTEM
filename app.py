import os
import json
import datetime
import random
import uuid
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
if "saved_questions" not in st.session_state:
    st.session_state.saved_questions = set()  # Tracks locked questions
if "skipped_questions" not in st.session_state:
    st.session_state.skipped_questions = set()  # Tracks skipped questions
if "current_q_index" not in st.session_state:
    st.session_state.current_q_index = 0
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "result_saved" not in st.session_state:
    st.session_state.result_saved = False

def init_json_file(filename):
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        with open(filename, "w") as f:
            json.dump([], f, indent=4)

init_json_file("Admin.json")
init_json_file("Login.json")
init_json_file("Quizz.json")
init_json_file("Result.json")

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
                    st.session_state.saved_questions = set()
                    st.session_state.skipped_questions = set()
                    st.session_state.current_q_index = 0
                    st.session_state.quiz_submitted = False
                    st.session_state.start_time = datetime.datetime.now().timestamp()
                    st.session_state.page = "Live Examination"
                    st.rerun()

# ------------------------------------------------------------------------
# LIVE EXAMINATION (FIXED: QUESTIONS TOP, MATRIX BOTTOM)
# ------------------------------------------------------------------------
elif st.session_state.page == "Live Examination":
    student = st.session_state.logged_in_user
    questions = st.session_state.active_quiz
    
    if "start_time" not in st.session_state:
        st.session_state.start_time = datetime.datetime.now().timestamp()
        
    total_allowed_seconds = 100 * 60  
    current_time_stamp = datetime.datetime.now().timestamp()
    elapsed = int(current_time_stamp - st.session_state.start_time)
    remaining = max(0, total_allowed_seconds - elapsed)
    
    st.markdown(f"### 📝 Live Exam Branch (Candidate: **{student['User Name']}**)")
    
    if remaining <= 0:
        st.error("⏰ Time Limit Reached! Auto-evaluating responses...")
        st.session_state.page = "Grade Evaluation Processing"
        st.rerun()
    else:
        mins, secs = divmod(remaining, 60)
        st.error(f"⏱️ **Time Remaining: {int(mins):02d}:{int(secs):02d}**")
        
    st.write("---")

    if questions:
        current_idx = st.session_state.current_q_index
        q = questions[current_idx]
        display_no = current_idx + 1

        # 1️⃣ QUESTIONS AND OPTIONS (STAYS ON TOP)
        st.markdown(f"#### **Question {display_no} of {len(questions)}**")
        
        if current_idx in st.session_state.saved_questions:
            st.warning("🔒 This question has been locked and saved. You cannot modify it.")
            st.write(f"**{q['Question']}**")
            saved_ans = st.session_state.quiz_answers.get(display_no, "A")
            st.info(f"Your Locked Response: Option {saved_ans}. {q['Options'][saved_ans]}")
        else:
            if current_idx in st.session_state.skipped_questions:
                st.warning("⚠️ You skipped this question earlier. You can solve it now!")

            st.write(f"**{q['Question']}**")
            current_ans = st.session_state.quiz_answers.get(display_no, None)
            default_idx = ["A", "B", "C", "D"].index(current_ans) if current_ans in ["A", "B", "C", "D"] else None

            answer = st.radio(
                f"Select option for question {display_no}:", 
                ["A", "B", "C", "D"], 
                index=default_idx,
                format_func=lambda x: f"{x}. {q['Options'][x]}",
                key=f"live_q_{display_no}"
            )
            
            st.write("")
            col_actions = st.columns([2, 2, 2])
            
            with col_actions[0]:
                if st.button("💾 Save & Next", type="primary", use_container_width=True):
                    if answer is not None:
                        st.session_state.quiz_answers[display_no] = answer
                        st.session_state.saved_questions.add(current_idx)
                        st.session_state.skipped_questions.discard(current_idx)
                        
                        if current_idx < len(questions) - 1:
                            st.session_state.current_q_index += 1
                        st.rerun()
                    else:
                        st.error("Please choose an answer before locking or choose Skip.")
            
            with col_actions[1]:
                if st.button("🟡 Skip Question", use_container_width=True):
                    st.session_state.skipped_questions.add(current_idx)
                    if current_idx < len(questions) - 1:
                        st.session_state.current_q_index += 1
                    st.rerun()

        st.write("---")
        col_foot = st.columns([2, 2, 2])
        with col_foot[0]:
            if st.button("⬅️ Previous Question", disabled=(current_idx == 0), use_container_width=True):
                st.session_state.current_q_index -= 1
                st.rerun()
        with col_foot[1]:
            if st.button("Next Question ➡️", disabled=(current_idx == len(questions) - 1), use_container_width=True):
                st.session_state.current_q_index += 1
                st.rerun()
        with col_foot[2]:
            if st.button("🛑 Submit Entire Test", type="primary", use_container_width=True):
                st.session_state.page = "Grade Evaluation Processing"
                st.rerun()

        # 2️⃣ NAVIGATION MATRIX BOX (STAYS AT THE BOTTOM)
        st.write("")
        st.write("---")
        st.write("**📋 Exam Question Navigator Matrix:**")
        
        grid_cols = st.columns(10)
        for i in range(len(questions)):
            col_pos = i % 10
            btn_no = i + 1
            
            if i in st.session_state.saved_questions:
                btn_label = f"🔒{btn_no}"  
                disabled_state = True
            elif i in st.session_state.skipped_questions:
                btn_label = f"🟡{btn_no}"  
                disabled_state = False
            else:
                btn_label = f"📄{btn_no}"  
                disabled_state = False
                
            with grid_cols[col_pos]:
                if st.button(btn_label, key=f"nav_btn_{i}", disabled=disabled_state, use_container_width=True):
                    st.session_state.current_q_index = i
                    st.rerun()
    else:
        st.warning("No dynamic questions resolved.")

# ------------------------------------------------------------------------
# GRADE EVALUATION PROCESSING (COMPONENTS LAYER FIXED FOR FIREWORKS)
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
        
        # Safe Isolation using Native Component Framework
        import streamlit.components.v1 as html_components
        html_components.html("""
        <style>
            @keyframes trail {
                0% { top: 100%; opacity: 1; width: 4px; height: 30px; }
                40% { width: 4px; height: 4px; opacity: 1; }
                50% { top: var(--burst-top); opacity: 0; }
                100% { top: var(--burst-top); opacity: 0; }
            }
            @keyframes particle-explode {
                0% { transform: rotate(var(--angle)) translateY(0); opacity: 1; width: 4px; height: 4px; }
                80% { opacity: 1; }
                100% { transform: rotate(var(--angle)) translateY(var(--distance)); opacity: 0; width: 2px; height: 15px; }
            }
            body {
                background-color: #0e1117;
                margin: 0;
                overflow: hidden;
            }
            .fw-universe {
                position: relative;
                width: 100%;
                height: 180px;
            }
            .firework-shell {
                position: absolute;
                left: var(--left-x);
                width: 5px; height: 5px;
                animation: trail 3s infinite linear;
            }
            .burst-center {
                position: absolute;
                left: var(--left-x);
                top: var(--burst-top);
                animation: trail 3s infinite linear;
            }
            .spark-line {
                position: absolute;
                top: 0; left: 0;
                background: linear-gradient(to bottom, var(--color), transparent);
                transform-origin: top center;
                animation: particle-explode 3s infinite cubic-bezier(0.1, 0.8, 0.3, 1);
            }
            .fw-one { --left-x: 20%; --burst-top: 20%; animation-delay: 0s; }
            .fw-two { --left-x: 80%; --burst-top: 25%; animation-delay: 0.7s; }
            .fw-three { --left-x: 50%; --burst-top: 35%; animation-delay: 1.4s; }
            
            .banner-box {
                border: 2px solid #2e7d32;
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                font-family: sans-serif;
            }
        </style>
        
        <div class="banner-box">
            <h1 style="color: #4caf50; margin:0; font-size: 28px;">🎆 CONGRATULATIONS 🎆</h1>
            <p style="color: white; margin: 5px 0 0 0;">Your ECAT exam has been evaluated successfully.</p>
        </div>
        
        <div class="fw-universe">
            <div class="firework-shell fw-one" style="background: #ffeb3b;"></div>
            <div class="burst-center fw-one">
                <div class="spark-line" style="--angle: 0deg; --distance: 100px; --color: #ff1744;"></div>
                <div class="spark-line" style="--angle: 60deg; --distance: 90px; --color: #ffeb3b;"></div>
                <div class="spark-line" style="--angle: 120deg; --distance: 110px; --color: #2196f3;"></div>
                <div class="spark-line" style="--angle: 180deg; --distance: 100px; --color: #4caf50;"></div>
                <div class="spark-line" style="--angle: 240deg; --distance: 95px; --color: #e91e63;"></div>
                <div class="spark-line" style="--angle: 300deg; --distance: 105px; --color: #00e5ff;"></div>
            </div>

            <div class="firework-shell fw-two" style="background: #00e676;"></div>
            <div class="burst-center fw-two">
                <div class="spark-line" style="--angle: 30deg; --distance: 110px; --color: #00e5ff;"></div>
                <div class="spark-line" style="--angle: 90deg; --distance: 85px; --color: #ffea00;"></div>
                <div class="spark-line" style="--angle: 150deg; --distance: 120px; --color: #d500f9;"></div>
                <div class="spark-line" style="--angle: 210deg; --distance: 95px; --color: #ff1744;"></div>
                <div class="spark-line" style="--angle: 270deg; --distance: 100px; --color: #00e676;"></div>
                <div class="spark-line" style="--angle: 330deg; --distance: 115px; --color: #ffff00;"></div>
            </div>

            <div class="firework-shell fw-three" style="background: #e0f2f1;"></div>
            <div class="burst-center fw-three">
                <div class="spark-line" style="--angle: 45deg; --distance: 90px; --color: #e91e63;"></div>
                <div class="spark-line" style="--angle: 135deg; --distance: 110px; --color: #00e5ff;"></div>
                <div class="spark-line" style="--angle: 225deg; --distance: 100px; --color: #ffea00;"></div>
                <div class="spark-line" style="--angle: 315deg; --distance: 105px; --color: #76ff03;"></div>
            </div>
        </div>
        """, height=340)
        
        st.success("Test Logged Safely in Central Registry Ledger Databases.")
        st.write("---")
        
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
        st.session_state.saved_questions = set()
        st.session_state.skipped_questions = set()
        st.session_state.current_q_index = 0
        st.session_state.logged_in_user = None
        st.session_state.result_saved = False
        if "start_time" in st.session_state:
            del st.session_state.start_time
        st.rerun()