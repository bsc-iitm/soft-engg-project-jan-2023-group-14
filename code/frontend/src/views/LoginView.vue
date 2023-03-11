<template>
  <div style="margin-top: 3%; margin-left: 3%; text-align: left">
    <h1 style="text-align: center">Welcome to Online Support Ticket System</h1>
    
    <div class="login-form">
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
      <b-link href="/register">New user? Please Register here.</b-link>

      <b-card class="mt-3" header="Form Data : Temporary">
        <pre class="m-0">{{ form }}</pre>
      </b-card>
    </div>
  </div>
</template>

<script>
import * as common from "../assets/common.js";

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
      this.$log.info('Submitting login form');
      // alert('Do you want to login?');
      
      this.flashMessage.success({
        message: "Submitting login form",
      });

      
      // fetch(common.BASEURL + common.AUTH_API_PREFIX + "/login", {
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json",
      //   },
      //   body: JSON.stringify(this.form),
      // })
      //   .then((response) => response.json())
      //   .then((data) => {
      //     console.log("Success:", data);
      //     if (data.category == "success") {
      //       common.displayStatusSuccess(data.message);
      //       this.$router.push("/student_home");
      //     }
      //     if (data.category == "error") {
      //       common.displayStatusError(data.message);
      //     }
      //   })
      //   .catch((error) => {
      //     console.error("Error:", error);
      //     // common.displayStatusError('Internal Server Error');
      //     this.flash("Internal Server Error", "error");
      //   });
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
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
.login-form {
  width: 50%;
  margin: 5%;
}
</style>
