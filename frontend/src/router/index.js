import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import Events from '../views/Events.vue'
import EventDetail from '../views/EventDetail.vue'
import CreateEvent from '../views/CreateEvent.vue'
import MyInscriptions from '../views/MyInscriptions.vue'
import MySubmissions from '../views/MySubmissions.vue'
import MyOrganizedEvents from '../views/MyOrganizedEvents.vue'
import TermsOfUse from '../views/TermsOfUse.vue'
import PrivacyPolicy from '../views/PrivacyPolicy.vue'
import SubmissionForm from '../views/SubmissionForm.vue'
import ManageSchedule from '../views/ManageSchedule.vue'
import EditEvent from '../views/EditEvent.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
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
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/events',
    name: 'Events',
    component: Events
  },
  {
    path: '/events/new',
    name: 'CreateEvent',
    component: CreateEvent,
    meta: { requiresAuth: true }
  },
  {
    path: '/events/:id',
    name: 'EventDetail',
    component: EventDetail,
    props: true
  },
  {
    path: '/events/:id/submit',
    name: 'SubmissionForm',
    component: SubmissionForm,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/events/:id/manage-schedule',
    name: 'ManageSchedule',
    component: ManageSchedule,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/my-inscriptions',
    name: 'MyInscriptions',
    component: MyInscriptions,
    meta: { requiresAuth: true }
  },
  {
    path: '/my-submissions',
    name: 'MySubmissions',
    component: MySubmissions,
    meta: { requiresAuth: true }
  },
  {
    path: '/my-organized-events',
    name: 'MyOrganizedEvents',
    component: MyOrganizedEvents,
    meta: { requiresAuth: true }
  },
  {
    path: '/termos-de-uso',
    name: 'TermsOfUse',
    component: TermsOfUse
  },
  {
    path: '/politica-de-privacidade',
    name: 'PrivacyPolicy',
    component: PrivacyPolicy
  },
  {
    path: '/events/:id/edit',
    name: 'EditEvent',
    component: EditEvent,
    props: true,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    try {
      // Check if user is authenticated by calling the API
      const response = await axios.get('/api/')
      if (response.data.authenticated) {
        next()
      } else {
        next('/login')
      }
    } catch (error) {
      next('/login')
    }
  } else {
    next()
  }
})

export default router