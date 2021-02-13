<template>
  <div class="top">
    <img alt="Vue logo" src="../assets/logo.png" />
    <h1>{{ heading }}</h1>
    <br />
    <h5>{{ info }}</h5>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  props: {
    heading: String,
    info: String
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.top {
  background: #262626;
  height: 130px;

  img {
    height: inherit;
    float: right;
  }

  h1 {
    color: #fbfbfb;
    text-align: center;
  }
  h5 {
    color: #fbfbfb;
  }
}
</style>
