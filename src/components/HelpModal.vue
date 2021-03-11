<template>
  <div>
    <mdb-modal v-if="showModal" @close="hideSearchInfo">
      <mdb-modal-header>
        <mdb-modal-title tag="h4" class="w-100 text-center font-weight-bold"
          >Searching</mdb-modal-title
        >
      </mdb-modal-header>
      <mdb-modal-body>
        <p>
          The <code>SC_NAME</code> queries value should always be in Upper
          Case.<br />
          Append a <code>*</code> to the string to perform prefix based search.
          Else the string has to ben an exact match.<br />
          <code>MIN_PREFIX_LENGTH</code> has been set to 2 (default).
        </p>

        <p>
          You can perform <code>SC_NAME</code> query according to the rules
          mentioned at
          <a href="https://oss.redislabs.com/redisearch/Query_Syntax/"
            >the official redisearch docs</a
          >.
        </p>

        <p>
          To add Numeric filters, seperate the queries with
          <code>&</code>.<br />
          And the value string containing <code>,</code> should have no
          spaces.<br />
          Decimal values are also allowed.
        </p>

        <p>
          Possible Numeric filters include:
          <code
            >[ 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST', 'PREVCLOSE', 'NO_TRADES',
            'NO_OF_SHRS', 'NET_TURNOV', ]
          </code>
        </p>

        <h4>Example Queries:</h4>
        1.) <code>SC_NAME: CRES* & OPEN: 0.23,78.6 & LAST: 22.1,40</code>
        <br />
        2.) <code>SC_NAME: BH*</code>
      </mdb-modal-body>
    </mdb-modal>
  </div>
</template>

<script>
import { mdbModal, mdbModalHeader, mdbModalTitle, mdbModalBody } from "mdbvue";
export default {
  name: "HelpModal",
  props: {
    showModal: Boolean
  },
  components: {
    mdbModal,
    mdbModalHeader,
    mdbModalTitle,
    mdbModalBody
  },
  data() {
    return {};
  },
  methods: {
    hideSearchInfo() {
      this.$emit("hideSearchInfo");
    }
  }
};
</script>

<style></style>
