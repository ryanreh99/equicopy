<template>
  <div id="app">
    <Header heading="Equicopy" url="http://localhost:8000/getCSV/" />
    <Datatable
      url="http://localhost:8000/bhavcopy/"
      @showSearchInfo="showSearchInfo"
    />
    <HelpModal
      v-bind:showModal="this.showModal"
      @hideSearchInfo="hideSearchInfo"
    />
  </div>
</template>

<script>
// Add Footer
import "bootstrap-css-only/css/bootstrap.min.css";
import "mdbvue/lib/css/mdb.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";

import Header from "./components/Header.vue";
import Datatable from "./components/Datatable.vue";
import HelpModal from "./components/HelpModal.vue";

export default {
  name: "App",
  components: {
    Header,
    Datatable,
    HelpModal
  },
  data() {
    return {
      showModal: false
    };
  },
  methods: {
    showSearchInfo() {
      this.showModal = true;
    },
    hideSearchInfo() {
      this.showModal = false;
    }
  }
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap");
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background: white;
}
</style>
