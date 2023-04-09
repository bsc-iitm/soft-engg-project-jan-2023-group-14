<template>
    <div>
      <UserNavbar :id_="4"></UserNavbar>
      <h1>This is support home page</h1>
      
    </div>
</template>

<script>
import UserNavbar from '../components/UserNavbar.vue';


export default {
  name: 'SupportHome',
  components: {UserNavbar},
  data() {
    return {
    };
  },
  mounted() {},
  methods: {
    
  },
  computed: {},
};
</script>

<style>


</style>
