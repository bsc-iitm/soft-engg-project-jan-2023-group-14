<template>
    <div>
      <StudentNavbar :id_="3"></StudentNavbar>
      <h1>This is student my tickets page</h1>
      
    </div>
</template>

<script>
import StudentNavbar from '../components/StudentNavbar.vue';


export default {
  name: 'StudentMyTickets',
  components: {StudentNavbar},
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
