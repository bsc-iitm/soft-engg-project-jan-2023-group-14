<template>
  <div>
    
    <b-container class="ticket-card-container">
      <!-- Stack the columns on mobile by making one full-width and the other half-width -->
      <b-row class="row">
        <b-col class="col" cols="12" lg="5" sm="12"><i>Id: </i>{{ ticket_id.slice(0,15) }}</b-col>
        <b-col class="col" cols="12" lg="5" sm="8"><i>Created On: </i>{{ created_on }}</b-col>
        <b-col class="col" cols="12" lg="2" sm="4"><i>Votes: </i>{{ votes }}</b-col>
      </b-row>
      <b-row class="row">
        <b-col class="col" cols="12" sm="10" lg="11">
          <b-row class="row">
            <b-col class="col" cols="12"><b>Title: </b>{{ title.slice(0, 80) }}</b-col>
          </b-row>
          <b-row class="row">
            <b-col class="col" cols="12"><b>Description: </b>{{ description.slice(0, 200) }}</b-col>
          </b-row>
        </b-col>
        <b-col class="col" cols="12" sm="2" lg="1">
          <b-row class="row">
            <b-col class="col" cols="4" sm="12" lg="12">
              <b-button href="#" variant="outline-light" size="sm" class="ticket-card-buttons"
                ><b-icon
                  icon="heart-fill"
                  aria-hidden="true"
                  class="bg-light"
                  variant="success"
                ></b-icon>
              </b-button>
            </b-col>

            <b-col class="col" cols="4" sm="12" lg="12"
              ><b-button href="#" variant="outline-light" size="sm" class="ticket-card-buttons"
              
                ><b-icon
                  icon="pencil-fill"
                  aria-hidden="true"
                  class="bg-light"
                  variant="primary"
                ></b-icon
              ></b-button>
            </b-col>

            <b-col class="col" cols="4" sm="12" lg="12"
              ><b-button href="#" variant="outline-light" size="sm" class="ticket-card-buttons"
                ><b-icon
                  icon="trash-fill"
                  aria-hidden="true"
                  class="bg-light"
                  variant="danger"
                ></b-icon></b-button
            ></b-col>
          </b-row>
        </b-col>
      </b-row>

      <!-- Columns start at 50% wide on mobile and bump up to 33.3% wide on desktop -->
    </b-container>
  </div>
</template>

<script>
export default {
  name: "TicketCard",
  props: ["ticket_id", "created_on", "title", "description", "votes"],
  components: {},
  data() {
    return {
      button_1_active: false,
    };
  },
  mounted() {},
  methods: {},
  computed: {},
};
</script>

<style scoped>
.ticket-card-container {
  /* border: 1px solid rgb(0, 0, 0); */
  box-shadow: 2px 4px 5px 5px #dbdada;
  background-color: rgb(251, 252, 252);
  margin: 12px 5px;
}
.ticket-card-container:hover {
  /* border: 1px solid rgb(0, 0, 0); */
  box-shadow: 5px 8px 8px 10px #888888;
  background-color: rgb(255, 255, 255);
}
.row {
  /* border: 1px solid rgb(0, 0, 255); */
  /* margin: 3px auto; */
  padding-top: 5px;
  padding-bottom: 5px;
}
/* .col {
  border: 1px solid red;
} */

.ticket-card-buttons {
  border-color: #ffffff;
  /* box-shadow: 3px 3px 8px 10px #888888; */
}
.ticket-card-buttons:hover {
  border-color: #95ddfa;
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
</style>
