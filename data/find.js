const fs = require("fs");

const data = JSON.parse(fs.readFileSync("text.json").toString());

// console.log(data);

const search = [
  '-delayed release'
];

function loadFeature(feature = '') {
  const val = feature[0];
  const feat = feature.substring(1);

  return [val, feat];
}

function phoneHasFeature(phone = '', featureset = [[]]) {
  return featureset.every(([val, feat]) => {
    return data[phone][feat] === val;
  });
}

const params = search.map(loadFeature);

const phones = Object.keys(data).filter(phone => {
  return phoneHasFeature(phone, params);
});



console.log(phones);