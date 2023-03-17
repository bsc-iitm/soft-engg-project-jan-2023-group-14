<template>
    <div>
      <UserNavbar :id_="4"></UserNavbar>
      <h1>This is admin validate users page</h1>
      
    </div>
</template>

<script>
import UserNavbar from '../components/UserNavbar.vue';


export default {
  name: 'AdminValidateUsers',
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
