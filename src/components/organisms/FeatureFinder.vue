<template>
  <div>
    <form @submit="handleSubmit">
      <input class="input" v-model="search" />
    </form>
    <FeatureTag
      v-for="feature in activeFeatures"
      v-bind:key="feature"
      :feature="feature"
      :deletable="true"
      @delete="removeActive"
    />
    <hr />

    <Phone @click="handlePhoneClick" v-for="phone in found" v-bind:key="phone" :phone="phone" />

    <div :class="modalClass">
      <div class="modal-background"></div>
      <div class="modal-content box">
        <!-- Any other Bulma elements you want -->
        <FeatureTag v-for="feature in modalInfo" v-bind:key="feature" :feature="feature" />
      </div>
      <button @click="handleModalClose" class="modal-close is-large" aria-label="close"></button>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { ref, watch, computed } from "@vue/composition-api";

import FeatureTag from "@/components/atoms/FeatureTag.vue";
import Phone from "@/components/atoms/Phone.vue";
import { Phones, getFeatures } from "@/utils.ts";

export default Vue.extend({
  components: {
    FeatureTag,
    Phone
  },
  setup() {
    const phones = new Phones();

    const search = ref("");
    const found = ref([] as string[]);
    const activeFeatures = ref([] as string[]);
    const modalInfo = ref([] as string[]);
    const modalClass = computed(() => ({
      modal: true,
      "is-active": modalInfo.value.length > 0
    }));

    watch(activeFeatures, async () => {
      if (!phones.isInit) {
        await phones.init();
      }

      found.value = phones.getPhones(activeFeatures.value);
    });

    function removeActive(feature: string) {
      activeFeatures.value = activeFeatures.value.filter(f => f !== feature);
    }

    async function handleSubmit(e: Event) {
      e.preventDefault();
      if (search.value.length < 1) {
        return;
      }

      if (!phones.isInit) {
        await phones.init();
      }

      const features = phones.allFeatures();

      switch (search.value[0]) {
        case "+":
        case "-":
        case "0":
          const feat = search.value.substring(1);
          if (features.includes(feat)) {
            activeFeatures.value.push(search.value);
          }
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
      modalInfo.value = data;
    }

    function handleModalClose() {
      modalInfo.value = [];
    }

    return {
      search,
      found,
      activeFeatures,
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
