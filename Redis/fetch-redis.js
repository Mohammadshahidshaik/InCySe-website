const redis = require('redis');

const client = redis.createClient({
    socket: {
        host: '10.203.12.106',  // Replace with your Redis host
        port: 6379
    },
    password: 'e87052bfcc0b65b2d0603ad4baa8d8ced7aa929b6698a568d2ce53dfd2dc04bcs'  // Use your actual Redis password
});

async function fetchData() {
    try {
        await client.connect();
        console.log("✅ Connected to Redis successfully!");

        // 🔹 Fetch all keys (Modify if you have a specific key pattern)
        const keys = await client.keys('*');
        console.log("🔑 Available Keys:", keys);

        // Fetch the specific key where the data is stored
        const redisKey = 'P1_key-value';  // Change this if necessary
        const rawData = await client.get(redisKey);
        
        if (!rawData) {
            console.log(`❌ No data found for key: ${redisKey}`);
            return;
        }

        // 🔹 Parse JSON data
        const row_dict = JSON.parse(rawData);
        console.log("📦 Retrieved Data:", row_dict);

        // Extracting values
        const date = row_dict.date;
        const time = row_dict.time;
        const state = row_dict.State;  // Nested object
        const measure = row_dict.Measure;  // Nested object

        console.log(`📅 Date: ${date}, ⏰ Time: ${time}`);
        console.log("📊 State Data:", state);
        console.log("📏 Measurement Data:", measure);

    } catch (error) {
        console.error("❌ Redis Fetch Error:", error);
    } finally {
        await client.disconnect();
    }
}

// Run fetch function
fetchData();
