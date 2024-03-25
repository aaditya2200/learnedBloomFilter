import { Kafka } from "kafkajs";

const kafka = new Kafka({
  clientId: "my-ecommerce-app",
  brokers: ["localhost:29092"],
});

const producer = kafka.producer();

const activityTypes = ["view", "click", "purchase"];
const categories = [
  "electronics",
  "fashion",
  "furniture",
  "toys",
  "books",
  "home appliances",
  "sports",
  "automotive",
  "jewelry",
  "travel",
  "party supplies",
];
const devices = ["android", "ios", "mac", "windows", "linux"];
const locations = [
  "New York",
  "Los Angeles",
  "SaltLakeCity",
  " Chicago",
  "Boston",
  "Newyork",
  "Houston",
  "Phoenix",
  "Philadelphia",
  "San Antonio",
  "San Diego",
  "Dallas",
  "San Jose",
  "Austin",
  "San Francisco",
  "Indianapolis",
  "Colorado",
];

function getRandomElement<T>(array: T[]): T {
  return array[Math.floor(Math.random() * array.length)];
}

const generateActivity = () => ({
  userId: `${Math.floor(Math.random() * 1000000)}`,
  activityType: getRandomElement(activityTypes),
  productId: `product${Math.floor(Math.random() * 1000)}`,
  timestamp: new Date().toISOString(),
  category: getRandomElement(categories),
  price: Math.random() * 1200,
  location: getRandomElement(locations),
  device: getRandomElement(devices),
});

const produceMessage = async () => {
  try {
    const message = generateActivity();

    await producer.send({
      topic: "ecommerce_activity",
      messages: [{ value: JSON.stringify(message) }],
    });
  } catch (err) {
    console.log(err);
  }
};

const run = async () => {
  await producer.connect();

  setInterval(produceMessage, 10000);
};

run().catch(console.error);
