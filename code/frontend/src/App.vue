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
</style>
