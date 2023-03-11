<template>
  <div style="margin-top: 3%; margin-left: 3%; text-align: left">
    <h1 style="text-align: center">Welcome to Online Support Ticket System</h1>
    <div class="register-form">
      <h3 style="text-align: left">Register</h3>
      <br />
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group
          ><b-form-input
            id="input-first-name"
            v-model="form.first_name"
            type="text"
            placeholder="Enter first name"
            :state="check_name"
            aria-describedby="input-live-feedback-first-name"
            required
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback-first-name">
            Enter at least 3 letters of first name
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group
          ><b-form-input
            id="input-last-name"
            v-model="form.last_name"
            type="text"
            placeholder="Enter last name (Optional)"
          ></b-form-input
        ></b-form-group>

        <b-form-group label="Select role:" v-slot="{ ariaDescribedby }">
          <b-form-radio-group
            id="radio-group-role"
            v-model="form.role"
            :options="role_options"
            :aria-describedby="ariaDescribedby"
            name="radio-group-role"
          ></b-form-radio-group>
        </b-form-group>

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
            :state="check_password"
            aria-describedby="input-live-feedback-password"
            required
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback-password">
            Password should contain letters A-Z a-z and numbers 0-9 only and should be atleast 4 and
            atmost 8 characters long.
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group
          ><b-form-input
            id="input-retype-password"
            v-model="form.retype_password"
            placeholder="Retype password"
            type="password"
            :state="check_retype_password"
            aria-describedby="input-live-feedback-retype-password"
            required
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback-retype-password">
            Password did not match.
          </b-form-invalid-feedback>
        </b-form-group>

        <br />
        <b-button style="margin: 10px" type="submit" variant="primary">Submit</b-button>
        <b-button style="margin: 10px" type="reset" variant="danger">Reset</b-button>
      </b-form>
      <br />
      <b-link href="/login">Already registered? Please login here.</b-link>

      <b-card class="mt-3" header="Form Data : Temporary">
        <pre class="m-0">{{ form }}</pre>
      </b-card>
    </div>
  </div>
</template>

<script>
export default {
  name: "RegisterView",
  components: {},
  data() {
    return {
      role_options: [
        { text: "Student", value: "student" },
        { text: "Support", value: "support" },
        { text: "Admin", value: "admin" },
      ],
      form: {
        first_name: "",
        last_name: "",
        role: "student",
        email: "",
        password: "",
        retype_password: "",
      },
      show: true,
    };
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      alert(JSON.stringify(this.form));
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.form.first_name = "";
      this.form.last_name = "";
      this.form.email = "";
      this.form.password = "";
      this.form.retype_password = "";
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
  computed: {
    check_name() {
      return this.form.first_name.length > 2 ? true : false;
    },
    check_password() {
      console.log('inside check password');
      let password = this.form.password;
      if (password.length < 4 || password.length > 9) {
        return false;
      }
      const valid_char_array = Array.from(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
      );
      const password_array = Array.from(password);
      for (let i = 0; i < password_array.length; i++) {
        if (!valid_char_array.includes(password_array[i])) {
          return false;
        }
      }
      return true;
    },
    check_retype_password() {
      return this.form.password === this.form.retype_password ? true : false;
    },
  },
};
</script>

<style>
.register-form {
  width: 50%;
  margin: 5%;
}
</style>
