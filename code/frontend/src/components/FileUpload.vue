<template>
  <div class="container">
    <div>
      <label
        >Upload files
        <input type="file" @change="handleFileUpload($event)" multiple />
      </label>
      <br />
      <p style="font-size: 12px">Only <code>.jpg, .png, .gif</code> formats are allowed</p>
      <!-- <div class="mt-2">
        Selected files:
        <span v-for="(file, index) in form.attachments" :key="index">{{ file ? file.name : "" }}</span>
      </div> -->
    </div>
  </div>
</template>

<script>
import * as common from "../assets/common.js";

export default {
  components: {},
  data() {
    return {
      attachments: [],
      user_id: this.$store.getters.get_user_id,
    };
  },
  mounted() {},
  methods: {
    fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
      });
    },
    checkFileExtension() {},
    handleFileUpload: async function (event) {
      const files = event.target.files;
      console.log("files length: ", files.length);
      for (let i = 0; i < files.length; i++) {
        try {
          const result = await this.fileToBase64(files[i]);
          console.log("pushing ", i, "element");
          let attach = {
            user_id: this.user_id, 
            attachment_loc: result
            }
          this.attachments.push(attach);
          console.log("length ", this.attachments.length);
          // console.log('inside file upload')
          // console.log('form image: ', JSON.stringify(this.form), '---------');

          this.$emit("file_uploading", this.attachments);
        } catch (error) {
          console.error(error);
        }
      }
    },
  },
  computed: {},
};
</script>

<style></style>
