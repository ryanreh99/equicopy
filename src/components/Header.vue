<template>
  <div class="top">
    <img alt="Vue logo" src="../assets/logo.png" />
    <h1>{{ heading }}</h1>
    <p>
      This displays the latest 
      <a href="https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx">BhavCopy</a>
      published by the BSE and is updated everyday at 6:00pm
    </p>
  </div>
</template>

<script>
export default {
  name: "Header",
  props: {
    heading: String,
  }
};
</script>

<style scoped lang="scss">
.top {
  background: #262626;
  padding-bottom: 10px;

  img {
    height: inherit;
    max-height: 100px;
    float: right;
  }

  h1, p {
    color: #fbfbfb;
    text-align: center;
  }
}
</style>
