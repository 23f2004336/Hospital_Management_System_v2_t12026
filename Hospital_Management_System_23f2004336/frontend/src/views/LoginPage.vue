<template>
  <div class="page-wrapper">
    <div class="orb-container">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
    </div>

    <div class="content-container d-flex align-items-center justify-content-center">
      <div class="glass-card p-5">
        
        <div class="text-center mb-4">
          <h2 class="fw-bold mb-2">Welcome Back</h2>
          <p class="text-muted">Enter your details to access your account</p>
        </div>

        <form @submit.prevent="login">
          <div class="mb-4">
            <label class="form-label small fw-bold text-secondary">Email Address</label>
            <input type="email" class="form-control" v-model="email" placeholder="name@hospital.com" required>
          </div>
          <div class="mb-4">
            <label class="form-label small fw-bold text-secondary">Password</label>
            <input type="password" class="form-control" v-model="password" placeholder="••••••••" required>
          </div>
          
          <button type="submit" class="btn btn-primary-gradient w-100 py-3 mb-3 shadow">Log In</button>
        </form>

        <p v-if="error" class="text-danger text-center small fw-bold">{{ error }}</p>

        <div class="text-center mt-3">
          <p class="small text-muted mb-2">Don't have an account? 
            <router-link to="/register" class="fw-bold text-purple text-decoration-none">Sign Up</router-link>
          </p>
          <router-link to="/" class="small text-secondary text-decoration-none"> Back to Home</router-link>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      error: ''
    };
  },
  methods: {
    async login() {
      try {
        console.log("Attempting login...");
        const response = await axios.post('http://127.0.0.1:5000/login', {
          email: this.email,
          password: this.password
        });
        
        console.log("Login Successful! Server Response:", response.data);
        console.log("Saving First Name:", response.data.first_name);

        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('role', response.data.role);
        localStorage.setItem('username', response.data.username);
        
        if (response.data.first_name) {
             localStorage.setItem('first_name', response.data.first_name);
        } else {
             console.warn("Server did not send first_name!");
             localStorage.setItem('first_name', response.data.username);
        }

        const userRole = response.data.role.toLowerCase(); 

if (userRole === 'admin') {
  this.$router.push('/admin-dashboard');
} else if (userRole === 'doctor') {
  this.$router.push('/doctor-dashboard');
} else if (userRole === 'patient') {
  this.$router.push('/patient-dashboard');
} else {
  console.error("Unknown role detected:", userRole);
  this.$router.push('/'); 
}
      } catch (err) {
        console.error("Login Error:", err);
        this.error = "Invalid Credentials or Server Error";
      }
    }
  }
};
</script>

<style scoped>
.page-wrapper { position: relative; min-height: 100vh; width: 100%; overflow: hidden; background-color: #f8f9fa; }
.content-container { position: relative; z-index: 2; min-height: 100vh; }
.orb-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; }
.orb { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.7; animation: float 10s infinite alternate ease-in-out; }
.orb-1 { width: 500px; height: 500px; background: radial-gradient(circle, #a18cd1 0%, #fbc2eb 100%); top: -100px; left: -150px; }
.orb-2 { width: 600px; height: 600px; background: radial-gradient(circle, #84fab0 0%, #8fd3f4 100%); bottom: -100px; right: -100px; }
.orb-3 { width: 300px; height: 300px; background: radial-gradient(circle, #ff9a9e 0%, #fecfef 100%); top: 40%; left: 30%; }
@keyframes float { 0% { transform: translate(0, 0); } 100% { transform: translate(30px, 50px); } }
.glass-card { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.8); border-radius: 24px; box-shadow: 0 20px 50px rgba(0,0,0,0.05); width: 100%; max-width: 450px; }
.form-control { background: rgba(255, 255, 255, 0.9); border: 1px solid #e2e8f0; padding: 12px; border-radius: 12px; }
.form-control:focus { border-color: #764ba2; box-shadow: 0 0 0 3px rgba(118, 75, 162, 0.1); }
.btn-primary-gradient { background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 12px; font-weight: 600; transition: transform 0.2s; }
.btn-primary-gradient:hover { transform: translateY(-2px); color: white; }
.text-purple { color: #764ba2; }
</style>