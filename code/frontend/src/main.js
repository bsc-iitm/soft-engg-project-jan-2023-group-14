import BootstrapVue from 'bootstrap-vue';
import VueLogger from 'vuejs-logger';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import 'bootstrap/dist/css/bootstrap.css';

const isProduction = process.env.NODE_ENV === 'production';

Vue.config.productionTip = false;
Vue.prototype.$BASEURL = (Vue.config.productionTip) ? 'https://hostname' : 'http://127.0.0.1:5000';

const options = {
  isEnabled: true,
  logLevel: isProduction ? 'error' : 'debug',
  stringifyArguments: true,
  showLogLevel: false,
  showMethodName: false,
  separator: '|',
  showConsoleColors: true,
};

Vue.use(VueLogger, options); // logLevels:['debug', 'info', 'warn', 'error', 'fatal']
Vue.use(BootstrapVue);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');

store.subscribe((mutation, state) => {
  // cache store data
  localStorage.setItem('store', JSON.stringify(state));
});