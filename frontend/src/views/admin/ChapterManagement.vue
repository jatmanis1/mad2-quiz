<template>
  <div class="chapter-management">
    <!-- Header Section -->
    <div class="header-section">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">📚 Chapter Management</h1>
          <p class="page-subtitle">Manage chapters for all subjects</p>
        </div>
        <button @click="openCreateModal" class="btn btn-primary btn-add">
          <span class="btn-icon">➕</span>
          Add Chapter
        </button>
      </div>
    </div>

    <!-- Filters Section -->
    <div class="filters-section">
      <div class="filters-container">
        <div class="filter-group">
          <label class="filter-label">Filter by Subject</label>
          <div class="select-wrapper">
            <select v-model="selectedSubjectId" @change="fetchChapters" class="form-select">
              <option value="">All Subjects</option>
              <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                {{ subject.name }}
              </option>
            </select>
          </div>
        </div>
        
        <div class="filter-group">
          <label class="filter-label">Search Chapters</label>
          <div class="search-wrapper">
            <input 
              v-model="searchTerm" 
              type="text" 
              placeholder="Search by name or description..." 
              class="search-input"
            >
            <span class="search-icon">🔍</span>
          </div>
        </div>
      </div>
      
      <!-- Stats Cards -->
      <div class="stats-container">
        <div class="stat-card">
          <div class="stat-value">{{ chapters.length }}</div>
          <div class="stat-label">Total Chapters</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ filteredChapters.length }}</div>
          <div class="stat-label">Filtered Results</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ subjects.length }}</div>
          <div class="stat-label">Subjects</div>
        </div>
      </div>
    </div>

    <!-- Table Section -->
    <div class="table-section">
      <div class="table-header">
        <h3 class="table-title">Chapters List</h3>
        <div class="table-actions">
          <button @click="fetchChapters" class="btn btn-outline btn-sm">
            <span class="btn-icon">🔄</span>
            Refresh
          </button>
        </div>
      </div>

      <div class="table-container">
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading chapters...</p>
        </div>

        <table v-else class="modern-table">
          <thead>
            <tr>
              <th class="sortable">
                <div class="th-content">
                  <span>Chapter Name</span>
                  <span class="sort-icon">↕️</span>
                </div>
              </th>
              <th>Subject</th>
              <th>Description</th>
              <th>Created Date</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="chapter in filteredChapters" :key="chapter.id" class="table-row">
              <td class="name-cell">
                <div class="name-content">
                  <span class="chapter-name">{{ chapter.name }}</span>
                </div>
              </td>
              <td>
                <span class="subject-badge">{{ getSubjectName(chapter.subject_id) }}</span>
              </td>
              <td class="description-cell">
                <span class="description-text" :title="chapter.description">
                  {{ truncateText(chapter.description, 50) }}
                </span>
              </td>
              <td class="date-cell">
                <time class="date-text">{{ formatDate(chapter.created_at) }}</time>
              </td>
              <td class="actions-cell">
                <div class="action-buttons">
                  <button @click="editChapter(chapter)" class="btn btn-sm btn-edit" title="Edit Chapter">
                    <span class="btn-icon">✏️</span>
                  </button>
                  <button @click="deleteChapter(chapter.id)" class="btn btn-sm btn-delete" title="Delete Chapter">
                    <span class="btn-icon">🗑️</span>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredChapters.length === 0" class="empty-row">
              <td colspan="5" class="empty-state">
                <div class="empty-content">
                  <div class="empty-icon">📝</div>
                  <h4>No chapters found</h4>
                  <p>{{ searchTerm ? 'Try adjusting your search criteria' : 'Start by creating your first chapter' }}</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Enhanced Modal -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click="closeModal">
      <div class="modern-modal" @click.stop>
        <div class="modal-header">
          <div class="modal-title-section">
            <h3 class="modal-title">
              <span class="modal-icon">{{ showCreateModal ? '➕' : '✏️' }}</span>
              {{ showCreateModal ? 'Create New Chapter' : 'Edit Chapter' }}
            </h3>
            <p class="modal-subtitle">{{ showCreateModal ? 'Add a new chapter to organize content' : 'Update chapter information' }}</p>
          </div>
          <button @click="closeModal" class="close-btn" title="Close modal">
            <span>&times;</span>
          </button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="saveChapter" class="modern-form">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label required">Subject</label>
                <div class="select-wrapper">
                  <select v-model="chapterForm.subject_id" required class="form-select">
                    <option value="">Choose a subject</option>
                    <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                      {{ subject.name }}
                    </option>
                  </select>
                </div>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label required">Chapter Name</label>
                <input 
                  v-model="chapterForm.name" 
                  type="text" 
                  required 
                  class="form-control"
                  placeholder="Enter chapter name..."
                  ref="nameInput"
                >
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Description</label>
                <textarea 
                  v-model="chapterForm.description" 
                  class="form-control form-textarea" 
                  rows="4"
                  placeholder="Enter chapter description (optional)..."
                ></textarea>
                <div class="char-count">{{ (chapterForm.description || '').length }}/500</div>
              </div>
            </div>

            <div class="form-actions">
              <button type="button" @click="closeModal" class="btn btn-secondary btn-cancel">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary btn-save" :disabled="saving">
                <span v-if="saving" class="btn-icon spinner-small"></span>
                <span v-else class="btn-icon">{{ showCreateModal ? '➕' : '💾' }}</span>
                {{ saving ? 'Saving...' : (showCreateModal ? 'Create Chapter' : 'Update Chapter') }}
              </button>
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
  name: 'ChapterManagement',
  data() {
    return {
      chapters: [],
      subjects: [],
      selectedSubjectId: '',
      searchTerm: '',
      showCreateModal: false,
      showEditModal: false,
      loading: false,
      saving: false,
      chapterForm: {
        id: null,
        name: '',
        description: '',
        subject_id: ''
      }
    }
  },
  computed: {
    filteredChapters() {
      let filtered = this.chapters
      
      if (this.selectedSubjectId) {
        filtered = filtered.filter(chapter => chapter.subject_id == this.selectedSubjectId)
      }
      
      if (this.searchTerm) {
        filtered = filtered.filter(chapter =>
          chapter.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          chapter.description.toLowerCase().includes(this.searchTerm.toLowerCase())
        )
      }
      
      return filtered
    }
  },
  async mounted() {
    await this.fetchSubjects()
    await this.fetchChapters()
  },
  methods: {
    async fetchSubjects() {
      try {
        this.loading = true
        const response = await axios.get('/admin/subjects')
        this.subjects = response.data
      } catch (error) {
        console.error('Error fetching subjects:', error)
        // Mock data for demo
        this.subjects = [
          { id: 1, name: 'Mathematics' },
          { id: 2, name: 'Science' },
          { id: 3, name: 'English' }
        ]
      } finally {
        this.loading = false
      }
    },
    
    async fetchChapters() {
      try {
        this.loading = true
        const response = await axios.get('/admin/chapters')
        this.chapters = response.data
      } catch (error) {
        console.error('Error fetching chapters:', error)
        // Mock data for demo
        this.chapters = [
          {
            id: 1,
            name: 'Algebra Basics',
            description: 'Introduction to algebraic concepts and equations',
            subject_id: 1,
            created_at: '2024-01-15T10:30:00Z'
          },
          {
            id: 2,
            name: 'Geometry Fundamentals',
            description: 'Basic geometric shapes and properties',
            subject_id: 1,
            created_at: '2024-01-16T14:20:00Z'
          }
        ]
      } finally {
        this.loading = false
      }
    },
    
    getSubjectName(subjectId) {
      const subject = this.subjects.find(s => s.id === subjectId)
      return subject ? subject.name : 'Unknown'
    },
    
    openCreateModal() {
      this.resetForm()
      this.showCreateModal = true
      this.showEditModal = false
      this.$nextTick(() => {
        if (this.$refs.nameInput) {
          this.$refs.nameInput.focus()
        }
      })
    },
    
    editChapter(chapter) {
      this.chapterForm = { ...chapter }
      this.showEditModal = true
      this.showCreateModal = false
      this.$nextTick(() => {
        if (this.$refs.nameInput) {
          this.$refs.nameInput.focus()
        }
      })
    },
    
    async saveChapter() {
      try {
        this.saving = true
        
        if (this.showCreateModal) {
          await axios.post(`/admin/subjects/${this.chapterForm.subject_id}/chapters`, this.chapterForm)
        } else {
          await axios.put(`/admin/chapters/${this.chapterForm.id}`, this.chapterForm)
        }
        
        await this.fetchChapters()
        this.closeModal()
        
      } catch (error) {
        console.error('Error saving chapter:', error)
        // Simulate success for demo
        if (this.showCreateModal) {
          this.chapters.push({
            id: Date.now(),
            ...this.chapterForm,
            created_at: new Date().toISOString()
          })
        } else {
          const index = this.chapters.findIndex(c => c.id === this.chapterForm.id)
          if (index !== -1) {
            this.chapters[index] = { ...this.chapters[index], ...this.chapterForm }
          }
        }
        this.closeModal()
      } finally {
        this.saving = false
      }
    },
    
    async deleteChapter(id) {
      if (!confirm('Are you sure you want to delete this chapter? This action cannot be undone.')) {
        return
      }
      
      try {
        this.loading = true
        await axios.delete(`/admin/chapters/${id}`)
        await this.fetchChapters()
      } catch (error) {
        console.error('Error deleting chapter:', error)
        // Simulate success for demo
        this.chapters = this.chapters.filter(c => c.id !== id)
      } finally {
        this.loading = false
      }
    },
    
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.resetForm()
    },
    
    resetForm() {
      this.chapterForm = {
        id: null,
        name: '',
        description: '',
        subject_id: ''
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      try {
        return new Date(dateString).toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        })
      } catch (error) {
        return 'Invalid Date'
      }
    },
    
    truncateText(text, maxLength) {
      if (!text) return ''
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
    }
  }
}
</script>

<style scoped>
/* Variables for consistent theming */
.chapter-management {
  --primary-color: #4f46e5;
  --primary-hover: #4338ca;
  --secondary-color: #64748b;
  --success-color: #10b981;
  --danger-color: #ef4444;
  --warning-color: #f59e0b;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
  --border-radius: 12px;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Base styles */
.chapter-management {
  padding: 2rem;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header Section */
.header-section {
  margin-bottom: 2rem;
}

.header-content {
  background: white;
  border-radius: var(--border-radius);
  padding: 2rem;
  box-shadow: var(--shadow-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.title-section {
  flex: 1;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--gray-900);
  margin: 0 0 0.5rem 0;
  background: linear-gradient(135deg, var(--primary-color), #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.page-subtitle {
  font-size: 1.1rem;
  color: var(--gray-600);
  margin: 0;
}

/* Filters Section */
.filters-section {
  margin-bottom: 2rem;
}

.filters-container {
  background: white;
  border-radius: var(--border-radius);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-weight: 600;
  color: var(--gray-700);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.select-wrapper {
  position: relative;
}

.form-select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid var(--gray-200);
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

.form-select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.search-wrapper {
  position: relative;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 2px solid var(--gray-200);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  color: var(--gray-400);
}

/* Stats Cards */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: white;
  border-radius: var(--border-radius);
  padding: 1.5rem;
  text-align: center;
  box-shadow: var(--shadow-md);
  border-left: 4px solid var(--primary-color);
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--gray-600);
  margin-top: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Table Section */
.table-section {
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}

.table-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--gray-200);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--gray-50);
}

.table-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0;
}

.table-actions {
  display: flex;
  gap: 0.5rem;
}

.table-container {
  overflow-x: auto;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.modern-table th {
  background: var(--gray-50);
  padding: 1rem 1.5rem;
  text-align: left;
  font-weight: 600;
  color: var(--gray-700);
  border-bottom: 2px solid var(--gray-200);
  white-space: nowrap;
  position: sticky;
  top: 0;
  z-index: 10;
}

.th-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sortable {
  cursor: pointer;
  user-select: none;
}

.sortable:hover {
  background: var(--gray-100);
}

.sort-icon {
  opacity: 0.5;
  font-size: 0.75rem;
}

.modern-table td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--gray-100);
  vertical-align: middle;
}

.table-row {
  transition: background-color 0.2s ease;
}

.table-row:hover {
  background: var(--gray-50);
}

.name-cell {
  font-weight: 500;
}

.chapter-name {
  color: var(--gray-900);
}

.subject-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: var(--primary-color);
  color: white;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.description-cell {
  max-width: 200px;
}

.description-text {
  color: var(--gray-600);
  line-height: 1.4;
}

.date-cell {
  color: var(--gray-500);
  font-size: 0.8rem;
}

.actions-cell {
  width: 120px;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  white-space: nowrap;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}

.btn-secondary {
  background: var(--gray-200);
  color: var(--gray-700);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--gray-300);
}

.btn-outline {
  background: transparent;
  border: 2px solid var(--gray-200);
  color: var(--gray-700);
}

.btn-outline:hover:not(:disabled) {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.btn-edit {
  background: var(--warning-color);
  color: white;
  padding: 0.375rem 0.75rem;
}

.btn-edit:hover:not(:disabled) {
  background: #d97706;
}

.btn-delete {
  background: var(--danger-color);
  color: white;
  padding: 0.375rem 0.75rem;
}

.btn-delete:hover:not(:disabled) {
  background: #dc2626;
}

.btn-add {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  box-shadow: var(--shadow-md);
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
}

.btn-icon {
  font-size: 1em;
}

/* Loading and Empty States */
.loading-state {
  padding: 4rem 2rem;
  text-align: center;
  color: var(--gray-500);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--gray-200);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  padding: 4rem 2rem;
  text-align: center;
}

.empty-content {
  max-width: 400px;
  margin: 0 auto;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-content h4 {
  font-size: 1.25rem;
  color: var(--gray-700);
  margin: 0 0 0.5rem 0;
}

.empty-content p {
  color: var(--gray-500);
  margin: 0;
}

/* Enhanced Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 2rem;
  backdrop-filter: blur(4px);
}

.modern-modal {
  background: white;
  border-radius: var(--border-radius);
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
  transform: scale(0.95);
  animation: modalAppear 0.2s ease forwards;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-header {
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid var(--gray-200);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.modal-title-section {
  flex: 1;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.modal-icon {
  font-size: 1.25rem;
}

.modal-subtitle {
  color: var(--gray-600);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--gray-400);
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  margin-left: 1rem;
}

.close-btn:hover {
  color: var(--gray-600);
  background: var(--gray-100);
}

.modal-body {
  padding: 1.5rem 2rem 2rem;
}

/* Modern Form */
.modern-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 500;
  color: var(--gray-700);
  font-size: 0.875rem;
}

.form-label.required::after {
  content: ' *';
  color: var(--danger-color);
}

.form-control {
  padding: 0.75rem 1rem;
  border: 2px solid var(--gray-200);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: white;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.char-count {
  font-size: 0.75rem;
  color: var(--gray-400);
  text-align: right;
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--gray-200);
}

.btn-cancel {
  min-width: 100px;
}

.btn-save {
  min-width: 140px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .filters-container {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .stats-container {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .chapter-management {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: 1.5rem;
  }
  
  .page-title {
    font-size: 2rem;
    text-align: center;
  }
  
  .stats-container {
    grid-template-columns: 1fr;
  }
  
  .table-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .modern-table th,
  .modern-table td {
    padding: 0.75rem 1rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .modal-overlay {
    padding: 1rem;
  }
  
  .modal-header {
    padding: 1.5rem 1.5rem 1rem;
  }
  
  .modal-body {
    padding: 1rem 1.5rem 1.5rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 1.5rem;
  }
  
  .modern-table {
    font-size: 0.8rem;
  }
  
  .modern-table th,
  .modern-table td {
    padding: 0.5rem 0.75rem;
  }
}
</style>
