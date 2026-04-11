<template>
  <div class="d-flex admin-bg" style="min-height: 100vh;">
    
    <div class="sidebar bg-white m-3 rounded-4 shadow-sm d-flex flex-column p-3" style="width: 260px; min-height: calc(100vh - 2rem);">
      
      <div class="text-center mt-3 mb-5">
        <h3 class="fw-bold text-primary-gradient m-0">MediCare</h3>
        <small class="text-muted">Admin Panel</small>
      </div>

      <div class="nav flex-column gap-2 flex-grow-1">
        <button class="nav-btn" :class="{'active': activeTab === 'dashboard'}" @click="activeTab = 'dashboard'">
          <span class="me-3"></span> Dashboard 
        </button>
        <button class="nav-btn" :class="{'active': activeTab === 'doctors'}" @click="activeTab = 'doctors'">
           <span class="me-3"></span> Doctors
        </button>
        <button class="nav-btn" :class="{'active': activeTab === 'patients'}" @click="activeTab = 'patients'">
          <span class="me-3"></span> Patients
        </button>
        <button class="nav-btn" :class="{'active': activeTab === 'appointments'}" @click="activeTab = 'appointments'">
          <span class="me-3"></span> Appointments
        </button>
      </div>

      <div class="mt-auto pt-3">
        <button @click="logout" class="btn btn-logout w-100 fw-bold py-2 rounded-3">Sign Out</button>
      </div>
    </div>

    <div class="flex-grow-1 p-4 pe-5" style="max-height: 100vh; overflow-y: auto;">
      
      <div class="d-flex justify-content-between align-items-center mb-5 mt-2">
        <div>
          <h2 class="fw-bold m-0 text-dark">
            <span v-if="activeTab === 'dashboard'">Overview</span>
            <span v-if="activeTab === 'doctors'">Manage Doctors</span>
            <span v-if="activeTab === 'patients'">Manage Patients</span>
            <span v-if="activeTab === 'appointments'">Hospital Appointments</span>
          </h2>
          <p class="text-muted m-0">Welcome back, Admin</p>
        </div>
        <div class="d-flex align-items-center gap-3">
          <div class="text-end">
            <span class="d-block fw-bold text-dark">Super Admin</span>
            <small class="text-muted" style="font-size: 0.75rem;">System Control</small>
          </div>
          <div class="avatar-circle bg-purple text-white">A</div>
        </div>
      </div>

      <div v-if="activeTab === 'dashboard'" class="row g-4 mb-5">
        <div class="col-md-4">
          <div class="card stat-card border-0 rounded-4 shadow-sm h-100">
            <div class="card-body p-4 d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted fw-bold text-uppercase mb-1" style="font-size: 0.8rem;">Total Patients</h6>
                <h2 class="fw-bold text-dark m-0">{{ stats.patients }}</h2>
              </div>
              <div class="icon-box bg-purple-light text-purple">👥</div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card stat-card border-0 rounded-4 shadow-sm h-100">
            <div class="card-body p-4 d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted fw-bold text-uppercase mb-1" style="font-size: 0.8rem;">Active Doctors</h6>
                <h2 class="fw-bold text-dark m-0">{{ stats.doctors }}</h2>
              </div>
              <div class="icon-box bg-blue-light text-blue">👨‍⚕️</div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card stat-card border-0 rounded-4 shadow-sm h-100">
            <div class="card-body p-4 d-flex justify-content-between align-items-center">
              <div>
                <h6 class="text-muted fw-bold text-uppercase mb-1" style="font-size: 0.8rem;">Appointments</h6>
                <h2 class="fw-bold text-dark m-0">{{ stats.appointments }}</h2>
              </div>
              <div class="icon-box bg-green-light text-green">📅</div>
            </div>
          </div>
        </div>
      </div>

      <div class="card border-0 shadow-sm rounded-4 bg-white mb-4">
        <div class="card-body p-4">
          
          <div class="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-3">
  <h5 class="fw-bold m-0">
    <span v-if="activeTab === 'dashboard'">Recent System Activity</span>
    <span v-if="activeTab === 'doctors'">Doctor Search</span>
    <span v-if="activeTab === 'patients'">Patient Search</span>
    <span v-if="activeTab === 'appointments'">Schedule</span>
  </h5>
  
  <div class="d-flex gap-2 align-items-center">
    <input v-if="activeTab !== 'dashboard'" v-model="searchQuery" type="text" 
           class="form-control form-control-sm bg-light border-0 shadow-none rounded-pill px-3" 
           placeholder=" Search records..." style="width: 250px;">
    
    <button v-if="activeTab === 'dashboard'" @click="triggerDaily" 
            class="btn btn-sm btn-outline-primary rounded-pill px-3 fw-bold"> Send Reminders</button>
    <button v-if="activeTab === 'dashboard'" @click="triggerMonthly" 
            class="btn btn-sm btn-outline-success rounded-pill px-3 fw-bold"> Send Reports</button>
    
    <button v-if="activeTab === 'doctors'" class="btn btn-sm btn-primary-gradient rounded-pill px-3 fw-bold" 
            @click="openAddDoctorModal">+ Add Doctor</button>
    
    <button class="btn btn-sm btn-light border rounded-pill px-3" @click="fetchAllData">Refresh</button>
  </div>
</div>

          <div class="table-responsive">
            
            <table v-if="activeTab === 'dashboard' || activeTab === 'appointments'" class="table align-middle">
              <thead class="text-muted small text-uppercase" style="border-bottom: 2px solid #f0f2f5;">
                <tr>
                  <th class="border-0 pb-3">Patient Name</th>
                  <th class="border-0 pb-3">Doctor</th>
                  <th class="border-0 pb-3">Date & Time</th>
                  <th class="border-0 pb-3 text-end">Status</th>
                  <th class="border-0 rounded-end text-end pe-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="appt in filteredAppointments" :key="appt.id">
                  <td class="py-3">
                    <div class="d-flex align-items-center gap-3">
                      <div class="avatar-circle-sm bg-purple-light text-purple">{{ appt.patient_name.charAt(0) }}</div>
                      <div>
                        <span class="fw-bold text-dark d-block">{{ appt.patient_name }}</span>
                      </div>
                    </div>
                  </td>
                  <td class="text-primary fw-medium">{{ appt.doctor_name }}</td>
                  <td>
                     <span class="fw-bold text-dark">{{ formatDateDisplay(appt.date) }}</span>
                     <small class="text-muted d-block">{{ formatTimeDisplay(appt.time) }}</small>
                  </td>
                  <td class="text-end">
                    <span class="badge rounded-pill px-3 py-2 fw-normal" 
                      :class="{
                        'bg-green-light text-green': appt.status === 'Completed',
                        'bg-blue-light text-blue': appt.status === 'Confirmed',
                        'bg-warning-subtle text-warning': appt.status === 'Booked',
                        'bg-danger-subtle text-danger': appt.status === 'Cancelled'
                      }">
                      {{ appt.status }}
                    </span>
                  </td>
                  <td class="text-end pe-3">
  <button @click="deleteAppointment(appt.id)" class="btn btn-sm btn-outline-danger rounded-pill px-3">
    Delete
  </button>
</td>
                </tr>
              </tbody>
            </table>

            <table v-if="activeTab === 'doctors'" class="table align-middle">
              <thead class="text-muted small text-uppercase" style="border-bottom: 2px solid #f0f2f5;">
                <tr>
                  <th class="border-0 pb-3">Name</th>
                  <th class="border-0 pb-3">Email</th>
                  <th class="border-0 pb-3">Role / Spec</th>
                  <th class="border-0 pb-3 text-end">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="doc in filteredDoctors" :key="doc.id">
                  <td class="py-3">
                    <div class="d-flex align-items-center gap-3">
                      <div class="avatar-circle-sm bg-blue-light text-blue">Dr</div>
                      <span class="fw-bold text-dark">{{ doc.name }}</span>
                    </div>
                  </td>
                  <td class="text-muted">{{ doc.email }}</td>
                  <td>
                    <span class="badge bg-green-light text-green px-3 py-2 rounded-pill fw-normal">{{ doc.specialization }}</span>
                  </td>
                  <td class="text-end">
                    <button @click="openEditDoctorModal(doc)" class="btn btn-sm btn-outline-primary fw-bold px-3 rounded-pill me-2">Edit</button>
                    <button @click="deleteDoctor(doc.id)" class="btn btn-sm btn-danger-soft fw-bold px-3 rounded-pill">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>

            <table v-if="activeTab === 'patients'" class="table align-middle">
              <thead class="text-muted small text-uppercase" style="border-bottom: 2px solid #f0f2f5;">
                <tr>
                  <th class="border-0 pb-3">Name</th>
                  <th class="border-0 pb-3">Email</th>
                  <th class="border-0 pb-3">Gender</th>
                  <th class="border-0 pb-3 text-end">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="pat in filteredPatients" :key="pat.id">
                  <td class="py-3">
                    <div class="d-flex align-items-center gap-3">
                      <div class="avatar-circle-sm bg-purple-light text-purple">{{ pat.name.charAt(0) }}</div>
                      <span class="fw-bold text-dark">{{ pat.name }}</span>
                    </div>
                  </td>
                  <td class="text-muted">{{ pat.email }}</td>
                  <td class="text-muted">{{ pat.gender || 'N/A' }}</td>
                  <td class="text-end">
                    <button @click="openEditPatientModal(pat)" class="btn btn-sm btn-outline-primary fw-bold px-3 rounded-pill me-2">Edit</button>
                    <button @click="deletePatient(pat.id)" class="btn btn-sm btn-danger-soft fw-bold px-3 rounded-pill">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>

            <div v-if="(activeTab === 'dashboard' || activeTab === 'appointments') && filteredAppointments.length === 0" class="text-center text-muted py-4">No data available.</div>
            <div v-if="activeTab === 'doctors' && filteredDoctors.length === 0" class="text-center text-muted py-4">No doctors found.</div>
            <div v-if="activeTab === 'patients' && filteredPatients.length === 0" class="text-center text-muted py-4">No patients found.</div>

          </div>
        </div>
      </div>

    </div>

    <div class="modal fade" id="addDoctorModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-0 pb-0">
            <h5 class="modal-title fw-bold">Add New Doctor</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="submitAddDoctor">
              <div class="row mb-3">
                <div class="col-6">
                  <label class="small text-muted fw-bold">First Name</label>
                  <input v-model="newDoctor.first_name" type="text" class="form-control bg-light border-0" required>
                </div>
                <div class="col-6">
                  <label class="small text-muted fw-bold">Last Name</label>
                  <input v-model="newDoctor.last_name" type="text" class="form-control bg-light border-0" required>
                </div>
              </div>
              <div class="mb-3">
                <label class="small text-muted fw-bold">Email</label>
                <input v-model="newDoctor.email" type="email" class="form-control bg-light border-0" required>
              </div>
              <div class="mb-3">
                <label class="small text-muted fw-bold"> Password</label>
                <input v-model="newDoctor.password" type="text" class="form-control bg-light border-0" required>
              </div>
              <div class="row mb-4">
                <div class="col-8">
                  <label class="small text-muted fw-bold">Specialization</label>
                  <input v-model="newDoctor.specialization" type="text" class="form-control bg-light border-0" placeholder="e.g. Cardiologist" required>
                </div>
                <div class="col-4">
                  <label class="small text-muted fw-bold">Exp. in Years</label>
                  <input v-model="newDoctor.experience_years" type="number" class="form-control bg-light border-0" required>
                </div>
              </div>
              <button type="submit" class="btn btn-primary-gradient w-100 fw-bold py-2 text-white border-0 shadow-sm rounded-pill">Register Doctor</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editDoctorModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-0 pb-0">
            <h5 class="modal-title fw-bold">Edit Doctor</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="submitEditDoctor">
              <div class="row mb-3">
                <div class="col-6">
                  <label class="small text-muted fw-bold">First Name</label>
                  <input v-model="editingDoctor.first_name" type="text" class="form-control bg-light border-0" required>
                </div>
                <div class="col-6">
                  <label class="small text-muted fw-bold">Last Name</label>
                  <input v-model="editingDoctor.last_name" type="text" class="form-control bg-light border-0" required>
                </div>
              </div>
              <div class="row mb-4">
                <div class="col-8">
                  <label class="small text-muted fw-bold">Specialization</label>
                  <input v-model="editingDoctor.specialization" type="text" class="form-control bg-light border-0" required>
                </div>
                <div class="col-4">
                  <label class="small text-muted fw-bold">Exp. in Years</label>
                  <input v-model="editingDoctor.experience" type="number" class="form-control bg-light border-0" required>
                </div>
              </div>
              <button type="submit" class="btn btn-primary-gradient w-100 fw-bold py-2 text-white border-0 shadow-sm rounded-pill">Save Changes</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editPatientModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-0 pb-0">
            <h5 class="modal-title fw-bold">Edit Patient</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="submitEditPatient">
              <div class="row mb-3">
                <div class="col-6">
                  <label class="small text-muted fw-bold">First Name</label>
                  <input v-model="editingPatient.first_name" type="text" class="form-control bg-light border-0" required>
                </div>
                <div class="col-6">
                  <label class="small text-muted fw-bold">Last Name</label>
                  <input v-model="editingPatient.last_name" type="text" class="form-control bg-light border-0" required>
                </div>
              </div>
              <div class="row mb-4">
                <div class="col-6">
                  <label class="small text-muted fw-bold">Phone</label>
                  <input v-model="editingPatient.phone" type="text" class="form-control bg-light border-0">
                </div>
                <div class="col-6">
                  <label class="small text-muted fw-bold">Gender</label>
                  <select v-model="editingPatient.gender" class="form-select bg-light border-0">
                    <option>Male</option>
                    <option>Female</option>
                    <option>Other</option>
                  </select>
                </div>
              </div>
              <button type="submit" class="btn btn-primary-gradient w-100 fw-bold py-2 text-white border-0 shadow-sm rounded-pill">Save Changes</button>
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
      activeTab: 'dashboard',
      searchQuery: '',
      stats: { doctors: 0, patients: 0, appointments: 0 },
      appointments: [],
      doctors: [],
      patients: [],
      
      newDoctor: { first_name: '', last_name: '', email: '', password: '', specialization: '', experience_years: '' },
      editingDoctor: { id: null, first_name: '', last_name: '', specialization: '', experience: '' },
      editingPatient: { id: null, first_name: '', last_name: '', phone: '', gender: '' },
      
      addDoctorModal: null,
      editDoctorModal: null,
      editPatientModal: null
    };
  },
  computed: {
    filteredAppointments() {
      if (!this.searchQuery) return this.appointments;
      const q = this.searchQuery.toLowerCase();
      return this.appointments.filter(a => 
        a.patient_name.toLowerCase().includes(q) || 
        a.doctor_name.toLowerCase().includes(q)
      );
    },
    filteredDoctors() {
      if (!this.searchQuery) return this.doctors;
      const q = this.searchQuery.toLowerCase();
      return this.doctors.filter(d => 
        d.name.toLowerCase().includes(q) || 
        d.specialization.toLowerCase().includes(q)
      );
    },
    filteredPatients() {
      if (!this.searchQuery) return this.patients;
      const q = this.searchQuery.toLowerCase();
      return this.patients.filter(p => 
        p.name.toLowerCase().includes(q) || 
        p.email.toLowerCase().includes(q)
      );
    }
  },
  async mounted() {
    this.addDoctorModal = new bootstrap.Modal(document.getElementById('addDoctorModal'));
    this.editDoctorModal = new bootstrap.Modal(document.getElementById('editDoctorModal'));
    this.editPatientModal = new bootstrap.Modal(document.getElementById('editPatientModal'));
    await this.fetchAllData();
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

    async fetchAllData() {
      await this.fetchStats();
      await this.fetchAppointments();
      await this.fetchDoctors();
      await this.fetchPatients();
    },

    async fetchStats() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/admin/stats', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.stats = res.data;
      } catch (e) { console.error("Error fetching stats"); }
    },

    async fetchAppointments() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/admin/appointments', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.appointments = res.data.reverse(); 
      } catch (e) { console.error("Error fetching appointments"); }
    },

    async fetchDoctors() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/admin/doctors', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.doctors = res.data;
      } catch (e) { console.error("Error fetching doctors"); }
    },
    
    async deleteAppointment(id) {
      if (!confirm("Are you sure you want to delete this appointment?")) return;
      
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`http://127.0.0.1:5000/admin/appointment/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("Appointment Deleted Successfully");
        this.fetchAppointments(); 
      } catch (error) {
        alert("Access Denied: You must be an Admin to delete appointments.");
      }
    },

    async fetchPatients() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/admin/patients', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.patients = res.data;
      } catch (e) { console.error("Error fetching patients"); }
    },

    openAddDoctorModal() {
      this.newDoctor = { first_name: '', last_name: '', email: '', password: '', specialization: '', experience_years: '' };
      this.addDoctorModal.show();
    },

    async submitAddDoctor() {
      try {
        const payload = {
          name: `${this.newDoctor.first_name} ${this.newDoctor.last_name}`.trim(),
          email: this.newDoctor.email,
          password: this.newDoctor.password,
          specialization: this.newDoctor.specialization,
          experience: this.newDoctor.experience_years 
        };

        await axios.post('http://127.0.0.1:5000/admin/add_doctor', payload, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        
        alert("Doctor registered successfully!");
        this.addDoctorModal.hide();
        
        this.newDoctor = { first_name: '', last_name: '', email: '', password: '', specialization: '', experience_years: '' };
        
        this.fetchAllData();
      } catch (error) {
        alert("Failed to add doctor: " + (error.response?.data?.message || "Error"));
      }
    },

    openEditDoctorModal(doc) {
      const names = doc.name.split(' ');
      this.editingDoctor = {
        id: doc.id,
        first_name: names[0] || '',
        last_name: names.slice(1).join(' ') || '',
        specialization: doc.specialization,
        experience: doc.experience !== 'N/A' ? doc.experience : 0
      };
      this.editDoctorModal.show();
    },

    async submitEditDoctor() {
      try {
        await axios.put(`http://127.0.0.1:5000/admin/doctor/${this.editingDoctor.id}`, this.editingDoctor, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        alert("Doctor updated successfully!");
        this.editDoctorModal.hide();
        this.fetchAllData();
      } catch (error) {
        alert("Failed to update doctor.");
      }
    },

    openEditPatientModal(pat) {
      const names = pat.name.split(' ');
      this.editingPatient = {
        id: pat.id,
        first_name: names[0] || '',
        last_name: names.slice(1).join(' ') || '',
        phone: pat.phone !== 'N/A' ? pat.phone : '',
        gender: pat.gender !== 'N/A' ? pat.gender : 'Other'
      };
      this.editPatientModal.show();
    },

    async submitEditPatient() {
      try {
        await axios.put(`http://127.0.0.1:5000/admin/patient/${this.editingPatient.id}`, this.editingPatient, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        alert("Patient updated successfully!");
        this.editPatientModal.hide();
        this.fetchAllData();
      } catch (error) {
        alert("Failed to update patient.");
      }
    },

    async deleteDoctor(id) {
      if(!confirm("Do you want to permanently remove this doctor?")) return;
      try {
        await axios.delete(`http://127.0.0.1:5000/admin/doctor/${id}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.fetchAllData();
      } catch (e) { alert("Failed to delete doctor."); }
    },

    async deletePatient(id) {
      if(!confirm(" Do you want to remove this patient?")) return;
      try {
        await axios.delete(`http://127.0.0.1:5000/admin/patient/${id}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.fetchAllData();
      } catch (e) { alert("Failed to delete patient."); }
    },

    async triggerDaily() {
      try {
      const res = await axios.post('http://127.0.0.1:5000/admin/trigger/daily', {}, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      alert(res.data.message);
      } catch (e) { 
      alert("Failed to start daily reminders job."); 
      }
    },

    async triggerMonthly() {
      try {
      const res = await axios.post('http://127.0.0.1:5000/admin/trigger/monthly', {}, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      alert(res.data.message);
      } catch (e) { 
      alert("Failed to start monthly reports job."); 
    }
    },

    logout() {
      localStorage.clear();
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.admin-bg { background-color: #f4f7fe; font-family: 'Segoe UI', sans-serif; }
.text-primary-gradient { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.btn-primary-gradient { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; }

.nav-btn { text-align: left; padding: 12px 20px; background: transparent; border: none; border-radius: 12px; color: #a3aed1; font-weight: 600; transition: all 0.2s ease; margin-bottom: 5px; }
.nav-btn:hover { background-color: #f8f9fc; color: #764ba2; }
.nav-btn.active { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3); }

.btn-logout { background-color: #fff1f2; color: #e11d48; border: none; transition: all 0.2s; }
.btn-logout:hover { background-color: #ffe4e6; color: #be123c; }

.avatar-circle { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }
.avatar-circle-sm { width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.85rem; }
.icon-box { width: 50px; height: 50px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; }

.bg-purple { background-color: #764ba2; }
.bg-purple-light { background-color: #f3e8ff; } .text-purple { color: #7e22ce; }
.bg-blue-light { background-color: #e0f2fe; } .text-blue { color: #0369a1; }
.bg-green-light { background-color: #dcfce7; } .text-green { color: #15803d; }

.stat-card { transition: transform 0.2s; }
.stat-card:hover { transform: translateY(-3px); }

.btn-danger-soft { background: #ffe4e6; color: #e11d48; border: none; }
.btn-danger-soft:hover { background: #fecdd3; color: #be123c; }
.bg-warning-subtle { background-color: #fef9c3; } .text-warning { color: #854d0e; }
.bg-danger-subtle { background-color: #fee2e2; } .text-danger { color: #991b1b; }
</style>