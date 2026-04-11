<template>
  <div class="doctor-wrapper">
    <nav class="navbar navbar-expand-lg bg-white shadow-sm fixed-top px-4 py-3">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold text-primary fs-4" href="#">MediCare <span class="text-secondary small">| Doctor Panel</span></a>
        <div class="d-flex align-items-center gap-3">
          <div class="text-end d-none d-md-block line-height-sm">
            <span class="d-block fw-bold text-dark">{{ user.name }}</span>
            <small class="text-muted text-uppercase" style="font-size: 0.7rem;">{{ user.specialization }}</small>
          </div>
          <div class="avatar-circle bg-blue text-white">{{ user.initial }}</div>
          <button @click="logout" class="btn btn-light border btn-sm px-3 rounded-pill">Sign Out</button>
        </div>
      </div>
    </nav>

    <div class="container" style="margin-top: 100px;">
      <div class="row g-4">
        <div class="col-lg-4">
          <div class="card border-0 shadow-sm rounded-4 mb-4 bg-primary-gradient text-white">
            <div class="card-body p-4 text-center">
              <h1 class="display-4 fw-bold mb-0">{{ upcomingAppointments.length }}</h1>
              <p class="opacity-75">Active Appointments</p>
            </div>
          </div>

          <div class="card border-0 shadow-sm rounded-4 bg-white">
            <div class="card-body p-4">
              <h6 class="fw-bold text-dark mb-3"> Set 7-Day Schedule</h6>
              <form @submit.prevent="updateAvailability">
                <div class="schedule-container mb-3 border rounded-3 bg-light p-2" style="max-height: 250px; overflow-y: auto;">
                  <div v-for="(day, index) in schedule" :key="index" class="d-flex align-items-center justify-content-between mb-2 pb-2 border-bottom">
                    <div class="d-flex align-items-center gap-2" style="width: 45%;">
                      <div class="form-check form-switch m-0">
                        <input class="form-check-input" type="checkbox" v-model="day.is_available">
                      </div>
                      <span class="small fw-bold" :class="day.is_available ? 'text-dark' : 'text-muted text-decoration-line-through'">
                        {{ formatDate(day.date) }}
                      </span>
                    </div>
                    <div class="d-flex gap-1" style="width: 55%;" v-if="day.is_available">
                      <input v-model="day.start_time" type="time" class="form-control form-control-sm border-0 shadow-sm">
                      <input v-model="day.end_time" type="time" class="form-control form-control-sm border-0 shadow-sm">
                    </div>
                    <div style="width: 55%;" v-else class="text-end">
                      <span class="badge bg-danger-subtle text-danger">Off Duty</span>
                    </div>
                  </div>
                </div>
                <div class="mb-3">
                   <label class="small text-muted fw-bold">Consultation Fee</label>
                   <input v-model="fee" type="number" class="form-control bg-light border-0 shadow-none" required>
                </div>
                <button type="submit" class="btn btn-primary-gradient w-100 text-white btn-sm py-2 fw-bold shadow-sm">Save Schedule</button>
              </form>
            </div>
          </div>
        </div>

        <div class="col-lg-8">
          <div class="card border-0 shadow-sm rounded-4 bg-white mb-4">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <h5 class="fw-bold m-0 text-primary"> Upcoming Schedule</h5>
                <button class="btn btn-sm btn-light border" @click="fetchAppointments">Refresh</button>
              </div>
              <div v-if="upcomingAppointments.length === 0" class="text-center py-5 text-muted">No active appointments.</div>
              <div v-else class="table-responsive">
                <table class="table align-middle">
                  <thead class="bg-light small text-uppercase text-muted">
                    <tr><th>Patient</th><th>Date & Time</th><th>Status</th><th class="text-end">Actions</th></tr>
                  </thead>
                  <tbody>
                    <tr v-for="appt in upcomingAppointments" :key="appt.id">
                      <td class="fw-bold">{{ appt.patient_name }}</td>
                      <td>{{ appt.date }} <small class="text-muted d-block">{{ appt.time }}</small></td>
                      <td><span class="badge rounded-pill bg-primary-subtle text-primary">{{ appt.status }}</span></td>
                      <td class="text-end">
                        <button @click="viewHistory(appt.patient_id)" class="btn btn-sm btn-outline-secondary me-1">History</button>
                        <span v-if="appt.status === 'Booked'">
                          <button @click="updateStatus(appt.id, 'Confirmed')" class="btn btn-sm btn-primary-soft me-1">Confirm</button>
                          <button @click="updateStatus(appt.id, 'Cancelled')" class="btn btn-sm btn-danger-soft">✕</button>
                        </span>
                        <span v-if="appt.status === 'Confirmed'">
                          <button @click="openTreatmentModal(appt)" class="btn btn-sm btn-success text-white fw-bold">Treat</button>
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div class="card border-0 shadow-sm rounded-4 bg-white ">
            <div class="card-body p-4">
              <h6 class="fw-bold text-secondary mb-4"> Past & Closed Records</h6>
              <div v-if="pastAppointments.length === 0" class="text-center py-3 text-muted small">No history.</div>
              <div v-else class="table-responsive">
                <table class="table align-middle table-sm">
                  <tbody>
                    <tr v-for="appt in pastAppointments" :key="appt.id">
                      <td>{{ appt.patient_name }}</td>
                      <td class="text-muted">{{ appt.date }}</td>
                      <td><span class="badge rounded-pill" :class="appt.status === 'Completed' ? 'bg-success-subtle text-success' : 'bg-danger-subtle text-danger'">{{ appt.status }}</span></td>
                      <td class="text-end"><button @click="viewHistory(appt.patient_id)" class="btn btn-sm btn-light border">View</button></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="treatmentModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-0 pb-0">
            <h5 class="modal-title fw-bold">Add Treatment</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="submitTreatment">
              <div class="mb-3">
                <label class="fw-bold small text-muted">Diagnosis</label>
                <textarea v-model="treatment.diagnosis" class="form-control bg-light border-0" required></textarea>
              </div>
              <div class="mb-3">
                <label class="fw-bold small text-muted">Prescription</label>
                <textarea v-model="treatment.prescription" class="form-control bg-light border-0" rows="3" required></textarea>
              </div>
              <div class="mb-3">
                <label class="small fw-bold text-muted">Additional Notes</label>
                <textarea v-model="treatment.notes" class="form-control bg-light border-0" rows="2" placeholder="Any specific instructions "></textarea>
              </div>
              <div class="mb-3">
              <label class="small fw-bold text-muted">Next Recommended Visit</label>
              <input type="date" v-model="treatment.next_visit" class="form-control bg-light border-0 shadow-none">
              </div>
              <button type="submit" class="btn btn-primary-gradient w-100 fw-bold py-2 text-white border-0">Save</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="historyModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-0 pb-0">
            <h5 class="modal-title fw-bold">Medical History</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4 bg-light">
            <div v-if="patientHistory.length === 0" class="text-center py-3">No records.</div>
            <div v-else class="list-group">
              <div v-for="record in patientHistory" :key="record.id" class="list-group-item border-0 mb-3 rounded-4 p-4 shadow-sm">
                
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <h6 class="fw-bold m-0">{{ record.date }} - <small class="text-primary">{{ record.doctor }}</small></h6>
                  <button 
                    v-if="isMyRecord(record.doctor)" 
                    @click="toggleEdit(record)" 
                    class="btn btn-sm btn-light border rounded-pill px-3"
                  >
                    {{ record.isEditing ? 'Cancel' : 'Edit' }}
                  </button>
                </div>
                
                <hr class="my-2 opacity-10">

                <div v-if="!record.isEditing">
                  <p class="mb-1"><strong>Diagnosis:</strong> {{ record.diagnosis }}</p>
                  <p class="mb-1 text-secondary"><strong>Rx:</strong> {{ record.prescription }}</p>
                  <p v-if="record.notes" class="mb-0 text-muted small"><strong>Notes:</strong> {{ record.notes }}</p>
                </div>

                <div v-else>
                  <div class="mb-2">
                    <label class="small fw-bold text-muted">Diagnosis</label>
                    <input v-model="record.temp_diagnosis" class="form-control form-control-sm">
                  </div>
                  <div class="mb-3">
                    <label class="small fw-bold text-muted">Prescription</label>
                    <textarea v-model="record.temp_prescription" class="form-control form-control-sm" rows="2"></textarea>
                  </div>
                  <button @click="saveHistoryUpdate(record)" class="btn btn-sm btn-success w-100 text-white fw-bold">Save Changes</button>
                </div>

              </div>
            </div>
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
      user: { name: 'Doctor', specialization: 'Specialist', initial: 'D' },
      schedule: [], fee: '', appointments: [], patientHistory: [],
      treatment: { id: null, diagnosis: '', prescription: '', notes: '', next_visit: '' },
      modals: { treatment: null, history: null },
    };
  },
  computed: {
    upcomingAppointments() { return this.appointments.filter(a => ['Booked', 'Confirmed'].includes(a.status)); },
    pastAppointments() { return this.appointments.filter(a => ['Completed', 'Cancelled'].includes(a.status)); }
  },
  async mounted() {
    this.fetchUserInfo();
    await this.fetchProfile();
    await this.fetchAppointments();
    
    const treatEl = document.getElementById('treatmentModal');
    const histEl = document.getElementById('historyModal');
    if (treatEl) this.modals.treatment = new bootstrap.Modal(treatEl);
    if (histEl) this.modals.history = new bootstrap.Modal(histEl);
  },
  methods: {
    async updateAvailability() {
      try {
        const token = localStorage.getItem('token');
        await axios.put('http://127.0.0.1:5000/doctor/schedule', { 
          schedule: this.schedule,
          fee: this.fee 
        }, { 
          headers: { Authorization: `Bearer ${token}` } 
        });
        
        alert("7-Day Schedule Updated Successfully!");
      } catch (error) { 
        alert("Failed to update schedule. Check terminal for errors."); 
      }
    },
    isMyRecord(recordDoctorName) {
      return recordDoctorName.toLowerCase().includes(this.user.name.toLowerCase());
    },
    fetchUserInfo() {
      const storedName = localStorage.getItem('username');
      if(storedName) {
          this.user.name = storedName;
          this.user.initial = storedName.charAt(0).toUpperCase();
      }
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const [year, month, day] = dateString.split('-');
      return new Date(year, month - 1, day).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
    },
    async fetchProfile() {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('http://127.0.0.1:5000/doctor/schedule', { headers: { Authorization: `Bearer ${token}` } });
        this.schedule = res.data.schedule; this.fee = res.data.fee;
      } catch (e) { console.error(e); }
    },
    async fetchAppointments() {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('http://127.0.0.1:5000/doctor/appointments', { headers: { Authorization: `Bearer ${token}` } });
        this.appointments = res.data;
      } catch (e) { console.error(e); }
    },
    async updateStatus(id, status) {
      if(!confirm(`Change status to ${status}?`)) return;
      try {
        const token = localStorage.getItem('token');
        await axios.put(`http://127.0.0.1:5000/doctor/appointment/${id}`, { status }, { headers: { Authorization: `Bearer ${token}` } });
        this.fetchAppointments();
      } catch (e) { alert("Failed to update status"); }
    },
    openTreatmentModal(appt) {
      this.treatment.id = appt.id; 
      this.treatment.diagnosis = ''; 
      this.treatment.prescription = '';
      this.treatment.notes = '';
      this.treatment.next_visit = '';
      this.modals.treatment.show();
    },
    async submitTreatment() {
      try {
        const token = localStorage.getItem('token');
        
        await axios.post('http://127.0.0.1:5000/doctor/treat_patient', {
          appointment_id: this.treatment.id, 
          diagnosis: this.treatment.diagnosis, 
          prescription: this.treatment.prescription,
          notes: this.treatment.notes,
          next_visit: this.treatment.next_visit
        }, { headers: { Authorization: `Bearer ${token}` } });
        
        this.modals.treatment.hide(); 
        this.fetchAppointments();
      } catch (e) { alert("Error saving treatment"); }
    },

    async viewHistory(patientId) {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get(`http://127.0.0.1:5000/doctor/patient_history/${patientId}`, { 
            headers: { Authorization: `Bearer ${token}` } 
        });
        
        this.patientHistory = res.data.map(record => ({
            ...record,
            isEditing: false,
            temp_diagnosis: record.diagnosis,
            temp_prescription: record.prescription
        }));
        
        this.modals.history.show();
      } catch (e) { alert("Could not load patient history"); }
    },

    toggleEdit(record) {
        record.isEditing = !record.isEditing;
        if (!record.isEditing) {
            record.temp_diagnosis = record.diagnosis;
            record.temp_prescription = record.prescription;
        }
    },

    async saveHistoryUpdate(record) {
        try {
            const token = localStorage.getItem('token');
            await axios.put(`http://127.0.0.1:5000/doctor/update_treatment/${record.id}`, {
                diagnosis: record.temp_diagnosis,
                prescription: record.temp_prescription
            }, { headers: { Authorization: `Bearer ${token}` } });

            record.diagnosis = record.temp_diagnosis;
            record.prescription = record.temp_prescription;
            record.isEditing = false;
            alert("Record Updated!");
        } catch (e) { alert("Update failed: Backend endpoint might be missing."); }
    },

    logout() { localStorage.clear(); this.$router.push('/login'); }
  }
};
</script>

<style scoped>
.doctor-wrapper { min-height: 100vh; background-color: #f0f2f5; font-family: 'Segoe UI', sans-serif; }
.btn-primary-gradient, .bg-primary-gradient { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.avatar-circle { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }
.btn-primary-soft { background: #e0e7ff; color: #4338ca; border: none; font-weight: 600; }
.btn-danger-soft { background: #fee2e2; color: #991b1b; border: none; font-weight: 600; }
.bg-success-subtle { background-color: #d1fae5; color: #065f46; }
.bg-danger-subtle { background-color: #fee2e2; color: #991b1b; }
.bg-primary-subtle { background-color: #e0e7ff; color: #4338ca; }
</style>