import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: {
      user_id: "",
      role: "",
      first_name: "",
      last_name: "",
      email: "",
      profile_pic: "",
    },
    web_token: "",
    token_expiry_on: 0,
    logged_status: false,
  },
  getters: {
    get_user: function (state) {
      return state.user
    },
    get_user_id: function (state) {
      return state.user.user_id
    },
    get_user_role: function (state) {
      return state.user.role
    },
    get_web_token: function (state) {
      return state.web_token
    },
    get_token_expiry_on: function (state) {
      return state.token_expiry_on
    },
    get_logged_status: function (state) {
      return state.logged_status
    },

  },
  mutations: {
    initialiseStore(state) {
      // Check if the ID exists
      if (localStorage.getItem('store')) {
        console.log('App creating. Store available in local storage');
        // Replace the state object with the stored item
        this.replaceState(
          Object.assign(state, JSON.parse(localStorage.getItem('store')))
        );
      }
    },
    SET_STATE_AFTER_LOGIN(state, payload){
      state.user.user_id = payload.user_id;
      state.user.role = payload.role;
      state.web_token = payload.web_token;
      state.token_expiry_on = payload.token_expiry_on;
      state.logged_status = true;
    },
    SET_STATE_AFTER_LOGOUT(state, payload){
      state.user.user_id = "";
      state.user.role = "";
      state.web_token = "";
      state.token_expiry_on = 0;
      state.logged_status = false;
    }
  },
  actions: {
    set_state_after_login(context, payload) {
      context.commit('SET_STATE_AFTER_LOGIN', payload);
    },
    set_state_after_logout(context, payload) {
      context.commit('SET_STATE_AFTER_LOGOUT', payload);
    }
  },
  modules: {
  },
});
