import { createRouter, createWebHistory } from 'vue-router';
import axios from 'axios';

const Home = () => import('../views/Home.vue');
const Login = () => import('../views/Login.vue');
const Register = () => import('../views/Register.vue');
const Dashboard = () => import('../views/Dashboard.vue');
const Events = () => import('../views/Events.vue');
const EventDetail = () => import('../views/EventDetail.vue');
const CreateEvent = () => import('../views/CreateEvent.vue');
const MyInscriptions = () => import('../views/MyInscriptions.vue');
const MySubmissions = () => import('../views/MySubmissions.vue');
const MyOrganizedEvents = () => import('../views/MyOrganizedEvents.vue');
const TermsOfUse = () => import('../views/TermsOfUse.vue');
const PrivacyPolicy = () => import('../views/PrivacyPolicy.vue');
const Profile = () => import('../views/Profile.vue');
const SubmissionForm = () => import('../views/SubmissionForm.vue');
const ManageSchedule = () => import('../views/ManageSchedule.vue');
const EditEvent = () => import('../views/EditEvent.vue');
const ForgotPassword = () => import('../views/ForgotPassword.vue');
const ResetPassword = () => import('../views/ResetPassword.vue');
const ManageTurmas = () => import('../views/ManageTurmas.vue');
const Calendar = () => import('../views/Calendar.vue');

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true },
  },
  {
    path: '/events',
    name: 'Events',
    component: Events,
  },
  {
    path: '/events/new',
    name: 'CreateEvent',
    component: CreateEvent,
    meta: { requiresAuth: true },
  },
  {
    path: '/events/:id',
    name: 'EventDetail',
    component: EventDetail,
    props: true,
  },
  {
    path: '/events/:id/submit',
    name: 'SubmissionForm',
    component: SubmissionForm,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/events/:id/manage-schedule',
    name: 'ManageSchedule',
    component: ManageSchedule,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/my-inscriptions',
    name: 'MyInscriptions',
    component: MyInscriptions,
    meta: { requiresAuth: true },
  },
  {
    path: '/my-submissions',
    name: 'MySubmissions',
    component: MySubmissions,
    meta: { requiresAuth: true },
  },
  {
    path: '/my-organized-events',
    name: 'MyOrganizedEvents',
    component: MyOrganizedEvents,
    meta: { requiresAuth: true },
  },
  {
    path: '/termos-de-uso',
    name: 'TermsOfUse',
    component: TermsOfUse,
  },
  {
    path: '/politica-de-privacidade',
    name: 'PrivacyPolicy',
    component: PrivacyPolicy,
  },
  {
    path: '/events/:id/edit',
    name: 'EditEvent',
    component: EditEvent,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword,
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: ResetPassword,
  },
  {
    path: '/manage-turmas',
    name: 'ManageTurmas',
    component: ManageTurmas,
    meta: { requiresAuth: true },
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: Calendar,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard
router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    try {
      // Check if user is authenticated by calling the API
      const response = await axios.get('/api/');
      if (response.data.authenticated) {
        next();
      } else {
        next('/login');
      }
    } catch (error) {
      next('/login');
    }
  } else {
    next();
  }
});

export default router;
