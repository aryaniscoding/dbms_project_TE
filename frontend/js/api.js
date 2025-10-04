const API_BASE = "http://127.0.0.1:8000";

function authHeaders(){
  const t = localStorage.getItem('token');
  return t ? { 'Authorization': `Bearer ${t}` } : {};
}

async function apiLogin(username, password){
  const res = await fetch(`${API_BASE}/auth/login`, {
    method:'POST',
    headers: { 'Content-Type':'application/json' },
    body: JSON.stringify({ username, password })
  });
  if(!res.ok) return null;
  return await res.json();
}

async function apiGet(path){
  const res = await fetch(`${API_BASE}${path}`, { headers: { ...authHeaders() }});
  if(!res.ok) throw new Error(await res.text());
  return await res.json();
}

async function apiPost(path, body){
  const res = await fetch(`${API_BASE}${path}`, {
    method:'POST',
    headers: { 'Content-Type':'application/json', ...authHeaders() },
    body: JSON.stringify(body)
  });
  if(!res.ok) throw new Error(await res.text());
  return await res.json();
}
