(async function init(){
  await loadSubjects();
  await loadStudents();
})().catch(console.error);

async function loadSubjects(){
  const data = await apiGet('/admin/subjects');
  const tbl = document.getElementById('subjects');
  tbl.innerHTML = `<tr><th>ID</th><th>Code</th><th>Name</th><th>Credits</th><th>TeacherID</th></tr>` + 
    data.map(s => `<tr><td>${s.id}</td><td>${s.code}</td><td>${s.name}</td><td>${s.credits}</td><td>${s.teacher_id ?? ''}</td></tr>`).join('');
}

async function loadStudents(){
  const data = await apiGet('/admin/students');
  const tbl = document.getElementById('students');
  tbl.innerHTML = `<tr><th>ID</th><th>Username</th><th>Full Name</th><th>Role</th></tr>` + 
    data.map(u => `<tr><td>${u.id}</td><td>${u.username}</td><td>${u.full_name ?? ''}</td><td>${u.role}</td></tr>`).join('');
}

async function createSubject(){
  const code = document.getElementById('sub_code').value.trim();
  const name = document.getElementById('sub_name').value.trim();
  const credits = parseInt(document.getElementById('sub_credits').value, 10) || 4;
  await apiPost(`/admin/subjects?code=${encodeURIComponent(code)}&name=${encodeURIComponent(name)}&credits=${credits}`, {});
  await loadSubjects();
}

async function createUser(){
  const qs = new URLSearchParams({
    username: document.getElementById('u_username').value,
    password: document.getElementById('u_password').value,
    role: document.getElementById('u_role').value,
    full_name: document.getElementById('u_full_name').value,
    email: document.getElementById('u_email').value,
    student_id: document.getElementById('u_student_id').value
  }).toString();
  const res = await apiPost(`/admin/create-user?${qs}`, {});
  await loadStudents();
}

async function assignTeacher(){
  const subject_id = parseInt(document.getElementById('as_subject_id').value,10);
  const teacher_user_id = parseInt(document.getElementById('as_teacher_user_id').value,10);
  await apiPost(`/admin/assign-teacher?subject_id=${subject_id}&teacher_user_id=${teacher_user_id}`, {});
  document.getElementById('as_msg').textContent = 'Assigned!';
}
