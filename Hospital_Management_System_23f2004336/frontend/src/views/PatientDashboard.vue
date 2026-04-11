<template>
  <div class="patient-wrapper">
    
    <nav class="navbar navbar-expand-lg bg-white shadow-sm fixed-top px-4 py-3">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold text-primary fs-4" href="#">MediCare</a>
        
        <div class="d-flex align-items-center gap-3">
          <div class="text-end d-none d-md-block line-height-sm">
            <span class="d-block fw-bold text-dark">{{ profile.first_name || user.name }}</span>
            <small class="text-muted text-uppercase" style="font-size: 0.7rem;">Patient</small>
          </div>
          <div class="avatar-circle bg-purple text-white">{{ user.initial }}</div>
          
          <button @click="openProfileModal" class="btn btn-light border btn-sm px-3 rounded-pill me-1">Profile</button>
          <button @click="logout" class="btn btn-light border btn-sm px-3 rounded-pill">Sign Out</button>
        </div>
      </div>
    </nav>

    <div class="container" style="margin-top: 100px;">
      <div class="row g-4">
        
        <div class="col-lg-4">
          <div class="card border-0 shadow-sm rounded-4 mb-4 overflow-hidden">
            <div class="card-body p-4 text-center bg-white position-relative">
              <div class="mb-4">
                <h3 class="fw-bold text-dark m-0">Hello, {{ profile.first_name || user.name.split(' ')[0] }}!</h3>
                <p class="text-muted">Manage your health journey.</p>
              </div>
              
              <button @click="activeView = 'doctors'; fetchDoctors()" 
                      class="btn btn-primary-gradient w-100 py-2 mb-3 fw-bold shadow-sm rounded-3 text-white border-0">
                Book New Appointment
              </button>
              
              <button @click="activeView = 'appointments'; fetchMyAppointments()" 
                      class="btn btn-light w-100 py-2 fw-bold text-secondary border rounded-3">
                My Appointments
              </button>
            </div>
          </div>

          <div class="card border-0 shadow-sm rounded-4 bg-white">
            <div class="card-body p-4">
              <h6 class="fw-bold text-dark mb-3">Your Status</h6>
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted">Total Appointments</span>
                <span class="fw-bold text-dark">{{ myAppointments.length }}</span>
              </div>
              <hr class="my-2 opacity-10">
              <div class="d-flex justify-content-between align-items-center">
                <span class="text-muted">Next Checkup</span>
                <span class="fw-bold text-primary">{{ formatDateDisplay(nextCheckupDate) || 'N/A' }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-8">
          <div class="card border-0 shadow-sm rounded-4 bg-white h-100" style="min-height: 500px;">
            <div class="card-body p-4">
              
              <div class="d-flex justify-content-between align-items-center mb-4">
                <h4 class="fw-bold m-0">
                  {{ activeView === 'doctors' ? 'Book Appointment' : 'My Appointments' }}
                </h4>
                
                <div v-if="activeView === 'doctors'">
                  <button class="btn btn-sm btn-light border rounded-pill px-3" @click="activeView='appointments'">Cancel</button>
                </div>
                
                <div v-else class="d-flex gap-2">
                  <button @click="exportHistory" class="btn btn-sm btn-primary-gradient rounded-pill px-3 shadow-sm"> Export History</button>
                  <button class="btn btn-sm btn-light border rounded-pill px-3" @click="fetchMyAppointments">Refresh</button>
                </div>
              </div>

              <div v-if="activeView === 'appointments'">
                <div v-if="myAppointments.length === 0" class="text-center py-5 mt-5">
                   <h5 class="fw-bold text-muted">No appointments yet</h5>
                   <p class="text-secondary small">Click "Book New Appointment" to get started.</p>
                </div>

                <div v-else class="table-responsive">
                  <table class="table align-middle table-hover">
                    <thead class="bg-light small text-uppercase text-muted">
                      <tr>
                        <th class="border-0 rounded-start ps-3">Doctor</th>
                        <th class="border-0">Date & Time</th>
                        <th class="border-0">Status</th>
                        <th class="border-0 rounded-end text-end pe-3">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="appt in myAppointments" :key="appt.id">
                        <td class="ps-3 py-3">
                          <span class="fw-bold d-block text-dark">{{ appt.doctor_name }}</span>
                          <small class="text-muted">{{ appt.specialization }}</small>
                        </td>
                        <td>
                          <div class="d-flex flex-column">
                            <span class="fw-bold text-dark">{{ formatDateDisplay(appt.date) }}</span>
                            <small class="text-muted">{{ formatTimeDisplay(appt.time) }}</small>
                          </div>
                        </td>
                        <td>
                          <span class="badge rounded-pill px-3 py-2 fw-normal" 
                            :class="{
                              'bg-success-subtle text-success': appt.status === 'Completed',
                              'bg-primary-subtle text-primary': appt.status === 'Confirmed',
                              'bg-warning-subtle text-warning': appt.status === 'Booked',
                              'bg-danger-subtle text-danger': appt.status === 'Cancelled'
                            }">
                            {{ appt.status }}
                          </span>
                        </td>
                        <td class="text-end pe-3">
                           
                           <div v-if="appt.status === 'Completed'">
                             <button @click="openTreatmentModal(appt)" class="btn-badge btn-badge-info">View Details</button>
                           </div>
                           
                           <div v-if="appt.status === 'Booked' || appt.status === 'Confirmed'" class="d-flex justify-content-end gap-2">
                             <button @click="openRescheduleModal(appt)" class="btn-badge btn-badge-primary">Reschedule</button>
                             <button @click="cancelAppointment(appt.id)" class="btn-badge btn-badge-danger">Cancel</button>
                           </div>

                           <span v-if="appt.status === 'Cancelled'" class="text-muted small">-</span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div v-if="activeView === 'doctors'">
                
                <div class="row mb-4 g-2">
                  <div class="col-md-8">
                    <input v-model="searchQuery" type="text" class="form-control form-control-lg bg-light border-0 shadow-none" placeholder="Search by doctor name or specialization">
                  </div>
                  <div class="col-md-4">
                    <select v-model="selectedSpecialization" class="form-select form-select-lg bg-light border-0 shadow-none text-secondary">
                      <option value="">All Specializations</option>
                      <option v-for="spec in uniqueSpecializations" :key="spec" :value="spec">
                        {{ spec }}
                      </option>
                    </select>
                  </div>
                </div>
                
                <div class="row g-3">
                  <div class="col-md-6" v-for="doc in filteredDoctors" :key="doc.id">
                    <div class="p-3 border rounded-3 hover-shadow transition-all bg-white">
                      <div class="d-flex justify-content-between align-items-start mb-2">
                        <div>
                          <h6 class="fw-bold m-0 text-dark">{{ doc.name }}</h6>
                          <small class="text-primary">{{ doc.specialization }}</small>
                        </div>
                        <span class="badge bg-light text-dark border">₹{{ doc.fee }}</span>
                        </div>

                        <div class="mt-2">
                         <small class="text-muted">
                            <i class="bi bi-calendar3 me-1"></i> 
                            {{ doc.availability_text || 'Schedule not provided' }}
                         </small>
                        </div>
                        <div class="d-flex gap-2 mt-3">
                          <button @click="openBookingModal(doc)" class="btn btn-sm btn-primary-gradient w-100 text-white border-0 shadow-sm">Book Now</button>
                        </div>
                      </div>
                    </div>
                  <div v-if="filteredDoctors.length === 0" class="col-12 text-center text-muted py-5">
                    <h5 class="fw-bold">No doctors found</h5>
                    <p class="small">Try adjusting your search.</p>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

      </div>
    </div>
    
    <div class="modal fade" id="bookingModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-0 pb-0">
            <h5 class="modal-title fw-bold">{{ isRescheduling ? 'Reschedule Appointment' : 'Confirm Booking' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            <div v-if="selectedDoctor" class="p-3 bg-purple-light rounded-3 mb-4 d-flex align-items-center gap-3">
              <div class="avatar-circle bg-white text-purple shadow-sm">Dr</div>
              <div>
                <h6 class="fw-bold m-0 text-dark">{{ selectedDoctor.name || selectedDoctor.doctor_name }}</h6>
                <small class="text-secondary">{{ selectedDoctor.specialization }}</small>
              </div>
            </div>
            
            <div v-if="doctorSchedule.length > 0" class="mb-4">
              <label class="fw-bold small text-muted mb-2">Doctor's Availability for next 7 days</label>
              <div class="d-flex flex-wrap gap-2">
                <span v-for="day in doctorSchedule" :key="day.date" 
                      class="badge border fw-normal"
                      :class="day.is_available ? 'bg-light text-dark' : 'bg-danger-subtle text-danger'">
                  {{ formatDateDisplay(day.date) }}: 
                  <span v-if="day.is_available" class="fw-bold">{{ day.start_time }} - {{ day.end_time }}</span>
                  <span v-else class="fw-bold">Off</span>
                </span>
              </div>
            </div>
            
            <form @submit.prevent="submitBooking">
              <div class="mb-3">
                <label class="fw-bold small text-muted">Select Date</label>
                <input v-model="booking.date" type="date" class="form-control form-control-lg bg-light border-0" required :min="todayDate">
              </div>
              <div class="mb-4">
                <label class="fw-bold small text-muted">Select Time</label>
                <input v-model="booking.time" type="time" class="form-control form-control-lg bg-light border-0" required>
              </div>
              <button type="submit" class="btn btn-primary-gradient w-100 py-2 text-white fw-bold border-0 rounded-3 shadow-sm">
                {{ isRescheduling ? 'Confirm New Time' : 'Confirm Appointment' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="treatmentDetailsModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-0 pb-0">
            <h5 class="modal-title fw-bold text-primary">Treatment History</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4" v-if="selectedTreatment">
            <div class="d-flex align-items-center gap-3 mb-4 pb-3 border-bottom">
              <div class="avatar-circle bg-primary-subtle text-primary">Dr</div>
              <div>
                <h6 class="fw-bold m-0">{{ selectedTreatment.doctor_name }}</h6>
                <small class="text-muted">{{ formatDateDisplay(selectedTreatment.date) }} at {{ formatTimeDisplay(selectedTreatment.time) }}</small>
              </div>
            </div>
            
            <div class="mb-3">
              <h6 class="fw-bold small text-muted text-uppercase mb-2">Diagnosis</h6>
              <div class="p-3 bg-light rounded-3 text-dark">{{ selectedTreatment.diagnosis }}</div>
            </div>
            
            <div class="mb-3">
              <h6 class="fw-bold small text-muted text-uppercase mb-2">Prescription</h6>
              <div class="p-3 bg-light rounded-3 text-dark">{{ selectedTreatment.prescription }}</div>
            </div>

            <div class="mb-3" v-if="selectedTreatment.notes">
              <h6 class="fw-bold small text-muted text-uppercase mb-2">Doctor's Notes</h6>
              <div class="p-3 bg-light rounded-3 text-dark">{{ selectedTreatment.notes }}</div>
            </div>
            
            <div class="mb-3" v-if="selectedTreatment.next_visit">
  <h6 class="fw-bold small text-muted text-uppercase mb-2">Next Visit</h6>
  <div class="p-3 bg-light rounded-3 text-dark">{{ formatDateDisplay(selectedTreatment.next_visit) }}</div>
</div>

          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="profileModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-0 pb-0">
            <h5 class="modal-title fw-bold">Update Profile</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="updateProfile">
              <div class="row mb-3">
                <div class="col-6">
                  <label class="small text-muted fw-bold">First Name</label>
                  <input v-model="profile.first_name" type="text" class="form-control bg-light border-0" required>
                </div>
                <div class="col-6">
                  <label class="small text-muted fw-bold">Last Name</label>
                  <input v-model="profile.last_name" type="text" class="form-control bg-light border-0" required>
                </div>
              </div>
              <div class="row mb-3">
                <div class="col-6">
                  <label class="small text-muted fw-bold">Phone</label>
                  <input v-model="profile.phone_number" type="text" class="form-control bg-light border-0">
                </div>
                <div class="col-6">
                  <label class="small text-muted fw-bold">Date of Birth</label>
                  <input v-model="profile.dob" type="date" class="form-control bg-light border-0">
                </div>
              </div>
              <div class="mb-3">
                <label class="small text-muted fw-bold">Address</label>
                <input v-model="profile.address" type="text" class="form-control bg-light border-0">
              </div>
              <div class="mb-3">
                <label class="small text-muted fw-bold">Gender</label>
                <select v-model="profile.gender" class="form-select bg-light border-0">
                  <option>Male</option>
                  <option>Female</option>
                  <option>Other</option>
                </select>
              </div>
              <div class="mb-4">
                <label class="small text-muted fw-bold">New Password</label>
                <input v-model="profile.password" type="password" class="form-control bg-light border-0" placeholder="Leave blank to keep current">
              </div>
              <button type="submit" class="btn btn-primary-gradient w-100 fw-bold py-2 text-white border-0 shadow-sm">Save Profile</button>
            </form>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import * as bootstrap from 'bootstrap';

export default {
  data() {
    return {
      user: { name: 'Patient', initial: 'P' },
      profile: { first_name: '', last_name: '', phone_number: '', address: '', dob: '', gender: 'Other', password: '' },
      activeView: 'appointments', 
      searchQuery: '',
      selectedSpecialization: '', 
      doctors: [],
      myAppointments: [], 
      
      selectedDoctor: null,
      doctorSchedule: [], 
      booking: { id: null, date: '', time: '' },
      isRescheduling: false,
      
      selectedTreatment: null,
      modals: { booking: null, treatmentDetails: null, profile: null }
    };
  },
  computed: {
    todayDate() {
      return new Date().toISOString().split('T')[0];
    },
    nextCheckupDate() {
        if (this.myAppointments.length === 0) return 'N/A';
        const upcoming = this.myAppointments.find(a => a.status === 'Confirmed' || a.status === 'Booked');
        return upcoming ? upcoming.date : ''; 
    },
    uniqueSpecializations() {
      const specs = this.doctors.map(doc => doc.specialization);
      return [...new Set(specs)].filter(Boolean); 
    },
    filteredDoctors() {
  let result = this.doctors;

  if (this.selectedSpecialization) {
    const specQ = this.selectedSpecialization.toLowerCase();
    result = result.filter(doc => (doc.specialization || '').toLowerCase().includes(specQ));
  }

  if (this.searchQuery) {
    const lowerQ = this.searchQuery.toLowerCase();
    
    result = result.filter(doc => {
      const nameMatch = (doc.name || '').toLowerCase().includes(lowerQ);
      const specMatch = (doc.specialization || '').toLowerCase().includes(lowerQ);
      const availabilityMatch = (doc.availability_text || '').toLowerCase().includes(lowerQ);

      return nameMatch || specMatch || availabilityMatch;
    });
  }
  return result;
}
  },
  async mounted() {
    this.fetchUserInfo();
    await this.fetchProfile();
    await this.fetchMyAppointments(); 
    
    this.modals.booking = new bootstrap.Modal(document.getElementById('bookingModal'));
    this.modals.treatmentDetails = new bootstrap.Modal(document.getElementById('treatmentDetailsModal'));
    this.modals.profile = new bootstrap.Modal(document.getElementById('profileModal'));
  },
  methods: {
    formatDateDisplay(dateStr) {
      if (!dateStr || dateStr === 'N/A') return dateStr;
      const opts = { month: 'short', day: 'numeric', year: 'numeric' };
      return new Date(dateStr).toLocaleDateString('en-US', opts);
    },
    formatTimeDisplay(timeStr) {
      if (!timeStr) return '';
      const [hour, min] = timeStr.split(':');
      const d = new Date();
      d.setHours(hour, min);
      return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    },

    fetchUserInfo() {
        const storedName = localStorage.getItem('username'); 
        if(storedName) {
            this.user.name = storedName;
            this.user.initial = storedName.charAt(0).toUpperCase();
        }
    },
    
    async exportHistory() {
      try {
        const token = localStorage.getItem('token');
        await axios.post('http://127.0.0.1:5000/patient/export_history', {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("Export job started in the background! You will receive an email alert shortly.");
      } catch (error) {
        alert("Failed to start export.");
      }
    },

    async fetchProfile() {
    try {
        const token = localStorage.getItem('token'); 
        
        if (!token) {
            console.error("No token found in storage!");
            this.$router.push('/login');
            return;
        }

        const response = await axios.get('http://127.0.0.1:5000/patient/profile', {
            headers: { 
                Authorization: `Bearer ${token}` 
            }
        });
        this.profile = response.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
    }
},
    
    openProfileModal() {
      this.profile.password = '';
      this.modals.profile.show();
    },

    async updateProfile() {
      try {
        const token = localStorage.getItem('token');
        await axios.put('http://127.0.0.1:5000/patient/profile', this.profile, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("Profile Updated Successfully!");
        this.modals.profile.hide();
        localStorage.setItem('first_name', this.profile.first_name);
      } catch (error) { alert("Failed to update profile."); }
    },

    async fetchDoctors() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/patient/doctors', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.doctors = response.data;
      } catch (error) { console.error("Error fetching doctors:", error); }
    },

    async fetchMyAppointments() {
      try {
        const token = localStorage.getItem('token'); 
        const response = await axios.get('http://127.0.0.1:5000/patient/my_appointments', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.myAppointments = response.data;
      } catch (error) { console.error("Error fetching appointments", error); }
    },

    async fetchDoctorSchedule(doctorId) {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get(`http://127.0.0.1:5000/patient/doctor/${doctorId}/schedule`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.doctorSchedule = res.data;
      } catch (error) {
        console.error("Could not fetch schedule", error);
        this.doctorSchedule = [];
      }
    },

    async openBookingModal(doctor) {
      this.isRescheduling = false;
      this.selectedDoctor = doctor;
      this.booking = { id: null, date: '', time: '' }; 
      await this.fetchDoctorSchedule(doctor.id);
      this.modals.booking.show();
    },

    async openRescheduleModal(appt) {
      this.isRescheduling = true;
      this.selectedDoctor = appt; 
      this.booking = { id: appt.id, date: appt.date, time: appt.time };
      await this.fetchDoctorSchedule(appt.doctor_id);
      this.modals.booking.show();
    },

    async submitBooking() {
      try {
        const token = localStorage.getItem('token'); 
        
        if (this.isRescheduling) {
          await axios.put(`http://127.0.0.1:5000/patient/appointment/${this.booking.id}/reschedule`, {
            date: this.booking.date,
            time: this.booking.time,
          }, { headers: { Authorization: `Bearer ${token}` } });
          alert("Appointment Rescheduled Successfully!");
        } else {
          await axios.post('http://127.0.0.1:5000/patient/book', {
            doctor_id: this.selectedDoctor.id,
            date: this.booking.date,
            time: this.booking.time,
            reason: "General Checkup"
          }, { headers: { Authorization: `Bearer ${token}` } });
          alert("Success! Appointment Booked.");
        }
        
        this.modals.booking.hide();
        this.activeView = 'appointments'; 
        this.fetchMyAppointments();       
      } catch (error) {
        alert("Action Failed: " + (error.response?.data?.message || "Error"));
      }
    },

    async cancelAppointment(id) {
      if(!confirm("Are you sure you want to cancel this appointment?")) return;
      try {
        const token = localStorage.getItem('token');
        await axios.put(`http://127.0.0.1:5000/patient/appointment/${id}/cancel`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.fetchMyAppointments();
      } catch (error) { alert("Cancellation failed"); }
    },

    openTreatmentModal(appt) {
      this.selectedTreatment = appt;
      this.modals.treatmentDetails.show();
    },

    logout() {
      localStorage.clear();
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.patient-wrapper { min-height: 100vh; background-color: #f0f2f5; position: relative; overflow-x: hidden; font-family: 'Segoe UI', sans-serif; }
.btn-primary-gradient { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); transition: transform 0.2s; }
.btn-primary-gradient:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); }
.text-primary { color: #667eea !important; }
.bg-purple { background-color: #764ba2; }
.bg-purple-light { background-color: #f3e5f5; }
.text-purple { color: #764ba2; }
.avatar-circle { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }
.hover-shadow:hover { box-shadow: 0 5px 15px rgba(0,0,0,0.05); cursor: pointer; border-color: #667eea !important; }
.transition-all { transition: all 0.3s ease; }

.btn-badge { border: none; font-size: 0.8rem; font-weight: 600; padding: 6px 14px; border-radius: 50rem; transition: all 0.2s ease; cursor: pointer; }
.btn-badge:hover { transform: translateY(-1px); box-shadow: 0 4px 6px rgba(0,0,0,0.05); }

.btn-badge-info { background-color: #ccfbf1; color: #0f766e; } 
.btn-badge-primary { background-color: #e0e7ff; color: #4338ca; } 
.btn-badge-danger { background-color: #ffe4e6; color: #e11d48; } 

.bg-success-subtle { background-color: #d1fae5; } .text-success { color: #065f46; }
.bg-primary-subtle { background-color: #e0e7ff; } .text-primary { color: #4338ca; }
.bg-warning-subtle { background-color: #fef9c3; } .text-warning { color: #854d0e; }
.bg-danger-subtle { background-color: #fee2e2; } .text-danger { color: #991b1b; }
</style>