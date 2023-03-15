<template>
  <div class="login-form">
    <div style="margin: 3%; padding: 3%; width: 50%">
      <h3 style="text-align: left">Login</h3>
      <br />
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group
          ><b-form-input
            id="input-email"
            v-model="form.email"
            type="email"
            placeholder="Enter email"
            required
          ></b-form-input
        ></b-form-group>

        <b-form-group
          ><b-form-input
            id="input-password"
            v-model="form.password"
            placeholder="Enter password"
            type="password"
            required
          ></b-form-input
        ></b-form-group>
        <br />
        <b-button style="margin: 10px" type="submit" variant="primary">Submit</b-button>
        <b-button style="margin: 10px" type="reset" variant="danger">Reset</b-button>
      </b-form>
      <br />
      
       <p>New user? Please <b-link href="/register">Register here</b-link> </p>
       <p>Go to <b-link href="/home">Home Page</b-link> </p>
    </div>
  </div>
</template>

<script>
import * as common from "../assets/common.js";
// import TicketCard from "../components/TicketCard.vue";

export default {
  name: "LoginView",
  components: {},
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      show: true,
    };
  },
  methods: {
    onSubmit: async function (event) {
      event.preventDefault();
      this.$log.info("Submitting login form");

      fetch(common.AUTH_API_LOGIN, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.form),
      })
        .then((response) => response.json())
        .then((data) => {
          this.$log.debug(`Success : ${data}`);
          if (data.category == "success") {
            this.flashMessage.success({
              message: "Successfully logged in.",
            });
            console.log(JSON.stringify(data));

            // update store
            this.$store.dispatch("set_state_after_login", data.message);

            console.log("State after setting user: ", JSON.stringify(this.$store.state));

            this.$router.push(`/${data.message.role}-home`); //home page depends on role
          }
          if (data.category == "error") {
            this.flashMessage.error({
              message: data.message,
            });
          }
        })
        .catch((error) => {
          this.$log.debug(`Error : ${error}`);
          this.flashMessage.error({
            message: "Internal Server Error",
          });
        });
    },
    onReset(event) {
      event.preventDefault();
      this.form.email = "";
      this.form.password = "";
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
};
</script>

<style>
/* .login-div {
   margin-top: 5%; 
  margin-left: 10%; 
  margin-right: 5%;  
  text-align: "left";
  height: 100vh;
  background-color:  #D9AFD9;
  background-image: linear-gradient(0deg, #D9AFD9 0%, #97D9E1 100%);

} */

/*
.login-form {
   box-shadow: 2px 4px 5px 5px #dbdada; 
  width: 50%;
  padding-top: 5%; 
  margin-left: 10%; 
  margin-right: 5%;
  background-color: rgb(224, 223, 223);
  margin: 12px 5px;
}
*/
/*
.login-form:hover {
   box-shadow: 5px 8px 8px 10px #888888; 
  background-color: rgb(255, 255, 255);
}
*/
</style>
