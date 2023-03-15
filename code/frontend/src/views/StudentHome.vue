<template>
  <div>
    <StudentNavbar :id_="1"></StudentNavbar>

    <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="7" md="8">
          <h2 style="text-align: center">My Unresolved Tickets</h2>
          <div style="height: 550px; overflow: auto; padding: 10px">
            <div v-for="ticket in ticket_card_details" :key="ticket.ticket_id">
              <TicketCard
                :ticket_id="ticket.ticket_id"
                :created_on="ticket.created_on"
                :title="ticket.title"
                :description="ticket.description"
                :votes="ticket.votes"
              ></TicketCard>
            </div>
          </div>
        </b-col>
        <b-col cols="12" sm="5" md="4" style="border: 1px solid red">
          <h2 style="text-align: center">My Activity</h2>
        </b-col>
      </b-row>
    </b-container>

    <br />
  </div>
</template>

<script>
import StudentNavbar from "../components/StudentNavbar.vue";

import * as common from "../assets/common.js";
import TicketCard from "../components/TicketCard.vue";

export default {
  name: "StudentHome",
  components: { StudentNavbar, TicketCard },
  data() {
    return {
      ticket_card_details: [
        {
          ticket_id: "1 Lorem Ipsum is simply dummy",
          created_on: 1669734650,
          title: "Lorem Ipsum is simply dummy Lorem Ipsum is simply dummy",
          description:
            "Lorem Ipsum is simply dummy Lorem Ipsum is simply dummyLorem Ipsum is simply dummy Lorem Ipsum is simply dummyLorem Ipsum is simply dummy Lorem Ipsum is simply dummy",
          votes: 5,
        },
        {
          ticket_id: "2 Lorem Ipsum is simply dummy",
          created_on: 1669734650,
          title: "Lorem Ipsum is simply dummy Lorem Ipsum is simply dummy",
          description:
            "Lorem Ipsum is simply dummy Lorem Ipsum is simply dummyLorem Ipsum is simply dummy Lorem Ipsum is simply dummyLorem Ipsum is simply dummy Lorem Ipsum is simply dummy",
          votes: 5,
        },
        {
          ticket_id: "3 Lorem Ipsum is simply dummy",
          created_on: 1669734650,
          title: "Lorem Ipsum is simply dummy Lorem Ipsum is simply dummy",
          description:
            "Lorem Ipsum is simply dummy Lorem Ipsum is simply dummyLorem Ipsum is simply dummy Lorem Ipsum is simply dummyLorem Ipsum is simply dummy Lorem Ipsum is simply dummy",
          votes: 5,
        },
        {
          ticket_id: "4 Lorem Ipsum is simply dummy",
          created_on: 1669734650,
          title: "Lorem Ipsum is simply dummy Lorem Ipsum is simply dummy",
          description:
            "Lorem Ipsum is simply dummy Lorem Ipsum is simply dummyLorem Ipsum is simply dummy Lorem Ipsum is simply dummyLorem Ipsum is simply dummy Lorem Ipsum is simply dummy",
          votes: 5,
        },
        {
          ticket_id: "5 Lorem Ipsum is simply dummy",
          created_on: 1669734650,
          title: "Lorem Ipsum is simply dummy Lorem Ipsum is simply dummy",
          description:
            "Lorem Ipsum is simply dummy Lorem Ipsum is simply dummyLorem Ipsum is simply dummy Lorem Ipsum is simply dummyLorem Ipsum is simply dummy Lorem Ipsum is simply dummy",
          votes: 5,
        },
        {
          ticket_id: "6 Lorem Ipsum is simply dummy",
          created_on: 1669734650,
          title: "Lorem Ipsum is simply dummy Lorem Ipsum is simply dummy",
          description:
            "Lorem Ipsum is simply dummy Lorem Ipsum is simply dummyLorem Ipsum is simply dummy Lorem Ipsum is simply dummyLorem Ipsum is simply dummy Lorem Ipsum is simply dummy",
          votes: 5,
        },
      ],
    };
  },
  mounted() {},
  methods: {},
  computed: {},
};
</script>

<style></style>
