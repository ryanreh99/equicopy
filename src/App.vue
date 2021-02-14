<template>
  <div id="app">
    <Header
      heading="Equicopy"
      info="The contents get refreshed everyday at 6:00pm except on Saturday and Sunday. For this case, the latest released data will be displayed."
    />
    <Datatable />
  </div>
</template>

<script>
// Add Footer
import "bootstrap-css-only/css/bootstrap.min.css";
import "mdbvue/lib/css/mdb.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";

import Header from "./components/Header.vue";
import Datatable from "./components/Datatable.vue";

export default {
  name: "App",
  components: {
    Header,
    Datatable
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
