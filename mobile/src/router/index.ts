import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import TabsPage from '../views/TabsPage.vue';
import { useAuthStore } from '../stores/auth';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/tabs/home'
  },
  {
    path: '/login',
    component: () => import('../views/LoginPage.vue')
  },
  {
    path: '/register',
    component: () => import('../views/RegisterPage.vue')
  },
  {
    path: '/forgot-password',
    component: () => import('../views/ForgotPasswordPage.vue')
  },
  {
    path: '/tabs/',
    component: TabsPage,
    children: [
      {
        path: '',
        redirect: '/tabs/home'
      },
      {
        path: 'home',
        component: () => import('../views/DashboardPage.vue')
      },
      {
        path: 'events',
        component: () => import('../views/EventsPage.vue')
      },
      {
        path: 'events/:id',
        component: () => import('../views/EventDetailPage.vue')
      },
      {
        path: 'inscriptions',
        component: () => import('../views/MyInscriptionsPage.vue')
      },
      {
        path: 'schedule',
        component: () => import('../views/SchedulePage.vue')
      },
      {
        path: 'profile',
        component: () => import('../views/ProfilePage.vue')
      },
      {
        path: 'submissions',
        component: () => import('../views/MySubmissionsPage.vue')
      }
    ]
  },
  {
    path: '/events/create',
    component: () => import('../views/CreateEventPage.vue')
  },
  {
    path: '/events/:id/edit',
    component: () => import('../views/EditEventPage.vue')
  },
  {
    path: '/events/:id/manage-schedule',
    component: () => import('../views/ManageSchedulePage.vue')
  },
  {
    path: '/events/:id/submit',
    component: () => import('../views/SubmissionFormPage.vue')
  },
  {
    path: '/manage-turmas',
    component: () => import('../views/ManageTurmasPage.vue')
  },
  {
    path: '/my-organized-events',
    component: () => import('../views/MyOrganizedEventsPage.vue')
  },
  {
    path: '/privacy-policy',
    component: () => import('../views/PrivacyPolicyPage.vue')
  },
  {
    path: '/terms-of-use',
    component: () => import('../views/TermsOfUsePage.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const publicPages = ['/login', '/register', '/forgot-password'];
  const authRequired = !publicPages.includes(to.path);

  if (authRequired && !authStore.isAuthenticated) {
    return next('/login');
  }

  if (to.path === '/login' && authStore.isAuthenticated) {
    return next('/tabs/events');
  }

  next();
});

export default router
