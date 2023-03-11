<template>
    <div>
      <b-navbar toggleable="lg" type="light" variant="light">
        <b-navbar-brand href="#">OSTS</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <div class="buttons" v-for="b in buttons" :key="b.id">
              <b-button
                variant="primary"
                :to="{ path: b.link }"
                @click="change_button_state(b.id)"
                :style="{
                  boxShadow: b.active ? '5px 5px 15px 5px #a3a3a3' : 'none',
                  backgroundColor: b.active ? 'blue' : '#f8f9fa',
                  color: b.active ? 'white' : 'black',
                  borderColor: b.active ? '#007bff' : '#f8f9fa',
                  fontSize: b.active ? '18px' : '16px',
                }"
                >{{ b.title }}</b-button
              >
            </div>
          </b-navbar-nav>

          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-button id="profile_pic" :style="{backgroundImage: 'url(' + profile_pic_url + ')'}"></b-button>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
</template>

<script>
export default {
  name: 'StudentHome',
  components: {},
  data() {
    return {
      profile_pic_url: "https://blog.hubspot.com/hs-fs/hubfs/Google%20Drive%20Integration/Untitled%20document-Mar-24-2021-04-57-46-58-PM.jpeg?width=650&name=Untitled%20document-Mar-24-2021-04-57-46-58-PM.jpeg",
      buttons: [
        { id: 1, title: "Home", link: "/", active: true },
        { id: 2, title: "Create Ticket", link: "/", active: false },
        { id: 3, title: "My Tickets", link: "/", active: false },
        { id: 4, title: "FAQs", link: "/", active: false },
        { id: 5, title: "Logout", link: "/student_home", active: false },
      ],
    };
  },
  mounted() {},
  methods: {
    change_button_state(id_) {
      for (let b of this.buttons) {
        if (b.id == id_) {
          b.active = true;
        } else {
          b.active = false;
        }
      }
    },
  },
  computed: {},
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #4dd325;
}

nav a.router-link-exact-active {
  color: #441ada;
}

.buttons {
  margin: 15px;
  justify-content: space-between;
}

#profile_pic {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-repeat: no-repeat;
  background-size: cover;
}

router-link {
  box-shadow: 5px 10px 8px 10px #888888;
  background-color: aqua;
}
</style>
