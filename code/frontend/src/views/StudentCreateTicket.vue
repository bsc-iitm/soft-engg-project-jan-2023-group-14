<template>
    <div>
      <StudentNavbar :id_="2"></StudentNavbar>

      <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="6" md="5" style="border-right: dashed black">
          <h2 style="text-align: center">Create Ticket</h2>
          <TicketForm></TicketForm>
        </b-col>
        <b-col cols="12" sm="6" md="7" >
          <h2 style="text-align: center">Search Tickets</h2>
          <SearchTicket></SearchTicket>
        </b-col>
      </b-row>
    </b-container>

    <br />
      
    </div>
</template>

<script>
import StudentNavbar from '../components/StudentNavbar.vue';
import TicketForm from '../components/TicketForm.vue';
import SearchTicket from '../components/SearchTicket.vue';


export default {
  name: 'StudentCreateTicket',
  components: {StudentNavbar, TicketForm, SearchTicket},
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
