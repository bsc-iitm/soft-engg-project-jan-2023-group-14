<template>
  <div id="app">
    <FlashMessage :position="'left bottom'" style="font-size: 15px" />
    <!-- <LoginView v-if="$route.name == 'login'"></LoginView> -->
    <!-- <FileUpload></FileUpload> -->
    <!-- <div style="width: 50%;"><TicketForm></TicketForm></div> -->
    <router-view />
  </div>
</template>

<script>
import LoginView from "./views/LoginView.vue";
import FileUpload from "./components/FileUpload.vue";
import TicketForm from './components/TicketForm.vue';

export default {
  components: { TicketForm },
  data() {
    return {};
  },
  beforeCreate() {
    console.log('Creating app.');
		this.$store.commit('initialiseStore');
	},
  mounted() {},
  methods: {},
  computed: {},
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: start;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #4dd325;
}

nav a.router-link-exact-active {
  color: #441ada;
}

.buttons {
  margin: 15px;
  justify-content: space-between;
}

#profile_pic {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-repeat: no-repeat;
  background-size: cover;
}

router-link {
  box-shadow: 5px 10px 8px 10px #888888;
  background-color: aqua;
}
</style>
