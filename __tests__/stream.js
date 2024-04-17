async function readStream(apiUrl, query) {
  const res = {
    err: null
  };

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ "input": query, "chat_history": [] })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }
      const text = decoder.decode(value);
      try {
        const obj = JSON.parse(text);
        if (obj.output) {
          process.stdout.write(obj.output?.result ?? obj.output);
        } else if (obj.action) {
          process.stdout.write(`Running \`${obj.action}\`...\n`);
        }
      } catch (error) {
        console.log("Invalid JSON... skipping");
      }
    }

    console.log("\nResponse Finished.");
  } catch (error) {
    res.err = error;
  }

  return res;
}

const API = "http://localhost:8080/api/chat";

if (process.argv.length === 2) {
  console.log("Provide a query!");
  process.exit(1);
} 

readStream(API, process.argv[2])
.then((res) => console.log(res.err != null ? "❎ TEST FAILED" : "✅ TEST PASSED"))
