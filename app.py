import os
import json
import datetime
import random
import uuid
import streamlit as st
import streamlit.components.v1 as components

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

# --- INTERACTIVE FIREWORKS HTML/JS MATRIX GENERATOR ---
def play_fireworks():
    fireworks_js = """
    <canvas id="canvas" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:99999;pointer-events:none;"></canvas>
    <script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    let particles = [];
    class Particle {
        constructor(x, y, color) {
            this.x = x; this.y = y; this.color = color;
            this.radius = Math.random() * 3 + 1;
            this.velocity = { x: (Math.random() - 0.5) * 8, y: (Math.random() - 0.5) * 8 };
            this.alpha = 1;
        }
        draw() {
            ctx.save(); ctx.globalAlpha = this.alpha; ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
            ctx.fillStyle = this.color; ctx.fill(); ctx.restore();
        }
        update() {
            this.velocity.y += 0.05; this.x += this.velocity.x; this.y += this.velocity.y;
            this.alpha -= 0.012;
        }
    }
    function spawnFirework() {
        const x = Math.random() * canvas.width; const y = Math.random() * (canvas.height * 0.6);
        const colors = ['#FF1493', '#00FFFF', '#FFD700', '#FF4500', '#7FFF00', '#9400D3'];
        const color = colors[Math.floor(Math.random() * colors.length)];
        for (let i = 0; i < 40; i++) { particles.push(new Particle(x, y, color)); }
    }
    let interval = setInterval(spawnFirework, 400);
    setTimeout(() => { clearInterval(interval); }, 6000);
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach((p, i) => { if (p.alpha <= 0) { particles.splice(i, 1); } else { p.update(); p.draw(); } });
        requestAnimationFrame(animate);
    }
    animate();
    </script>
    """
    components.html(fireworks_js, height=0, width=0)

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
                    st.warning("Section already exists!")
                else:
                    quizz_data.append({"Section": new_sec, "Questions": []})
                    save_json("Quizz.json", quizz_data)
                    st.success("Section Added Successfully!")
                    
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
                st.success("Question Saved Successfully!")

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
        users = load_json("Login.json")
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
                u_id = u.get("User ID", f"USR-{idx+1:03d}")
                with col1: st.text(u_id)
                with col2: st.text(u.get("User Name", "N/A"))
                with col3: st.text(u.get("Email", "N/A"))
                with col4: st.text(u.get("Password", "N/A"))
                with col5: st.text(u.get("Last Login", "Not Logged In"))
                with col6:
                    if st.button("❌ Remove", key=f"del_usr_{idx}", use_container_width=True):
                        target_email = u.get("Email")
                        new_users = [usr for usr in users if usr.get("Email") != target_email]
                        save_json("Login.json", new_users)
                        
                        results = load_json("Result.json")
                        new_results = [r for r in results if r.get("User Email") != target_email]
                        save_json("Result.json", new_results)
                        
                        st.success("Account dropped! Clean system reset complete.")
                        st.rerun()
        else:
            st.info("No registered users found.")

    with t5:
        st.subheader("📊 Candidate Performance Results")
        results = load_json("Result.json")
        if results:
            flattened_results = []
            for r in results:
                res = r.get("User Result", [{}])[0]
                flattened_results.append({
                    "User ID": r.get("USER ID", "N/A"),
                    "Student Name": r.get("User Name", "N/A"),
                    "Email Address": r.get("User Email", "N/A"),
                    "Attempted Subject 📚": r.get("Selected Subject", "General Test"),
                    "Login/Test Time 🕒": r.get("Login Time", "N/A"),
                    "Total Qs": res.get("Total Questions", 100),
                    "Max Marks": res.get("Total Marks", 400),
                    "Score Obtained": res.get("Obtained Marks", 0)
                })
            import pandas as pd
            st.dataframe(pd.DataFrame(flattened_results), use_container_width=True, hide_index=True)

# STUDENT AUTHENTICATION
elif st.session_state.page == "Student Auth Menu":
    st.subheader("🔑 Student Registration & Login")
    mode = st.radio("Action:", ["User Login", "Create Account", "Forget Password"])
    
    def get_pakistan_time():
        from datetime import datetime, timedelta
        return (datetime.utcnow() + timedelta(hours=5)).strftime("%I:%M %p (%d-%b)")

    if mode == "User Login":
        login_input = st.text_input("Enter Email or Username:").strip().lower()
        login_pass = st.text_input("Password:", type="password").strip()
        if st.button("Log In"):
            users = load_json("Login.json")
            found = None
            for u in users:
                if (login_input == u.get("Email","").lower() or login_input == u.get("User Name","").lower()) and login_pass == u.get("Password",""):
                    found = u
                    break
            if found:
                found["Last Login"] = get_pakistan_time()
                save_json("Login.json", users)
                st.session_state.logged_in_user = found
                st.session_state.page = "Main Menu"
                st.rerun()
            else:
                st.error("❌ Invalid Credentials!")

    elif mode == "Create Account":
        reg_email = st.text_input("Email:").strip()
        reg_name = st.text_input("Full Name (Username):").strip()
        reg_pass = st.text_input("Password:", type="password").strip()
        if st.button("Register"):
            users = load_json("Login.json")
            if not reg_email or not reg_name or not reg_pass:
                st.error("❌ All fields are required!")
            elif any(u.get("Email","").lower() == reg_email.lower() for u in users):
                st.error("❌ This Email is already registered!")
            else:
                users.append({"User ID": str(uuid.uuid4())[:8], "User Name": reg_name, "Email": reg_email, "Password": reg_pass, "Last Login": "Not Logged In"})
                save_json("Login.json", users)
                st.success("🎉 Registered! Proceed to Login.")

    elif mode == "Forget Password":
        f_email = st.text_input("Enter Registered Email:")
        f_name = st.text_input("Enter Registered Username:")
        if st.button("Retrieve Password 🔍"):
            users = load_json("Login.json")
            match = next((u for u in users if u.get("Email","").lower() == f_email.lower() and u.get("User Name","").lower() == f_name.lower()), None)
            if match:
                st.info(f"Your Password is: **{match.get('Password')}**")
            else:
                st.error("Profile matching criteria not found.")

    if st.button("Back"):
        st.session_state.page = "Main Menu"
        st.rerun()

elif st.session_state.page == "ECAT Test Login":
    st.subheader("✍️ Identity Verification Prior to ECAT")
    t_input = st.text_input("Enter Registered Email or Username:").strip().lower()
    t_pass = st.text_input("Password:", type="password").strip()
    if st.button("Verify Identity"):
        users = load_json("Login.json")
        match = next((u for u in users if (t_input == u.get("Email","").lower() or t_input == u.get("User Name","").lower()) and u["Password"] == t_pass), None)
        if match:
            st.session_state.logged_in_user = match
            st.session_state.page = "ECAT Subject Selection"
            st.rerun()
        else:
            st.error("Verification failed.")
    if st.button("Back"):
        st.session_state.page = "Main Menu"
        st.rerun()

elif st.session_state.page == "ECAT Subject Selection":
    st.subheader("📝 Subject Selection Criteria")
    quizz_data = load_json("Quizz.json")
    available_subjects = [s["Section"] for s in quizz_data if s["Section"].lower() != "english"]
    
    if len(available_subjects) < 3:
        st.error("Database error: Needs at least 3 alternative branches plus English.")
    else:
        chosen_tracks = st.multiselect("Pick exactly 3 subject branches:", available_subjects)
        if chosen_tracks:
            st.session_state.selected_tracks = chosen_tracks + ["English"]
            st.info(f"📚 Stream Assignment: {get_stream_name(st.session_state.selected_tracks)}")

        if st.button("Assemble Test Matrix"):
            if len(chosen_tracks) != 3:
                st.error("Please select exactly 3 branches.")
            else:
                all_qs = []
                eng = next((s for s in quizz_data if s["Section"].lower() == "english"), None)
                if eng and eng["Questions"]:
                    all_qs.extend(random.sample(eng["Questions"], min(10, len(eng["Questions"]))))
                for track in chosen_tracks:
                    sec = next(s for s in quizz_data if s["Section"] == track)
                    if sec["Questions"]:
                        all_qs.extend(random.sample(sec["Questions"], min(30, len(sec["Questions"]))))
                
                if not all_qs:
                    st.error("Compilation matrix returned empty.")
                else:
                    random.shuffle(all_qs)
                    st.session_state.active_quiz = all_qs
                    st.session_state.quiz_answers = {}
                    st.session_state.saved_questions = set()
                    st.session_state.skipped_questions = set()
                    st.session_state.current_q_index = 0
                    st.session_state.start_time = datetime.datetime.now().timestamp()
                    st.session_state.page = "Live Examination"
                    st.rerun()

elif st.session_state.page == "Live Examination":
    student = st.session_state.logged_in_user
    questions = st.session_state.active_quiz
    
    elapsed = int(datetime.datetime.now().timestamp() - st.session_state.get("start_time", datetime.datetime.now().timestamp()))
    remaining = max(0, (100 * 60) - elapsed)
    
    st.markdown(f"### 📝 Live Exam (Candidate: **{student['User Name']}**)")
    if remaining <= 0:
        st.session_state.page = "Grade Evaluation Processing"
        st.rerun()
    else:
        mins, secs = divmod(remaining, 60)
        st.error(f"⏱️ **Time Remaining: {int(mins):02d}:{int(secs):02d}**")
        
    st.write("---")
    if questions:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Items", len(questions))
        c2.metric("Saved/Locked", len(st.session_state.saved_questions))
        c3.metric("Skipped", len(st.session_state.skipped_questions))
        c4.metric("Remaining", len(questions) - (len(st.session_state.saved_questions) + len(st.session_state.skipped_questions)))
        
        st.write("---")
        idx = st.session_state.current_q_index
        q = questions[idx]
        display_no = idx + 1
        
        st.markdown(f"#### **Question {display_no} of {len(questions)}**")
        if idx in st.session_state.saved_questions:
            st.warning("🔒 Question Locked.")
            st.write(f"**{q['Question']}**")
            ans = st.session_state.quiz_answers.get(display_no, "A")
            st.info(f"Your Choice: {ans}. {q['Options'][ans]}")
        else:
            st.write(f"**{q['Question']}**")
            cur_ans = st.session_state.quiz_answers.get(display_no, None)
            def_idx = ["A", "B", "C", "D"].index(cur_ans) if cur_ans in ["A", "B", "C", "D"] else None
            
            answer = st.radio("Options:", ["A", "B", "C", "D"], index=def_idx, format_func=lambda x: f"{x}. {q['Options'][x]}", key=f"q_{display_no}")
            
            act = st.columns(3)
            with act[0]:
                if st.button("💾 Save & Next", type="primary", use_container_width=True):
                    st.session_state.quiz_answers[display_no] = answer
                    st.session_state.saved_questions.add(idx)
                    st.session_state.skipped_questions.discard(idx)
                    if idx < len(questions) - 1: st.session_state.current_q_index += 1
                    st.rerun()
            with act[1]:
                if st.button("🟡 Skip Item", use_container_width=True):
                    st.session_state.skipped_questions.add(idx)
                    st.session_state.saved_questions.discard(idx)
                    if idx < len(questions) - 1: st.session_state.current_q_index += 1
                    st.rerun()

        st.write("---")
        foot = st.columns(3)
        with foot[0]:
            if st.button("⬅️ Previous", disabled=(idx == 0), use_container_width=True):
                st.session_state.current_q_index -= 1
                st.rerun()
        with foot[1]:
            if st.button("Next ➡️", disabled=(idx == len(questions) - 1), use_container_width=True):
                st.session_state.current_q_index += 1
                st.rerun()
        with foot[2]:
            if st.button("🛑 Submit Test", type="primary", use_container_width=True):
                st.session_state.page = "Grade Evaluation Processing"
                st.rerun()

        st.write("---")
        g_cols = st.columns(10)
        for i in range(len(questions)):
            pos = i % 10
            lbl = f"🔒{i+1}" if i in st.session_state.saved_questions else (f"🟡{i+1}" if i in st.session_state.skipped_questions else f"📄{i+1}")
            with g_cols[pos]:
                if st.button(lbl, key=f"nav_{i}", disabled=(i in st.session_state.saved_questions), use_container_width=True):
                    st.session_state.current_q_index = i
                    st.rerun()

# ------------------------------------------------------------------------
# GRADE EVALUATION PROCESSING (WITH DOWNSIDE FIREWORKS / CRYING ENGINE)
# ------------------------------------------------------------------------
elif st.session_state.page == "Grade Evaluation Processing":
    st.subheader("📊 Performance Metric Breakdown")
    questions = st.session_state.active_quiz
    answers = st.session_state.quiz_answers
    student = st.session_state.logged_in_user
    
    correct_count, wrong_count, unanswered_count = 0, 0, 0
    
    if questions:
        for idx, q in enumerate(questions, start=1):
            user_choice = answers.get(idx, None)
            if user_choice is None: unanswered_count += 1
            elif user_choice == q["Correct Answer"]: correct_count += 1
            else: wrong_count += 1
                
        total_q = len(questions)
        total_marks = total_q * 4
        calculated_marks = (correct_count * 4) - (wrong_count * 1) 
        final_score = max(0, calculated_marks)
        
        if not st.session_state.result_saved:
            results_db = load_json("Result.json")
            from datetime import datetime, timedelta
            current_login = (datetime.utcnow() + timedelta(hours=5)).strftime("%I:%M %p (%d-%b)")
            stream = get_stream_name(st.session_state.get("selected_tracks", []))
            
            results_db.append({
                "USER ID": student.get("User ID", "N/A"),
                "User Name": student.get("User Name", "N/A"),
                "User Email": student.get("Email", "N/A"),
                "Login Time": current_login,
                "Selected Subject": stream,  
                "User Result": [{"Total Questions": total_q, "Total Marks": total_marks, "Obtained Marks": final_score}]
            })
            save_json("Result.json", results_db)
            st.session_state.result_saved = True

        percentage = (final_score / total_marks) * 100 if total_marks > 0 else 0

        # REPORT CARD VISUALIZATION
        st.markdown(f"### 📋 **Official Report Card: {student['User Name']}**")
        st.write("---")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Items 📋", total_q)
        m2.metric("Correct ✅", correct_count, delta=f"+{correct_count*4} Marks")
        m3.metric("Wrong ❌", wrong_count, delta=f"-{wrong_count} Negative", delta_color="inverse")
        m4.metric("Unanswered 🟡", unanswered_count)
        
        st.write("---")
        st.subheader(f"🏆 Final Score Obtained: {final_score} / {total_marks}")
        st.progress(int(percentage))
        st.write("---")

        # 👇 DOWNSIDE DYNAMIC INTERFACE RULES AREA 👇
        st.markdown("### ✨ Performance Assessment Status")
        
        if final_score >= 100:
            st.success(f"💥 EXCELLENT METRIC PROFILE! You achieved {final_score} points! Visual Fireworks Triggered! 🎆🏆✨")
            play_fireworks()
        else:
            st.error(f"😭 UNACCEPTABLE BENCHMARK PROFILE... Score is {final_score} (Requires minimum 100).")
            st.markdown(
                """
                <div style="text-align: center; padding: 25px; border-radius: 10px; background-color: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b;">
                    <h1 style="font-size: 75px; margin: 0;">😭 😭 😭</h1>
                    <h2 style="color: #ff4b4b; margin-top: 10px;">Exam Metric Criteria Failure</h2>
                    <p style="font-size: 18px;">Please review your core concepts and try again. Practice makes perfect.</p>
                    <span style="font-size: 40px;">💔 🛌 📉 🚮</span>
                </div>
                """, 
                unsafe_allow_html=True
            )

        st.write("")
        if st.button("🚪 Return to Main Menu", type="primary", use_container_width=True):
            st.session_state.page = "Main Menu"
            st.session_state.active_quiz = None
            st.session_state.quiz_answers = {}
            st.session_state.result_saved = False
            st.rerun()