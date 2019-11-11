import request from "superagent";

type Dataset = {
  [phone: string]: {
    [feature: string]: string;
  };
};

function isDataset(dataset: any): dataset is Dataset {
  if (!dataset) {
    return false;
  }

  if (typeof dataset === "object") {
    const internallySound = Object.keys(dataset).every(key => {
      const featureset = dataset[key];
      if (typeof featureset !== "object") {
        return false;
      }

      return Object.keys(featureset).every(key => typeof key === "string");
    });

    return internallySound;
  }

  return false;
}

function phoneHasFeatures(
  dataset: Dataset,
  phone: string,
  featureset: string[]
) {
  return featureset.every(feature => {
    const val = feature[0];
    const feat = feature.substring(1);

    return dataset[phone][feat] === val;
  });
}

export class Phones {
  private data: Dataset | null = null;
  private cachedFeatures: string[] | null = null;

  public get isInit() {
    return !!this.data;
  }

  public allFeatures() {
    if (this.cachedFeatures) {
      return this.cachedFeatures;
    }
    const data = this.getData();

    const featureset = data[Object.keys(data)[0]];
    this.cachedFeatures = Object.keys(featureset);
    return this.cachedFeatures;
  }

  async init() {
    const data = await request.get("/text.json");
    if (!isDataset(data.body)) {
      throw new Error("Not a dataset!");
    }
    this.data = data.body;
  }

  getPhones(features: string[]) {
    const data = this.getData();

    return Object.keys(data).filter(phone =>
      phoneHasFeatures(data, phone, features)
    );
  }

  getFeatureset(phone: string) {
    const data = this.getData();
    return data[phone];
  }

  // available so that we can do a null check
  private getData() {
    const { data } = this;
    if (data === null) {
      throw new Error("Has not been initialized correctly!");
    }

    return data;
  }
}

export function getFeatures(input: string) {
  return input.replace(",", "").split(" ");
}
