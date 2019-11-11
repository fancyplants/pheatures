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
  private data: Dataset;
  public readonly allFeatures: Set<string>;

  private constructor(data: Dataset) {
    this.data = data;

    const featureset = data[Object.keys(data)[0]];
    this.allFeatures = new Set(Object.keys(featureset));
  }

  static async getPhoneInstance() {
    const data = await request.get("/text.json");
    if (!isDataset(data.body)) {
      throw new Error("Not a dataset!");
    }
    return new Phones(data.body);
  }

  getPhones(features: string[]) {
    const { data } = this;

    return Object.keys(data).filter(phone =>
      phoneHasFeatures(data, phone, features)
    );
  }

  getFeatureset(phone: string) {
    return this.data[phone];
  }
}

export function getFeatures(input: string) {
  return input.replace(",", "").split(" ");
}
