<template>
    <div>
      <StudentNavbar :id_="4"></StudentNavbar>
      <h1>This is student faqs page</h1>
      
    </div>
</template>

<script>
import StudentNavbar from '../components/StudentNavbar.vue';


export default {
  name: 'StudentFAQs',
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
