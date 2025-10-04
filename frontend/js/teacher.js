(async function init(){
  const s = await apiGet('/teacher/my-subject');
  const el = document.getElementById('subject');
  el.textContent = s?.code ? `${s.code} — ${s.name} (id=${s.id})` : 'No subject assigned';
})().catch(console.error);

async function submitMark(){
  const student_id = parseInt(document.getElementById('t_student_id').value, 10);
  const subject_id = parseInt(document.getElementById('t_subject_id').value, 10);
  const marks = parseInt(document.getElementById('t_marks').value, 10);
  try {
    await apiPost('/teacher/marks', { student_id, subject_id, marks });
    document.getElementById('t_msg').textContent = 'Saved!';
    document.getElementById('t_msg').className = 'notice';
  } catch(e){
    document.getElementById('t_msg').textContent = 'Error: ' + e.message;
    document.getElementById('t_msg').className = 'error';
  }
}
