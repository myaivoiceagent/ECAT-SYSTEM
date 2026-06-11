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
if "selected_tracks" not in st.session_state:
    st.session_state.selected_tracks = []

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

def get_stream_name(selected_subjects_list):
    if not selected_subjects_list:
        return "General Test"
    
    # Saare selected subjects ko lowercase mein check karne ke liye string banaya
    subs_str = "".join([str(s).lower() for s in selected_subjects_list])
    
    if "math" in subs_str and "physics" in subs_str and ("computer" in subs_str or "cs" in subs_str or "ics" in subs_str):
        return "ICS - Physics"
    elif "math" in subs_str and "physics" in subs_str and "chemistry" in subs_str:
        return "FSc Pre. Engineering"
    elif "math" in subs_str and "statistics" in subs_str and ("computer" in subs_str or "cs" in subs_str):
        return "ICS - Statistics"
    elif "biology" in subs_str and "physics" in subs_str and "chemistry" in subs_str:
        return "FSc Pre Medical"
    elif "math" in subs_str and "statistics" in subs_str and "physics" in subs_str:
        return "General Science"
        
    return "Custom Stream"

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
            h_id, h_name, h_email, h_pass, h_time, h_act = st.columns([1.2, 2, 2.5, 1.8, 2.2, 1.3])
            with h_id: st.markdown("**ID**")
            with h_name: st.markdown("**Name**")
            with h_email: st.markdown("**Email**")
            with h_pass: st.markdown("**Password**")
            with h_time: st.markdown("**Last Login 🕒**")
            with h_act: st.markdown("**Action**")
            st.markdown("<hr style='margin:2px 0px 8px 0px;'>", unsafe_allow_html=True)

            for idx, u in enumerate(users):
                col1, col2, col3, col4, col5, col6 = st.columns([1.2, 2, 2.5, 1.8, 2.2, 1.3])
                
                u_id = u.get("User ID", "N/A")
                if "function uuid4" in str(u_id):
                    u_id = f"USR-{idx+1:03d}"

                with col1: st.text(u_id)
                with col2: st.text(u.get("User Name", "N/A"))
                with col3: st.text(u.get("Email", "N/A"))
                with col4: st.text(u.get("Password", "N/A"))
                with col5: st.text(u.get("Last Login", "Not Logged In"))
                with col6:
                    if st.button("❌ Remove", key=f"del_usr_final_{idx}", use_container_width=True):
                        target_email = u.get("Email")
                        target_name = u.get("User Name")
                        
                        new_users_list = [usr for usr in users if usr.get("Email") != target_email]
                        admin_save_json("Login.json", new_users_list)
                        
                        results = admin_load_json("Result.json")
                        new_results_list = [r for r in results if r.get("User Email") != target_email]
                        admin_save_json("Result.json", new_results_list)
                        
                        st.success(f"🎉 {target_name} ka account aur saara data delete ho gaya!")
                        st.rerun()
                st.write("") 
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
                
                subj = r.get("Selected Subject", r.get("Subject", "Not Selected"))
                
                u_id = r.get("USER ID", r.get("User ID", "N/A"))
                if "function uuid4" in str(u_id):
                    u_id = "USR-NEW"
                
                flattened_results.append({
                    "User ID": u_id,
                    "Student Name": r.get("User Name", "N/A"),
                    "Email Address": r.get("User Email", "N/A"),
                    "Attempted Subject 📚": subj,  
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
                st.success("Database cleared!")
                st.rerun()
        else:
            st.info("No candidates have evaluated or logged exams yet.")

# STUDENT AUTHENTICATION
elif st.session_state.page == "Student Auth Menu":
    st.subheader("🔑 Student Registration & Login")
    
    def get_pakistan_time():
        from datetime import datetime, timedelta
        pkt_time = datetime.utcnow() + timedelta(hours=5)
        return pkt_time.strftime("%I:%M %p (%d-%b)")

    mode = st.radio("Action:", ["User Login", "Create Account", "Forget Password"])
    
    import json
    import os

    def force_load_login():
        if not os.path.exists("Login.json"):
            return []
        try:
            with open("Login.json", "r") as f:
                content = f.read().strip()
                return json.loads(content) if content else []
        except Exception:
            return []

    def force_save_login(data):
        with open("Login.json", "w") as f:
            json.dump(data, f, indent=4)

    # ------------------------------------------------------------------------
    # 🔓 USER LOGIN LOGIC (UPDATED WITH FOOLPROOF MATCH)
    # ------------------------------------------------------------------------
    if mode == "User Login":
        login_input = st.text_input("Email ya Username Enter Karein:").strip().lower()
        login_pass = st.text_input("Password:", type="password").strip()
        
        if st.button("Log In"):
            users = force_load_login()  
            found_user = None
            
            for u in users:
                db_email = str(u.get("Email", "")).strip().lower()
                db_user = str(u.get("User Name", "")).strip().lower()
                db_pass = str(u.get("Password", "")).strip()
                
                # Username ya email dono mein se koi aik b match ho jaye to chal jaye
                if (login_input == db_email or login_input == db_user) and login_pass == db_pass:
                    found_user = u
                    break
                    
            if found_user:
                current_time = get_pakistan_time()
                st.session_state["login_time"] = current_time
                found_user["Last Login"] = current_time  
                force_save_login(users)
                
                st.session_state.logged_in_user = found_user  
                st.session_state.page = "Main Menu"
                st.success("Login Successful! 🎉")
                st.rerun()
            else:
                st.error("❌ Invalid Credentials. Email/Username ya Password ghalt hai!")

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
                new_user = {
                    "User ID": str(uuid.uuid4())[:8],
                    "User Name": reg_name,
                    "Email": reg_email,
                    "Password": reg_pass,
                    "Last Login": "Not Logged In Yet"
                }
                users.append(new_user)
                force_save_login(users) 
                st.success("🎉 Account Created! Tab pe login karein.")
                st.rerun()

    elif mode == "Forget Password":
        st.write("---")
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
                    st.info(f"Your Password is: **{found_user.get('Password')}**")
                else:
                    st.error("❌ Profile nahi mili.")
            else:
                st.warning("⚠️ Dono fields fill karein.")

    st.write("---")
    if st.button("Back"):
        st.session_state.page = "Main Menu"
        st.rerun()

# ECAT TEST LOGIN (UPDATED TO ALLOW SINGLE MATCH INTERFACE AS WELL)
elif st.session_state.page == "ECAT Test Login":
    st.subheader("✍️ Verification Prior to ECAT")
    test_input = st.text_input("Email ya Username Enter Karein:").strip().lower()
    test_pass = st.text_input("Password:", type="password").strip()
    
    if st.button("Verify Identity"):
        users = load_json("Login.json")
        matched = None
        for u in users:
            db_email = str(u.get("Email", "")).strip().lower()
            db_user = str(u.get("User Name", "")).strip().lower()
            if (test_input == db_email or test_input == db_user) and u["Password"] == test_pass:
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
    st.subheader("📝 Subject Selection Criteria")
    quizz_data = load_json("Quizz.json")
    available_subjects = [s["Section"] for s in quizz_data if s["Section"].lower() != "english"]
    
    if len(available_subjects) < 3:
        st.error("Database needs at least 3 subjects alternative to English.")
    else:
        chosen_tracks = st.multiselect("Pick exactly 3 branches:", available_subjects)
        
        if chosen_tracks:
            full_user_selection = chosen_tracks + ["English"]
            st.session_state.selected_tracks = full_user_selection # Save securely to session state
            user_stream = get_stream_name(full_user_selection)
            st.info(f"📚 **Your Stream Group:** {user_stream}")

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

# LIVE EXAMINATION
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
        total_questions_count = len(questions)
        solved_count = len(st.session_state.saved_questions)
        skipped_count = len(st.session_state.skipped_questions)
        remaining_count = total_questions_count - (solved_count + skipped_count)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Items 📋", total_questions_count)
        c2.metric("Saved/Locked ✅", solved_count)
        c3.metric("Skipped Items 🟡", skipped_count)
        c4.metric("Remaining ⏳", remaining_count)
        st.write("---")

        current_idx = st.session_state.current_q_index
        q = questions[current_idx]
        display_no = current_idx + 1

        st.markdown(f"#### **Question {display_no} of {total_questions_count}**")
        
        if current_idx in st.session_state.saved_questions:
            st.warning("🔒 This question has been locked.")
            st.write(f"**{q['Question']}**")
            saved_ans = st.session_state.quiz_answers.get(display_no, "A")
            st.info(f"Your Locked Response: Option {saved_ans}. {q['Options'][saved_ans]}")
        else:
            if current_idx in st.session_state.skipped_questions:
                st.warning("⚠️ You skipped this question earlier.")

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
                        st.error("Please choose an answer.")
            
            with col_actions[1]:
                if st.button("🟡 Skip Question", use_container_width=True):
                    st.session_state.skipped_questions.add(current_idx)
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

        st.write("---")
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

# ------------------------------------------------------------------------
# GRADE EVALUATION PROCESSING (COMPLETED WITH STATE PERSISTENCE)
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
            
            from datetime import datetime, timedelta
            pkt_now = datetime.utcnow() + timedelta(hours=5)
            current_login = pkt_now.strftime("%I:%M %p (%d-%b)")
            
            # Fetch safely from session state
            if "selected_tracks" in st.session_state and st.session_state.selected_tracks:
                detected_stream = get_stream_name(st.session_state.selected_tracks)
            else:
                detected_stream = "General Test"
                
            results_db.append({
                "USER ID": student.get("User ID", "N/A"),
                "User Name": student.get("User Name", "N/A"),
                "User Email": student.get("Email", "N/A"),
                "Login Time": current_login,
                "Selected Subject": detected_stream,  
                "User Result": [{
                    "Total Questions": total_q,
                    "Total Marks": total_marks,
                    "Obtained Marks": final_score
                }]
            })
            save_json("Result.json", results_db)
            st.session_state.result_saved = True

        # Show final report card to user
        st.success("Test Submitted Successfully! 🎉")
        st.write(f"📝 **Total Questions:** {total_q}")
        st.write(f"✅ **Correct Answers:** {correct_count}")
        st.write(f"❌ **Wrong Answers:** {wrong_count}")
        st.write(f"🟡 **Unanswered:** {unanswered_count}")
        st.info(f"🏆 **Your Score:** {final_score} / {total_marks}")
        
        if st.button("Return to Main Menu", type="primary"):
            st.session_state.page = "Main Menu"
            st.session_state.active_quiz = None
            st.session_state.quiz_answers = {}
            st.session_state.result_saved = False
            st.rerun()