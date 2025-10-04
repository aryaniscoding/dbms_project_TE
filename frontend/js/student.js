(async function init(){
  const prof = await apiGet('/student/me');
  document.getElementById('profile').innerHTML =
    `<div class="grid grid-3">
       <div><div class="tag">Name</div><div>${prof.name}</div></div>
       <div><div class="tag">Roll No</div><div>${prof.roll_no}</div></div>
       <div><div class="tag">Code</div><div>${prof.student_code}</div></div>
     </div>`;
  const res = await apiGet('/student/me/marks');
  document.getElementById('cgpa').textContent = res.cgpa.toFixed(2);
  const tbl = document.getElementById('marks');
  tbl.innerHTML = `<tr><th>Subject</th><th>Marks</th><th>Grade</th><th>Points</th></tr>` +
    res.marks.map(m => `<tr>
      <td>${m.subject_code} — ${m.subject_name}</td>
      <td>${m.marks}</td>
      <td>${m.grade}</td>
      <td>${m.grade_points.toFixed(1)}</td>
    </tr>`).join('');
})().catch(console.error);
