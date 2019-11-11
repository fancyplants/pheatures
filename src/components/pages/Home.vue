<template>
  <div class="container">
    <h1 class="tile is-info title notification">Feature Finder</h1>
    <FeatureFinder v-if="state.homeState === 'ready'" :phones="state.phones" />
    <template v-else-if="state.homeState === 'loading'">
      <h1 class="centered box bigfont">Loading...</h1>
    </template>
    <template v-else>
      <h1 class="centered box is-warning notification bigfont">Unable to load.</h1>
    </template>
  </div>
</template>

<style lang="scss" scoped>
.bigfont {
  font-size: 22px;
}
</style>

<script lang="ts">
import Vue from "vue";
import FeatureFinder from "../organisms/FeatureFinder.vue";
import { ref, reactive } from '@vue/composition-api';
import { Phones } from '../../utils';

type HomeState = "loading" | "error" | "ready";

export default Vue.extend({
  name: "home",
  components: {
    FeatureFinder
  },
  setup() {
    const state = reactive({
      homeState: "loading" as HomeState,
      phones: null as unknown
    });

    Phones.getPhoneInstance()
      .then((phones) => {
        state.homeState = "ready";
        state.phones = phones;
      })
      .catch((error) => {
        console.error(error);
        state.homeState = "error";
      });

    return {
      state
    };
  }
});
</script>
