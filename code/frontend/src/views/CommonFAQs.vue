<template>
  <div>
    <UserNavbar :id_="id_"></UserNavbar>

    <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="12" md="12">
          <h3 style="text-align: center">Frequently Asked Questions</h3>
          <div style="height: 550px; overflow: auto; padding: 10px">
            <div v-for="faq in faq_card_details" :key="faq.faq_id">
              <FAQCard :faq_id="faq.faq_id" :question="faq.question" :answer="faq.solution"></FAQCard>
            </div>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>

import UserNavbar from "../components/UserNavbar.vue";
import * as common from "../assets/common.js";
import FAQCard from "../components/FAQCard.vue";

export default {
  name: "CommonFAQs",
  components: { UserNavbar, FAQCard },
  data() {
    return {
      id_: "",
      user_id: this.$store.getters.get_user_id,
      faq_card_details: [],
    };
  },
  created() {
    let user_role = this.$store.getters.get_user_role;
    if (user_role == "student") {
      this.id_ = 4;
    }
    if (user_role == "support") {
      this.id_ = 4; // need to be updated
    }
    if (user_role == "admin") {
      this.id_ = 4; // need to be updated
    }
    let form = {
      filter_status: ["pending"],
    };
    let params = "";
    params = new URLSearchParams(form).toString();
    console.log("params: ", params);

    fetch(common.FAQ_API, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        web_token: this.$store.getters.get_web_token,
        user_id: this.user_id,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        this.$log.debug(`Success : ${data}`);
        // console.log(data)
        if (data.category == "success") {
          this.flashMessage.success({
            message: "FAQs retrieved.",
          });
          console.log(data)
          this.faq_card_details = data.message;
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
  mounted() {},
  methods: {},
  computed: {},
};
</script>

<style></style>
