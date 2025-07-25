import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

// Import components
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminDashboard from '../views/admin/Dashboard.vue'
import UserDashboard from '../views/user/Dashboard.vue'
import QuizList from '../views/user/QuizList.vue'
import TakeQuiz from '../views/user/TakeQuiz.vue'
import QuizResults from '../views/user/QuizResults.vue'
import SubjectManagement from '../views/admin/SubjectManagement.vue'
import ChapterManagement from '../views/admin/ChapterManagement.vue'
import QuizManagement from '../views/admin/QuizManagement.vue'

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
        path: '/admin',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/admin/subjects',
        name: 'SubjectManagement',
        component: SubjectManagement,
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/admin/chapters',
        name: 'ChapterManagement',
        component: ChapterManagement,
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/admin/quizzes',
        name: 'QuizManagement',
        component: QuizManagement,
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/dashboard',
        name: 'UserDashboard',
        component: UserDashboard,
        meta: { requiresAuth: true, role: 'user' }
    },
    {
        path: '/quizzes',
        name: 'QuizList',
        component: QuizList,
        meta: { role: 'user' }
    },
    {
        path: '/quiz/:quizId/take',
        name: 'TakeQuiz',
        component: TakeQuiz,
        meta: { requiresAuth: true, role: 'user' }
    },
    {
        path: '/quiz/results/:scoreId',
        name: 'QuizResults',
        component: QuizResults,
        meta: { requiresAuth: true, role: 'user' }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})
router.beforeEach((to, from, next) => {
    const isAuthenticated = store.getters.isAuthenticated
    const userRole = store.getters.userRole

    // Not authenticated and route requires login
    if (to.meta.requiresAuth && !isAuthenticated) {
        return next('/login')
    }

    // Authenticated but trying to access a role-restricted route
    if (to.meta.role && to.meta.role !== userRole) {
        // Prevent redirect loop
        if (userRole === 'admin' && to.path !== '/admin') {
            return next('/admin')
        }
        if (userRole === 'user' && to.path !== '/dashboard') {
            return next('/dashboard')
        }

        // Already at correct path; do nothing
        return next()
    }

    // All good
    return next()
})

export default router
