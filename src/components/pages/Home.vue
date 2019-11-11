<template>
  <div class="container">
    <h1 class="tile is-info title notification">Feature Finder</h1>
    <FeatureFinder />
  </div>
</template>

<style lang="scss" scoped>

</style>

<script>
import FeatureFinder from "../organisms/FeatureFinder.vue";

export default {
  name: "home",
  components: {
    FeatureFinder
  }
};
</script>
