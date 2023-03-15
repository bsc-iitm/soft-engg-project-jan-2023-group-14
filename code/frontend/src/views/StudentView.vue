<template>
    <div>
      <h1>This is student view page. This page will be deleted. It should not be visible.</h1>
    </div>
</template>

<script>
export default {
  name: 'StudentView',
  components: {},
  data() {
    return {
      profile_pic_url: "https://blog.hubspot.com/hs-fs/hubfs/Google%20Drive%20Integration/Untitled%20document-Mar-24-2021-04-57-46-58-PM.jpeg?width=650&name=Untitled%20document-Mar-24-2021-04-57-46-58-PM.jpeg",
      buttons: [
        { id: 1, title: "Home", link: "/student", active: true },
        { id: 2, title: "Create Ticket", link: "/student-home", active: false },
        { id: 3, title: "My Tickets", link: "/student", active: false },
        { id: 4, title: "FAQs", link: "/student", active: false },
        { id: 5, title: "Logout", link: "#", active: false },
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
      if (id_ == 5) {
        // logout pressed
        // this is temporary. logout component will be added soon
        // On logout -> delete user data
        this.$store.dispatch('set_state_after_logout', {});
        this.$router.push('/login');

      }
    },
  },
  computed: {},
};
</script>

<style>

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
