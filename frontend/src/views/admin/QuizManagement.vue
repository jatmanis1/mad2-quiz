<template>
  <div class="container py-4 quiz-management">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3 mb-0">Quiz Management</h1>
      <button class="btn btn-primary" @click="openCreate">➕ Add Quiz</button>
    </div>

    <!-- Filters -->
    <div class="row g-2 mb-3">
      <div class="col-md-3">
        <select 
          class="form-select"
          v-model="selectedSubjectId"
          @change="onSubjectChange"
        >
          <option value="">All Subjects</option>
          <option v-for="s in subjects" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>
      </div>
      <div class="col-md-3">
        <select 
          class="form-select"
          v-model="selectedChapterId"
          @change="fetchQuizzes"
        >
          <option value="">All Chapters</option>
          <option v-for="c in filteredChapters" :key="c.id" :value="c.id">
            {{ c.name }}
          </option>
        </select>
      </div>
      <div class="col-md-3">
        <input 
          class="form-control" 
          v-model="searchTerm"
          placeholder="Search quizzes…"
        />
      </div>
    </div>

    <!-- Table -->
    <div class="table-responsive mb-4">
      <table class="table table-hover align-middle shadow-sm">
        <thead class="table-light">
          <tr>
            <th scope="col">Title</th>
            <th scope="col">Chapter</th>
            <th scope="col">Quiz Date</th>
            <th scope="col">Duration</th>
            <th scope="col">Total Marks</th>
            <th scope="col">Questions</th>
            <th scope="col" style="width:150px">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="quiz in filteredQuizzes" :key="quiz.id">
            <td>{{ quiz.title }}</td>
            <td>{{ getChapterName(quiz.chapter_id) }}</td>
            <td>{{ formatDate(quiz.date_of_quiz) }}</td>
            <td>{{ quiz.time_duration }} min</td>
            <td>{{ quiz.total_marks }}</td>
            <td>
              <button class="btn btn-sm btn-info text-white" @click="manageQuestions(quiz)">
                Manage ({{ quiz.question_count || 0 }})
              </button>
            </td>
            <td>
              <button @click="openEdit(quiz)" class="btn btn-sm btn-secondary me-1">Edit</button>
              <button @click="deleteQuiz(quiz.id)" class="btn btn-sm btn-danger">Delete</button>
            </td>
          </tr>
          <tr v-if="filteredQuizzes.length===0">
            <td colspan="7" class="text-center text-muted py-4">No quizzes found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <form @submit.prevent="saveQuiz">
            <div class="modal-header">
              <h5 class="modal-title">{{ isEdit ? 'Edit Quiz' : 'Create Quiz' }}</h5>
              <button type="button" class="btn-close" @click="close"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Chapter *</label>
                <select v-model="quizForm.chapter_id" required class="form-select">
                  <option value="">Select chapter</option>
                  <option v-for="c in chapters" :key="c.id" :value="c.id">
                    {{ getSubjectName(c.subject_id) }} – {{ c.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Title *</label>
                <input v-model="quizForm.title" required class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="quizForm.description" class="form-control" rows="3"></textarea>
              </div>
              <div class="row g-2">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Date & time *</label>
                  <input type="datetime-local"
                         v-model="quizForm.date_of_quiz"
                         required
                         class="form-control" />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Duration (min) *</label>
                  <input type="number"
                         v-model="quizForm.time_duration"
                         min="1"
                         required
                         class="form-control" />
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" @click="close" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">{{ isEdit ? 'Update' : 'Create' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Manage Questions Modal (large) -->
    <div v-if="showQuestions" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Manage Questions – {{ selectedQuiz && selectedQuiz.title }}</h5>
            <button type="button" class="btn-close" @click="closeQuestions"></button>
          </div>
          <div class="modal-body">
            <!-- Add Question Form -->
            <div class="bg-light rounded p-3 mb-3">
              <form @submit.prevent="addQuestion" class="row g-2 align-items-end">
                <div class="col-12 mb-2">
                  <label class="form-label">Question Statement *</label>
                  <textarea v-model="questionForm.question_statement" required class="form-control" rows="2"></textarea>
                </div>
                <div class="col-md-3" v-for="i in 4" :key="i">
                  <label class="form-label">Option {{ i }} *</label>
                  <input v-model="questionForm[`option${i}`]" required class="form-control"/>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Correct Option *</label>
                  <select v-model="questionForm.correct_option" required class="form-select">
                    <option value="">Choose...</option>
                    <option v-for="i in 4" :value="i" :key="i">Option {{ i }}</option>
                  </select>
                </div>
                <div class="col-md-2">
                  <label class="form-label">Marks</label>
                  <input v-model="questionForm.marks" type="number" min="1" class="form-control" />
                </div>
                <div class="col-md-2">
                  <button type="submit" class="btn btn-primary w-100 mt-3">Add</button>
                </div>
              </form>
            </div>
            <!-- Questions listing -->
            <div>
              <h6 class="mb-2">Questions <span class="badge bg-primary">{{ questions.length }}</span></h6>
              <div v-if="questions.length === 0" class="alert alert-secondary text-center">No questions yet.</div>
              <div v-else>
                <div v-for="(q,idx) in questions" :key="q.id" class="border rounded p-3 mb-2">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <strong>Q{{ idx+1 }}. {{ q.question_statement }}</strong>
                    <span>
                      <span class="badge bg-success me-2">{{ q.marks }} marks</span>
                      <button @click="deleteQuestion(q.id)" class="btn btn-sm btn-danger">Delete</button>
                    </span>
                  </div>
                  <ul class="list-unstyled ms-3">
                    <li v-for="i in 4" :key="i" :class="{'fw-bold text-success': q.correct_option == i}">
                      {{ i }}. {{ q[`option${i}`] }}
                      <span v-if="q.correct_option == i" class="ms-1">✓</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const quizzes      = ref([])
const subjects     = ref([])
const chapters     = ref([])
const questions    = ref([])
const searchTerm   = ref('')
const selectedSubjectId = ref('')
const selectedChapterId = ref('')
const showModal = ref(false)
const isEdit    = ref(false)
const showQuestions = ref(false)
const quizForm = ref({
  id:null, title:'', description:'', chapter_id:'', date_of_quiz:'', time_duration:60
})
const questionForm = ref({
  question_statement:'', option1:'', option2:'', option3:'', option4:'',
  correct_option:'', marks:1
})
const selectedQuiz = ref(null)

const filteredChapters = computed(() =>
  selectedSubjectId.value
    ? chapters.value.filter(c => c.subject_id == selectedSubjectId.value)
    : chapters.value
)

const filteredQuizzes = computed(() => {
  let list = quizzes.value
  if (selectedChapterId.value)  list = list.filter(q => q.chapter_id == selectedChapterId.value)
  if (searchTerm.value)
    list = list.filter(q => q.title.toLowerCase().includes(searchTerm.value.toLowerCase()))
  return list
})

onMounted(async () => {
  await fetchSubjects(); await fetchChapters(); await fetchQuizzes()
})

async function fetchSubjects(){ try{subjects.value=(await axios.get('/admin/subjects')).data}catch(e){console.error(e)} }
async function fetchChapters(){ try{chapters.value=(await axios.get('/admin/chapters')).data}catch(e){console.error(e)} }
async function fetchQuizzes (){ try{quizzes.value=(await axios.get('/admin/quizzes')).data}catch(e){console.error(e)} }

function getSubjectName(id){ const s=subjects.value.find(x=>x.id===id);return s?s.name:'—' }
function getChapterName(id){ const c=chapters.value.find(x=>x.id===id);return c?c.name:'—' }

function openCreate(){ resetQuizForm(); isEdit.value=false; showModal.value=true }
function openEdit(q){ quizForm.value={...q}; isEdit.value=true; showModal.value=true }
function close(){ showModal.value=false; resetQuizForm() }
function resetQuizForm(){
  quizForm.value={ id:null, title:'', description:'', chapter_id:'', date_of_quiz:'', time_duration:60 }
}
async function saveQuiz(){ try{ if(isEdit.value){ await axios.put(`/admin/quizzes/${quizForm.value.id}`, quizForm.value) }else{ await axios.post('/admin/quizzes', quizForm.value) } }catch(e){console.error(e)} close() }
async function deleteQuiz(id){ if(!confirm('Delete?'))return; try{ await axios.delete(`/admin/quizzes/${id}`) }catch(e){ console.error(e) } fetchQuizzes() }
function onSubjectChange(){ selectedChapterId.value=''; fetchQuizzes() }
async function manageQuestions(q){ selectedQuiz.value=q; showQuestions.value=true; await fetchQuestions(q.id) }
function closeQuestions(){ showQuestions.value=false; selectedQuiz.value=null; questions.value=[]; resetQuestionForm() }
async function fetchQuestions(id){ try{questions.value=(await axios.get(`/admin/quizzes/${id}/questions`)).data}catch(e){console.error(e)} }
async function addQuestion(){ try{ await axios.post(`/admin/quizzes/${selectedQuiz.value.id}/questions`, questionForm.value) }catch(e){console.error(e)} resetQuestionForm() }
async function deleteQuestion(id){ if(!confirm('Delete this question?')) return; try{ await axios.delete(`/admin/questions/${id}`) }catch(e){ console.error(e) } fetchQuestions(selectedQuiz.value.id) }
function resetQuestionForm(){ questionForm.value={ question_statement:'', option1:'', option2:'', option3:'', option4:'', correct_option:'', marks:1 } }
function formatDate(d){ return d?new Date(d).toLocaleDateString():'' }
</script>

<style scoped>
.quiz-management .modal { display:block !important; background: transparent; }
.quiz-management .modal.fade { transition: opacity 0.2s; }
.quiz-management .modal .modal-dialog { max-width: 600px; }
.quiz-management .modal .modal-content { border-radius:10px; box-shadow:0 8px 32px rgba(0,0,0,0.14); }
.quiz-management .btn-info { background:#17a2b8; border-color:#17a2b8; }
.quiz-management .btn-info:hover,.quiz-management .btn-info:focus { background:#138496;border-color:#117a8b; }
.quiz-management .table { border-radius: 8px; overflow: hidden; }
.quiz-management .questions-list .question-item { background: #f8f9fa; }
.quiz-management .questions-list .fw-bold.text-success { text-shadow:0 0 0.2em #2dd88122; }
</style>
