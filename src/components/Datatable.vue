<template>
  <div>
    <br />
    <mdb-input class="mt-0" v-model="search" label="Search by Name" />
    <mdb-datatable-2
      v-model="data"
      :searching="{ value: search, field: 'title' }"
      striped
      bordered
      arrows
      scrollY
      maxHeight="500px"
    />
  </div>
</template>

<script>
  import { mdbDatatable2, mdbInput } from 'mdbvue';
  export default {
    components: {
      mdbDatatable2,
      mdbInput,
    },
    data() {
      return {
        search: "",
        data: {
          rows: [],
          columns: [],
        },
      };
    },
    mounted(){
      let ct = 0;

      while (ct <= 3500) {
        let url = new URL('http://localhost:8000/bhavcopy/')
        url.searchParams.append("start", ct)

        fetch(url)
        .then(res => res.json())
        .then(json => {
          this.data = {
            columns: json.columns,
            rows: this.data.rows.concat(json.rows),
          };
        })
        .catch(err => console.log(err));
      
        ct += 100 + 1;
      }
    }
  };
</script>

<style></style>
