<template>
  <div class="subject-management">
    <div class="header">
      <h1>Subject Management</h1>
      <button @click="showCreateModal = true" class="btn btn-primary">Add Subject</button>
    </div>

    <!-- Search -->
    <div class="search-container">
      <input 
        v-model="searchTerm" 
        type="text" 
        placeholder="Search subjects..." 
        class="search-input"
      >
    </div>

    <!-- Subjects Table -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Created Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="subject in filteredSubjects" :key="subject.id">
            <td>{{ subject.name }}</td>
            <td>{{ subject.description }}</td>
            <td>{{ formatDate(subject.created_at) }}</td>
            <td>
              <button @click="editSubject(subject)" class="btn btn-sm btn-secondary">Edit</button>
              <button @click="deleteSubject(subject.id)" class="btn btn-sm btn-danger">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click="closeModal">
      dfklasdkl;jklfjklsdjk;lsdjk;sdkk;jjk;sdfkjk;jk;sf
      <div class="modal" @click.stop>
        sdfsdfsdfefdssd
        <div class="modal-header">
          <h3>{{ showCreateModal ? 'Create Subject' : 'Edit Subject' }}</h3>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          fgjkjklfvmk;sdmfeipro
          <form @submit.prevent="saveSubject">
            <div class="form-group">
              <label>Name *</label>
              <input v-model="subjectForm.name" type="text" required class="form-control">
            </div>
            <div class="form-group">
              <label>Description</label>
              <textarea v-model="subjectForm.description" class="form-control" rows="3"></textarea>
            </div>
            <div class="form-actions">
              <button type="button" @click="closeModal" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">{{ showCreateModal ? 'Create' : 'Update' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SubjectManagement',
  data() {
    return {
      subjects: [],
      searchTerm: '',
      showCreateModal: false,
      showEditModal: false,
      subjectForm: {
        id: null,
        name: '',
        description: ''
      }
    }
  },
  computed: {
    filteredSubjects() {
      return this.subjects.filter(subject =>
        subject.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        subject.description.toLowerCase().includes(this.searchTerm.toLowerCase())
      )
    }
  },
  async mounted() {
    await this.fetchSubjects()
  },
  methods: {
    async fetchSubjects() {
      try {
        const response = await axios.get('/admin/subjects')
        this.subjects = response.data
      } catch (error) {
        console.error('Error fetching subjects:', error)
      }
    },
    editSubject(subject) {
      this.subjectForm = { ...subject }
      this.showEditModal = true
    },
    async saveSubject() {
      try {
        if (this.showCreateModal) {
          await axios.post('/admin/subjects', this.subjectForm)
        } else {
          await axios.put(`/admin/subjects/${this.subjectForm.id}`, this.subjectForm)
        }
        await this.fetchSubjects()
        this.closeModal()
      } catch (error) {
        console.error('Error saving subject:', error)
      }
    },
    async deleteSubject(id) {
      if (confirm('Are you sure you want to delete this subject?')) {
        try {
          await axios.delete(`/admin/subjects/${id}`)
          await this.fetchSubjects()
        } catch (error) {
          console.error('Error deleting subject:', error)
        }
      }
    },
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.subjectForm = { id: null, name: '', description: '' }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.subject-management {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-container {
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.table-container {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}

.btn-primary { background: #007bff; color: white; }
.btn-secondary { background: #6c757d; color: white; }
.btn-danger { background: #dc3545; color: white; }
.btn-sm { padding: 4px 8px; font-size: 0.875rem; }

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal {
  background: rgb(158, 38, 38);
  border-radius: 8px;
  width: 500px;
  max-width: 90vw;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.modal-body {
  padding: 20px;
  background: white;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

/* Fix the modal overlay and content */
.modal-overlay {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  background: rgba(0, 0, 0, 0.6) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 99999 !important;
  padding: 20px !important;
}

.modal {
  background: white !important;
  border-radius: 8px !important;
  width: 500px !important;
  max-width: 90vw !important;
  max-height: 90vh !important;
  overflow-y: auto !important;
  z-index: 100000 !important;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
  position: relative !important;
  display: block !important;
}

.modal-header {
  padding: 20px !important;
  border-bottom: 1px solid #eee !important;
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  background: white !important;
}

.modal-body {
  padding: 20px !important;
  background: white !important;
}

/* Ensure the form is visible */
.form-group {
  margin-bottom: 15px !important;
  display: block !important;
}

.form-control {
  width: 100% !important;
  padding: 8px 12px !important;
  border: 1px solid #ddd !important;
  border-radius: 4px !important;
  background: white !important;
  color: black !important;
  box-sizing: border-box !important;
}

.form-actions {
  display: flex !important;
  justify-content: flex-end !important;
  gap: 10px !important;
  margin-top: 20px !important;
}


</style>
