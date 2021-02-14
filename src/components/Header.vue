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
  name: "Header",
  props: {
    heading: String,
    info: String
  }
};
</script>

<style scoped lang="scss">
.top {
  background: #262626;

  img {
    height: inherit;
    max-height: 100px;
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
