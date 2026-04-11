<template>
  <div class="home-wrapper">
    
    <div class="orb-container">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
    </div>

    <div class="content-container">
      
      <nav class="navbar navbar-expand-lg p-4">
        <div class="container">
          <a class="navbar-brand fw-bold fs-3 d-flex align-items-center" href="#">
            <span class="brand-text">Medi</span>Care
          </a>
          <div class="d-flex gap-3">
            <router-link to="/login" class="btn btn-glass">Log In</router-link>
            <router-link to="/register" class="btn btn-primary-gradient shadow">Sign Up</router-link>
          </div>
        </div>
      </nav>

      <div class="container d-flex align-items-center hero-height">
        <div class="row align-items-center w-100">
          
          <div class="col-lg-6 mb-5 mb-lg-0">
            <div class="badge-glass mb-4">
              🩵Simplicity & Care
            </div>
            <h1 class="display-3 fw-bold mb-4 lh-sm">
              Your Health, <br>
              <span class="gradient-text">Beautifully Managed.</span>
            </h1>
            <p class="lead text-secondary mb-5">
              We believe hospital management should be invisible—so doctors can focus on what truly matters: <strong>saving lives.</strong>
            </p>
            <div class="d-flex gap-3">
              <router-link to="/register" class="btn btn-primary-gradient btn-lg px-5 shadow-lg">Get Started</router-link>
              <button class="btn btn-white btn-lg px-4 shadow-sm">Learn More</button>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="floating-card p-5 mx-auto text-center">
              
              <div class="icon-circle bg-purple-light text-purple mx-auto mb-4" style="width: 80px; height: 80px; font-size: 2rem;">
                💙
              </div>

              <h4 class="fw-bold mb-3">"Wherever the art of Medicine is loved, there is also a love of Humanity."</h4>
              <p class="text-muted fst-italic mb-4">— Hippocrates</p>
              
              <hr class="opacity-25 my-4">

              <div class="d-flex justify-content-center gap-2 flex-wrap">
                <span class="badge bg-light text-dark rounded-pill py-2 px-3 border">Compassion</span>
                <span class="badge bg-light text-dark rounded-pill py-2 px-3 border">Integrity</span>
                <span class="badge bg-light text-dark rounded-pill py-2 px-3 border">Innovation</span>
              </div>

            </div>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.home-wrapper {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
  background-color: #f8f9fa;
}

.content-container {
  position: relative;
  z-index: 2;
}

.orb-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.7;
  animation: float 10s infinite alternate ease-in-out;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #a18cd1 0%, #fbc2eb 100%);
  top: -100px;
  left: -150px;
}

.orb-2 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, #84fab0 0%, #8fd3f4 100%);
  bottom: -100px;
  right: -100px;
  animation-delay: -2s;
}

.orb-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #ff9a9e 0%, #fecfef 100%);
  top: 40%;
  left: 30%;
  animation-delay: -5s;
}

@keyframes float {
  0% { transform: translate(0, 0); }
  100% { transform: translate(30px, 50px); }
}

.hero-height {
  min-height: 85vh;
}

.brand-text {
  color: #764ba2;
  margin-right: 5px;
}

.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}

.badge-glass {
  display: inline-block;
  background: rgba(255, 255, 255, 0.9);
  padding: 10px 20px;
  border-radius: 50px;
  color: #764ba2;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  border: 1px solid rgba(255,255,255,1);
}

.btn-primary-gradient {
  background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 12px 30px;
  font-weight: 600;
  transition: transform 0.2s;
}
.btn-primary-gradient:hover {
  transform: translateY(-2px);
  color: white;
}

.btn-glass {
  background: rgba(255,255,255,0.5);
  border: 1px solid rgba(0,0,0,0.05);
  color: #333;
  border-radius: 50px;
  padding: 10px 25px;
  font-weight: 600;
}

.btn-white {
  background: white;
  color: #555;
  border-radius: 50px;
  border: none;
  font-weight: 600;
}

.floating-card {
  background: rgba(255, 255, 255, 0.6); /* Slightly more transparent */
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 24px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.05);
  transform: rotate(-2deg);
  transition: transform 0.3s;
  max-width: 450px;
}
.floating-card:hover {
  transform: rotate(0deg) translateY(-5px);
}

.icon-circle {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}
.bg-purple-light { background: #f3e5f5; }
.text-purple { color: #8e24aa; }
</style>