<template>
  <div>
    <mdb-progress :height="this.height" :value="this.loading">
      Loading {{ this.loading }}%
    </mdb-progress>

    <mdb-input
      class="mt-0 mb-3"
      placeholder="Redis Search. Click Help for query options."
      v-model="search"
    >
      <mdb-btn color="info" group slot="append" @click="showSearchInfo">
        Help
      </mdb-btn>
      <mdb-tooltip trigger="hover" :options="{ placement: 'left' }">
        <span slot="tip" v-if="this.disableSearch">Disabled while data loads.</span>
        <mdb-btn
          color="default"
          group
          slot="reference"
          id="search-button"
          v-on:click="searchQuery"
          v-bind:disabled="this.disableSearch"
        >
          Enter
        </mdb-btn>
      </mdb-tooltip>
    </mdb-input>

    <mdb-datatable-2
      v-model="data"
      striped
      bordered
      arrows
      scrollY
      maxHeight="500px"
    />
  </div>
</template>

<script>
import {
  mdbDatatable2,
  mdbInput,
  mdbProgress,
  mdbBtn,
  mdbTooltip
} from "mdbvue";

export default {
  name: "DataTable",
  props: {
    url: String
  },
  components: {
    mdbDatatable2,
    mdbInput,
    mdbProgress,
    mdbBtn,
    mdbTooltip
  },
  data() {
    return {
      loading: 0,
      height: 20,
      disableSearch: true,
      search: "",
      data: {
        rows: [],
        columns: []
      }
    };
  },
  methods: {
    showSearchInfo() {
      this.$emit("showSearchInfo");
    },
    searchQuery() {
      let search_string = "*";
      this.disableSearch = true;
      this.loading = 0;
      this.height = 20;
      this.data = {
        rows: [],
        columns: []
      };

      const filters = {};
      for (const query of this.search.split("&")) {
        const [prefix, value] = query.trim().split(":");
        if (prefix === "SC_NAME") {
          search_string = value;
        } else {
          filters[prefix] = value;
        }
      }

      this.fetchData(search_string, filters);
    },
    async fetchData(search, filters) {
      // should match with backend
      const MAX_ENTRIES = 4000;
      const intervals = 100;
      let ct = 0;

      while (ct <= MAX_ENTRIES) {
        let url = new URL(this.url);
        url.searchParams.append("start", ct);
        url.searchParams.append("query_string", search);
        url.searchParams.append("filters", JSON.stringify(filters));

        await fetch(url)
          .then(res => res.json())
          .then(json => {
            this.data = {
              columns: json.columns,
              rows: this.data.rows.concat(json.rows)
            };

            this.loading += (intervals * 100) / MAX_ENTRIES;
            if (this.loading >= 100) {
              this.height = 0;
              this.disableSearch = false;
            }
          })
          .catch(err => console.log(err));

        ct += intervals + 1;
      }
    }
  },
  mounted() {
    this.fetchData("*", {});
  }
};
</script>

<style>
.btn.disabled {
  /* Display tooltip on button even when disabled */
  pointer-events: auto !important;
}
.tooltip {
  pointer-events: none;
}
</style>
