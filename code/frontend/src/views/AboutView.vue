<template>
  <div class="about">
    <h1>This is an about page</h1>
  
      <b-card
    title="Card Title"
    img-src="https://picsum.photos/600/300/?image=25"
    img-alt="Image"
    img-top
    tag="article"
    style="max-width: 20rem;"
    class="mb-2"
  >
    <b-card-text>
      Some quick example text to build on the card title and make up the bulk of the card's content.
    </b-card-text>

    <b-button href="#" variant="primary">Go somewhere</b-button>
  </b-card>
    </div>
    
  
</template>

<script>

export default {
  components: { },
  data() {
    return {
      formData: {
        market: ""
      },
      formInput: {
        marketOptions: [
          { text: "BSE", value: "BSE" },
          { text: "NSE", value: "NSE" },
        ],
      },
    };
  },
  mounted() {
    
  },
  methods: {
   
  },
  computed: {},
};
</script>

<style scoped>

#bs_container {
  max-width: 95%;
}

.filter-col {
  background-color: #f5f3f3;
  border-radius: 15px;
  padding-bottom: 10px;
  padding-left: 5px;
  padding-right: 5px;
  background-clip: content-box;
  height: 100px;
}

#market {
  padding-bottom: 10px;
}
</style>
