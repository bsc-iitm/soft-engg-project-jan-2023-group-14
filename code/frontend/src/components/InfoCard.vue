<template>
  <div class="info-card-container">
      <b-card :title="value" :sub-title="title" bg-variant="light" class="text-center">
    </b-card>
  </div>
</template>

<script>
export default {
  name: "InfoCard",
  props: ["title", "value"],
  components: {},
  data() {
    return {};
  },
  created(){
    console.log('info card value: ', this.title, this.value);

  },
  mounted() {},
  methods: {},
  computed: {},
};
</script>

<style scoped>
.info-card-container {
  box-shadow: 2px 4px 5px 5px #dbdada;
  /* background-color: rgb(251, 252, 252); */
  margin: 12px 15px;
  /* padding: 10px; */
}
/* .info-card-container:hover {
  box-shadow: 5px 8px 8px 10px #888888;
   background-color: rgb(255, 255, 255); 
} */
</style>
