import Vue from 'vue';
import VueRouter from 'vue-router';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import store from '../store';
import * as common from "../assets/common.js";
// import TicketForm from '../components/TicketForm.vue';
// import SearchTicket from '../components/SearchTicket.vue';
import StudentHome from '../views/StudentHome.vue';
import StudentCreateTicket from '../views/StudentCreateTicket.vue';
import StudentMyTickets from '../views/StudentMyTickets.vue';
import CommonFAQs from '../views/CommonFAQs.vue';
// import StudentView from '../views/StudentView.vue';
// import SupportView from '../views/SupportView.vue';
// import AdminView from '../views/AdminView.vue';
import AppHomeView from '../views/AppHomeView.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    alias: '/home',
    name: 'AppHomeView',
    component: AppHomeView,
  },
  {
    path: '/login',
    name: 'LoginView',
    component: LoginView,
    // alias: '/',
  },
  {
    path: '/register',
    name: 'RegisterView',
    component: RegisterView,
  },
  {
    path: '/student-home',
    name: 'StudentHome',
    component: StudentHome,
  },
  {
    path: '/student-create-ticket',
    name: 'StudentCreateTicket',
    component: StudentCreateTicket,
  },
  {
    path: '/student-my-tickets',
    name: 'StudentMyTickets',
    component: StudentMyTickets,
  },
  {
    path: '/common-faqs',
    name: 'CommonFAQs',
    component: CommonFAQs,
  },
  {
    path: '*',
    redirect: '/',
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login', '/register', '/', '/home'];
  const authRequired = !publicPages.includes(to.path);
  if (!store.getters.get_logged_status) {
    store.commit('initialiseStore');
  }
  const logged_status = store.getters.get_logged_status;

  console.log('Routing', from.path, to.path, authRequired, logged_status);

  if (authRequired && !logged_status) {
    alert("Token expired. Please log in again.");
    return next('/login');
  }
  if (authRequired && logged_status) {
    const role = store.state.user.role;

    let accesing = "";
    if (common.STUDENT_ROUTES.includes(to.path)) { accesing = "student" }
    if (common.SUPPORT_ROUTES.includes(to.path)) { accesing = "support" }
    if (common.ADMIN_ROUTES.includes(to.path)) { accesing = "admin" }
    console.log('Checking role: ', role, to.path, accesing);
    if (role != accesing) {
      alert("You don't have access to this page.");
      return next(`/${role}-home`);
    }
  }
  next();
})


export default router;

// {
//   path: '/student',
//   name: 'StudentView',
//   component: StudentView,
// },
// {
//   path: '/support',
//   name: 'SupportView',
//   component: SupportView,
// },
// {
//   path: '/admin',
//   name: 'AdminView',
//   component: AdminView,
// },
