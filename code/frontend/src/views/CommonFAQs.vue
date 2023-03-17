<template>
  <div>
    <UserNavbar :id_="id_"></UserNavbar>

    <b-container fluid="xl">
      <b-row class="text-start">
        <b-col cols="12" sm="12" md="12">
          <h3 style="text-align: center">Frequently Asked Questions</h3>
          <div style="height: 550px; overflow: auto; padding: 10px">
            <div v-for="faq in faq_card_details" :key="faq.faq_id">
              <FAQCard :faq_id="faq.faq_id" :question="faq.question" :answer="faq.answer"></FAQCard>
            </div>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import FAQCard from "../components/FAQCard.vue";
import UserNavbar from "../components/UserNavbar.vue";

export default {
  name: "CommonFAQs",
  components: { UserNavbar, FAQCard },
  data() {
    return {
      id_: "",
      faq_card_details: [
        {
          faq_id: 1,
          question:
            "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the",
          answer:
            "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum",
        },
        {
          faq_id: 2,
          question: "Lorem Ipsum is simply dummy text of the printeen the.",
          answer:
            "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software",
        },
        {
          faq_id: 3,
          question:
            "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the",
          answer:
            "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop",
        },
      ],
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
  },
  mounted() {},
  methods: {},
  computed: {},
};
</script>

<style></style>
