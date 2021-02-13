<template>
  <div>
    <br />
    <mdb-input class="mt-0" v-model="search" label="Search by Name" />
    <mdb-datatable-2
      value="http://127.0.0.1:8000/bhavcopy/"
      :searching="{ value: search, field: 'SC_NAME' }"
      striped
      bordered
      arrows
      refresh
      scrollY
      maxHeight="500px"
    />
  </div>
</template>

<script>
import { mdbDatatable2, mdbInput } from "mdbvue";

export default {
  name: "Datatable",
  components: {
    mdbDatatable2,
    mdbInput
  },
  data() {
    return {
      search: ""
    };
  }
};
</script>

<style></style>
