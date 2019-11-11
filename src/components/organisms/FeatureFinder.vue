<template>
  <div>
    <form @submit="handleSubmit">
      <input class="input" v-model="search" />
    </form>
    <span :class="getClass(feature)" v-for="feature in activeFeatures" v-bind:key="feature">
      {{ feature }}
      <button class="delete" @click="removeActive(feature)"></button>
    </span>
    <hr />

    <span @click="handlePhoneClick(phone)" class="tag is-primary phone button" v-for="phone in found" v-bind:key="phone">{{ phone }}</span>

    <div :class="modalClass">
      <div class="modal-background"></div>
      <div class="modal-content box">
        <!-- Any other Bulma elements you want -->
        <p>{{ modalInfo }}</p>
      </div>
      <button @click="handleModalClose" class="modal-close is-large" aria-label="close"></button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.phone {
  font-size: 22px;
  margin: 5px;
}

.feature {
  margin: 4px;
}
</style>

<script lang="ts">
import Vue from "vue";
import { ref, watch, computed } from "@vue/composition-api";

import { Phones, getFeatures } from "@/utils.ts";

export default Vue.extend({
  setup() {
    const search = ref("");
    const found = ref([] as string[]);
    const activeFeatures = ref([] as string[]);
    const modalInfo = ref("");
    const modalClass = computed(() => ({
      modal: true,
      "is-active": modalInfo.value.length > 0
    }));

    const phones = new Phones();

    watch(activeFeatures, async () => {
      if (!phones.isInit) {
        await phones.init();
      }

      found.value = phones.getPhones(activeFeatures.value);
    });

    function getClass(feature: string) {
      const normalClasses = "tag feature is-large ";
      const val = feature[0];
      switch (val) {
        case "+":
          return normalClasses + "is-success";

        case "-":
          return normalClasses + "is-danger";

        default:
          return normalClasses;
      }
    }

    function removeActive(feature: string) {
      activeFeatures.value = activeFeatures.value.filter(f => f !== feature);
    }

    function handleSubmit(e: Event) {
      e.preventDefault();
      if (search.value.length < 1) {
        return;
      }

      switch (search.value[0]) {
        case "+":
        case "-":
        case "0":
          activeFeatures.value.push(search.value);
          break;
      }

      search.value = "";
    }

    function handlePhoneClick(phone: string) {
      const features = phones.getFeatureset(phone);
      const data = Object.keys(features).map(feature => {
        const value = features[feature];

        return value + feature;
      });
      // TODO: make this prettier
      modalInfo.value = JSON.stringify(data, null, 4);
    }

    function handleModalClose() {
      modalInfo.value = "";
    }

    return {
      search,
      found,
      activeFeatures,
      getClass,
      removeActive,
      handleSubmit,
      handlePhoneClick,
      modalClass,
      modalInfo,
      handleModalClose
    };
  }
});
</script>
