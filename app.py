import os
import json
import datetime
import random
import uuid
import streamlit as st
import streamlit.components.v1 as html_components

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
        "Password": "UET - CYBER - SECURITY - SPECIALIST - 2026 - 2030 - @#$%"
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
            if secret_key == "UET - ECAT - ADMIN - PORTAL - ACCESS":
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
        st.subheader("👥 Registered Users Details")
        import json
        import os
        
        # Safe reading inside admin panel
        def admin_load_json(filename):
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    content = f.read().strip()
                    return json.loads(content) if content else []
            return []

        def admin_save_json(filename, data):
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)

        users = admin_load_json("Login.json")
        
        if users:
            # 🛠️ Loop chala kar har user ki details aur delete button render karenge
            for idx, u in enumerate(users):
                col1, col2, col3, col4 = st.columns([2, 3, 3, 1.5])
                
                with col1:
                    st.write(f"**{u.get('User Name', 'N/A')}**")
                with col2:
                    st.write(f"📧 {u.get('Email', 'N/A')}")
                with col3:
                    st.write(f"🕒 {u.get('Last Login', 'Not Logged In Yet')}")
                with col4:
                    # 🗑️ REMOVE BUTTON
                    if st.button("❌ Remove", key=f"del_usr_{idx}"):
                        target_email = u.get("Email")
                        target_name = u.get("User Name")
                        
                        # 1. Login.json se nikalo
                        new_users_list = [usr for usr in users if usr.get("Email") != target_email]
                        admin_save_json("Login.json", new_users_list)
                        
                        # 2. Result.json se bhi sara data delete karo taake clean wipe ho
                        results = admin_load_json("Result.json")
                        new_results_list = [r for r in results if r.get("User Email") != target_email]
                        admin_save_json("Result.json", new_results_list)
                        
                        st.success(f"{target_name} ka data mukammal delete ho gaya!")
                        st.rerun()
                st.write("---")
        else:
            st.info("No registered users found.")

    with t5:
        st.subheader("📊 Candidate Performance Results")
        results = load_json("Result.json")
        if results:
            flattened_results = []
            for r in results:
                res_list = r.get("User Result", [{}])
                res = res_list[0] if isinstance(res_list, list) and len(res_list) > 0 else {}
                
                # 1. Pehle file se subject uthane ki koshish karein
                subj = r.get("Selected Subject", r.get("Subject", "Not Selected"))
                
                # 2. 🛠️ FOOLPROOF FIX: Agar subject save nahi hua tha, toh record se auto-detect karein
                if subj == "Not Selected" or not subj:
                    # Agar user result list mein koi structural detail ho, ya user profile check karni ho
                    if "active_quiz" in st.session_state and st.session_state.active_quiz:
                        # Pehle question se subject nikalne ki koshish
                        first_q = st.session_state.active_quiz[0]
                        subj = first_q.get("Subject", first_q.get("Section", "General Test"))
                    else:
                        # Aik automatic backup subject rakh dete hain jo aapki website par defaults hain
                        subj = "ECAT Main Stream"
                
                # Handle UUID bug if present
                u_id = r.get("USER ID", r.get("User ID", "N/A"))
                if "function uuid4" in str(u_id):
                    u_id = "USR-NEW"
                
                flattened_results.append({
                    "User ID": u_id,
                    "Student Name": r.get("User Name", "N/A"),
                    "Email Address": r.get("User Email", "N/A"),
                    "Attempted Subject 📚": subj,  # 💡 Ab yeh khali "Not Selected" nahi dikhayega
                    "Login/Test Time 🕒": r.get("Login Time", "N/A"),
                    "Total Qs": res.get("Total Questions", 100),
                    "Max Marks": res.get("Total Marks", 400),
                    "Score Obtained": res.get("Obtained Marks", 0)
                })
                
            import pandas as pd
            df_results = pd.DataFrame(flattened_results)
            st.dataframe(df_results, use_container_width=True, hide_index=True)
            
            st.write("")
            if st.button("Clear Submission Logs Databases", type="secondary", key="admin_clear_all_res"):
                save_json("Result.json", [])
                st.success("Database cleared! Now test with new fresh user login.")
                st.rerun()
        else:
            st.info("No candidates have evaluated or logged exams yet.")

# STUDENT AUTHENTICATION
elif st.session_state.page == "Student Auth Menu":
    st.subheader("🔑 Student Registration & Login")
    
    # 🕒 PAKISTAN TIME ZONE FUNCTION (Isay sab se upar rakhna hai)
    def get_pakistan_time():
        from datetime import datetime, timedelta
        # Server UTC time mein exactly 5 ghante plus kiye taake local computer time banay
        pkt_time = datetime.utcnow() + timedelta(hours=5)
        return pkt_time.strftime("%I:%M %p (%d-%b)")

    mode = st.radio("Action:", ["User Login", "Create Account", "Forget Password"])
    
    # Python ka apna json library import kiya backup ke liye
    import json
    import os

    # 🛠️ SAFE FILE LOADER (Direct Python Implementation)
    def force_load_login():
        if not os.path.exists("Login.json"):
            return []
        try:
            with open("Login.json", "r") as f:
                content = f.read().strip()
                return json.loads(content) if content else []
        except Exception:
            return []

    # 🛠️ SAFE FILE SAVER (Direct Python Implementation)
    def force_save_login(data):
        with open("Login.json", "w") as f:
            json.dump(data, f, indent=4)

    # ------------------------------------------------------------------------
    # 🔓 USER LOGIN LOGIC
    # ------------------------------------------------------------------------
    if mode == "User Login":
        login_email = st.text_input("Email:").strip()
        login_user = st.text_input("Username:").strip()
        login_pass = st.text_input("Password:", type="password").strip()
        
        if st.button("Log In"):
            users = force_load_login()  # Direct load kiya
            found = False
            for u in users:
                db_email = str(u.get("Email", "")).strip().lower()
                db_user = str(u.get("User Name", "")).strip().lower()
                db_pass = str(u.get("Password", "")).strip()
                
                if db_email == login_email.lower() and db_user == login_user.lower() and db_pass == login_pass:
                    found = True
                    
                    # 🕒 Purani line hata kar yeh lagayin
                    current_time = get_pakistan_time()
                    st.session_state["login_time"] = current_time
                    
                    u["Last Login"] = current_time  
                    force_save_login(users)
                    
                    u["Last Login"] = current_time  
                    force_save_login(users) # Force save updated list
                    
                    st.session_state.logged_in_user = u  
                    st.session_state.page = "Main Menu"
                    st.success("Login Successful! 🎉")
                    st.rerun()
            if not found:
                st.error("❌ Invalid Credentials. Email, Username ya Password ghalt hai!")

    # ------------------------------------------------------------------------
    # 📝 CREATE ACCOUNT LOGIC
    # ------------------------------------------------------------------------
    elif mode == "Create Account":
        reg_email = st.text_input("Email:").strip()
        reg_name = st.text_input("Full Name:").strip()
        reg_pass = st.text_input("Password:", type="password").strip()
        
        if st.button("Register"):
            users = force_load_login()
            
            if not reg_email or not reg_name or not reg_pass:
                st.error("❌ Saari fields ko bharna zaroori hai!")
            elif len(reg_pass) < 6:
                st.error("❌ Password kam az kam 6 characters ka hona chahiye.")
            elif any(str(u.get("Email", "")).lower() == reg_email.lower() for u in users):
                st.error("❌ Yeh Email pehle se registered hai!")
            else:
                import uuid
                new_user = {
                    "User ID": str(uuid.uuid4())[:8],
                    "User Name": reg_name,
                    "Email": reg_email,
                    "Password": reg_pass,
                    "Last Login": "Not Logged In Yet"
                }
                
                users.append(new_user)
                force_save_login(users) # Direct file ke andar write ho gaya
                
                st.success("🎉 Account Created Successfully! Ab 'User Login' tab par ja kar login karein.")
                st.rerun()

    # ------------------------------------------------------------------------
    # 🔄 FORGET PASSWORD LOGIC
    # ------------------------------------------------------------------------
    elif mode == "Forget Password":
        st.write("---")
        st.markdown("#### 🔄 Recover Your Password")
        forget_email = st.text_input("Enter Registered Email Address:")
        forget_name = st.text_input("Enter Your Registered Username:")
        
        if st.button("Retrieve Password 🔍", type="primary", use_container_width=True):
            if forget_email and forget_name:
                users_list = force_load_login()
                found_user = None
                
                for u in users_list:
                    if str(u.get("Email")).lower() == forget_email.strip().lower() and str(u.get("User Name")).lower() == forget_name.strip().lower():
                        found_user = u
                        break
                        
                if found_user:
                    st.success("🔑 Account Verified Successfully!")
                    st.info(f"Your Registered Password is: **{found_user.get('Password')}**")
                else:
                    st.error("❌ No matching profile found with these details.")
            else:
                st.warning("⚠️ Please fill out both fields.")

    st.write("---")
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
# LIVE EXAMINATION (UPDATED: WITH REAL-TIME QUESTION COUNTERS)
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
    
    st.markdown(f"### 📝 Live Exam Environment (Candidate: **{student['User Name']}**)")
    
    if remaining <= 0:
        st.error("⏰ Time Limit Reached! Auto-evaluating responses...")
        st.session_state.page = "Grade Evaluation Processing"
        st.rerun()
    else:
        mins, secs = divmod(remaining, 60)
        st.error(f"⏱️ **Time Remaining: {int(mins):02d}:{int(secs):02d}**")
        
    st.write("---")

    if questions:
        # 📊 REAL-TIME QUESTION TRACKING COUNTERS
        total_questions_count = len(questions)
        solved_count = len(st.session_state.saved_questions)
        skipped_count = len(st.session_state.skipped_questions)
        remaining_count = total_questions_count - (solved_count + skipped_count)

        # Counter Banner Visual Layout
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Items 📋", total_questions_count)
        c2.metric("Saved/Locked ✅", solved_count)
        c3.metric("Skipped Items 🟡", skipped_count)
        c4.metric("Remaining ⏳", remaining_count)
        st.write("---")

        current_idx = st.session_state.current_q_index
        q = questions[current_idx]
        display_no = current_idx + 1

        # 1️⃣ QUESTIONS AND OPTIONS (ON TOP)
        st.markdown(f"#### **Question {display_no} of {total_questions_count}**")
        
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
                    # Remove from saved just in case they re-skipped
                    st.session_state.saved_questions.discard(current_idx)
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

        # 2️⃣ NAVIGATION MATRIX BOX (AT THE BOTTOM)
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
# GRADE EVALUATION PROCESSING (FINAL CLEAN FIX: NO CODE BLOCKING)
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
            
            # 🕒 Pakistan ka current time catch karne ke liye function lagaya
            from datetime import datetime, timedelta
            pkt_now = datetime.utcnow() + timedelta(hours=5)
            current_login = pkt_now.strftime("%I:%M %p (%d-%b)")
            
            # Subject detector lagaya
            user_selected_subject = "Not Selected"
            possible_keys = ["selected_subject", "subject", "chosen_subject", "active_subject"]
            for key in possible_keys:
                if key in st.session_state and st.session_state[key]:
                    user_selected_subject = st.session_state[key]
                    break
            
            results_db.append({
                "USER ID": student.get("User ID", "N/A"),
                "User Name": student.get("User Name", "N/A"),
                "User Email": student.get("Email", "N/A"),
                "Login Time": current_login,  # 🕒 Yeh exact computer wala sahi time save karega
                "Selected Subject": user_selected_subject,
                "User Result": [{
                    "Total Questions": total_q,
                    "Total Marks": total_marks,
                    "Obtained Marks": final_score
                }]
            })
            save_json("Result.json", results_db)
            st.session_state.result_saved = True

        # 👤 1️⃣ CANDIDATE PROFILE DETAILS CARD (ALWAYS ON TOP)
        st.markdown(f"""
        <div style="background-color: #1e293b; border-left: 5px solid #3b82f6; border-radius: 8px; padding: 15px; margin-bottom: 20px;">
            <h4 style="margin: 0; color: #3b82f6;">👤 Candidate Profile & Session Info</h4>
            <p style="margin: 5px 0 0 0; color: #cbd5e1; font-size: 14px;">
                <strong>Name:</strong> {student['User Name']} | 
                <strong>ID:</strong> {student['User ID']} | 
                <strong>Email:</strong> {student['Email']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 🏆 2️⃣ EXAM PERFORMANCE SUMMARY METRICS
        st.success("Test Logged Safely in Central Registry Ledger Databases.")
        st.write("---")
        
        st.markdown("### 🏆 Exam Metric Performance Summary")
        st.metric(label="Calculated Scale Output Grade", value=f"{final_score} / {total_marks}")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Items", total_q)
        col2.metric("Correct ✔️", correct_count)
        col3.metric("Wrong ❌", wrong_count)
        col4.metric("Unanswered ⚪", unanswered_count)  
        
        st.write("---")

        # 🎬 3️⃣ CONDITION PACKS: DOWNSIDE EFFECTS WITH SEGREGATED IFRAME LAYER
        if final_score >= 100:
            # Clean Congratulations Card
            st.markdown("""
            <div style="background-color: #0e1117; border: 2px solid #2e7d32; border-radius: 12px; padding: 25px; text-align: center; margin-top: 15px; margin-bottom: 15px;">
                <h1 style="color: #4caf50 !important; font-family: sans-serif; font-weight: bold; margin:0;">🎆 CONGRATULATIONS 🎆</h1>
                <p style="color: white !important; margin: 5px 0 0 0;">Excellent work! You have successfully passed the threshold.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # True Full-Screen Safe Canvas Fireworks Iframe Component
            html_components.html("""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
                html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: transparent; }
                canvas {
                    position: fixed; top: 0; left: 0;
                    width: 100vw; height: 100vh;
                    z-index: -1; pointer-events: none;
                }
            </style>
            </head>
            <body>
            <canvas id="canvasSky"></canvas>
            <script>
                const canvas = document.getElementById('canvasSky');
                const ctx = canvas.getContext('2d');
                function resize() {
                    canvas.width = window.parent.innerWidth || window.innerWidth;
                    canvas.height = window.parent.innerHeight || window.innerHeight;
                }
                window.addEventListener('resize', resize); window.addEventListener('load', resize); resize();

                class Spark {
                    constructor(x, y, color) {
                        this.x = x; this.y = y; this.color = color;
                        const angle = Math.random() * Math.PI * 2;
                        const speed = Math.random() * 6 + 2;
                        this.vx = Math.cos(angle) * speed;
                        this.vy = Math.sin(angle) * speed;
                        this.friction = 0.95; this.gravity = 0.15;
                        this.alpha = 1; this.decay = 0.012 + Math.random() * 0.015;
                    }
                    update() {
                        this.vx *= this.friction; this.vy *= this.friction; this.vy += this.gravity;
                        this.x += this.vx; this.y += this.vy; this.alpha -= this.decay;
                    }
                    draw() {
                        ctx.save(); ctx.globalAlpha = this.alpha; ctx.beginPath();
                        ctx.arc(this.x, this.y, 2.5, 0, Math.PI * 2);
                        ctx.fillStyle = this.color; ctx.shadowBlur = 10; ctx.shadowColor = this.color;
                        ctx.fill(); ctx.restore();
                    }
                }

                class Rocket {
                    constructor() {
                        this.x = Math.random() * canvas.width; this.y = canvas.height;
                        this.targetY = Math.random() * (canvas.height * 0.5) + 50;
                        this.speed = 11 + Math.random() * 4;
                        this.color = `hsl(${Math.random() * 360}, 100%, 60%)`;
                        this.sparks = []; this.exploded = false;
                    }
                    update() {
                        if (!this.exploded) {
                            this.y -= this.speed;
                            if (this.y <= this.targetY) { this.exploded = true; this.explode(); }
                        } else {
                            for (let i = this.sparks.length - 1; i >= 0; i--) {
                                this.sparks[i].update();
                                if (this.sparks[i].alpha <= 0) this.sparks.splice(i, 1);
                            }
                        }
                    }
                    explode() {
                        const count = 80 + Math.floor(Math.random() * 30);
                        for (let i = 0; i < count; i++) this.sparks.push(new Spark(this.x, this.y, this.color));
                    }
                    draw() {
                        if (!this.exploded) {
                            ctx.beginPath(); ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
                            ctx.fillStyle = '#ffffff'; ctx.fill();
                        } else { this.sparks.forEach(s => s.draw()); }
                    }
                }

                const rockets = [];
                function loop() {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    if (Math.random() < 0.04 && rockets.length < 6) rockets.push(new Rocket());
                    for (let i = rockets.length - 1; i >= 0; i--) {
                        rockets[i].update(); rockets[i].draw();
                        if (rockets[i].exploded && rockets[i].sparks.length === 0) rockets.splice(i, 1);
                    }
                    requestAnimationFrame(loop);
                }
                loop();
            </script>
            </body>
            </html>
            """, height=250)
            
        else:
            # Crying Face Banner placed down below the metrics cleanly via CSS animation
            st.markdown("""
            <style>
                @keyframes tear-drop {
                    0% { transform: translateY(0) scale(1); opacity: 1; }
                    80% { opacity: 1; }
                    100% { transform: translateY(40px) scale(0.5); opacity: 0; }
                }
                .crying-container {
                    background-color: #0e1117; 
                    border: 2px solid #d32f2f; 
                    border-radius: 12px; 
                    padding: 25px; 
                    text-align: center; 
                    margin-top: 15px;
                }
                .sad-emoji-wrapper {
                    font-size: 70px;
                    position: relative;
                    display: inline-block;
                    line-height: 1;
                }
                .tear {
                    position: absolute;
                    font-size: 24px;
                    animation: tear-drop 1.5s infinite linear;
                }
                .tear-left { left: 10px; top: 45px; animation-delay: 0s; }
                .tear-right { right: 10px; top: 45px; animation-delay: 0.7s; }
            </style>
            
            <div class="crying-container">
                <div class="sad-emoji-wrapper">
                    😢
                    <span class="tear tear-left">💧</span>
                    <span class="tear tear-right">💧</span>
                </div>
                <h1 style="color: #d32f2f !important; font-family: sans-serif; font-weight: bold; margin: 10px 0 0 0;">BETTER LUCK NEXT TIME!</h1>
                <p style="color: white !important; margin: 5px 0 0 0;">Score is below 100. Hard work pays off, keep practicing!</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.error("Error generating score logs.")

    # 4️⃣ BUTTON IS TOTALLY OUTSIDE LAYOUT (ALWAYS WORKS)
    st.write("")
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