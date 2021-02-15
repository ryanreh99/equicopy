<template>
  <div>
    <mdb-progress :height="this.height" :value="this.loading">
      Loading {{ this.loading }}%
    </mdb-progress>
    <br />

    <mdb-input class="mt-0" v-model="search" label="Search by Name" />

    <mdb-datatable-2
      v-model="data"
      :searching="{ value: search, field: 'SC_NAME' }"
      striped
      bordered
      arrows
      scrollY
      maxHeight="500px"
    />
  </div>
</template>

<script>
import { mdbDatatable2, mdbInput, mdbProgress } from "mdbvue";
export default {
  name: "DataTable",
  props: {
    url: String
  },
  components: {
    mdbDatatable2,
    mdbInput,
    mdbProgress
  },
  data() {
    return {
      height: 20,
      loading: 0,
      search: "",
      data: {
        rows: [],
        columns: []
      }
    };
  },
  mounted() {
    let ct = 0;
    const MAX_ENTRIES = 4000;
    const intervals = 100; // should match with backend

    while (ct <= MAX_ENTRIES) {
      let url = this.url + "?start=" + ct;

      fetch(url)
        .then(res => res.json())
        .then(json => {
          this.data = {
            columns: json.columns,
            rows: this.data.rows.concat(json.rows)
          };

          if (json.rows.length < intervals) this.height = 0;
          this.loading = parseInt(
            Math.min((this.data.rows.length * 100) / MAX_ENTRIES, 100)
          );
        })
        .catch(err => console.log(err));

      ct += intervals + 1;
    }
  }
};
</script>

<style></style>
