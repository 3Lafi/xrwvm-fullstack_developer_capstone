import React, { useState } from 'react';
import Header from '../Header/Header';
import './Register.css';

const Register = () => {
  const [form, setForm] = useState({ userName: '', firstName: '', lastName: '', email: '', password: '' });
  const [message, setMessage] = useState('');

  const update = (event) => setForm({ ...form, [event.target.name]: event.target.value });
  const submit = async (event) => {
    event.preventDefault();
    const response = await fetch('/djangoapp/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) });
    const data = await response.json();
    if (response.ok) {
      sessionStorage.setItem('username', data.userName);
      sessionStorage.setItem('firstname', data.firstName);
      sessionStorage.setItem('lastname', data.lastName);
      window.location.href = '/';
    } else setMessage(data.message || 'Registration failed.');
  };

  return <><Header /><main className="register-panel"><h1>Create your account</h1>
    <form onSubmit={submit}>
      <label>Username<input required name="userName" value={form.userName} onChange={update} /></label>
      <label>First Name<input required name="firstName" value={form.firstName} onChange={update} /></label>
      <label>Last Name<input required name="lastName" value={form.lastName} onChange={update} /></label>
      <label>Email<input required type="email" name="email" value={form.email} onChange={update} /></label>
      <label>Password<input required type="password" name="password" value={form.password} onChange={update} /></label>
      <button type="submit">Register</button>{message && <p role="alert">{message}</p>}
    </form>
  </main></>;
};

export default Register;
